import argparse
import os
import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from dotenv import load_dotenv, set_key


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Valutaomregner via ExchangeRate API.'
    )
    parser.add_argument('--key', type=str, help='API key til exchangerate-api.com')
    parser.add_argument('--from-currency', type=str, required=True, help='Valutakode fra, fx USD')
    parser.add_argument('--to-currency', type=str, required=True, help='Valutakode til, fx DKK')
    parser.add_argument('--amount', type=float, required=True, help='Beløb der skal omregnes')
    return parser.parse_args()


def get_api_key(cli_key: str | None) -> str | None:
    load_dotenv()

    if cli_key:
        set_key('.env', 'API_KEY', cli_key)
        return cli_key

    env_key = os.getenv('API_KEY')
    if env_key:
        return env_key

    entered_key = input('Ingen --key fundet. Indtast API key (eller tryk Enter for at afslutte): ').strip()
    if entered_key:
        set_key('.env', 'API_KEY', entered_key)
        return entered_key

    return None


def convert_currency(api_key: str, from_currency: str, to_currency: str, amount: float) -> float:
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}'

    with urlopen(url, timeout=15) as response:
        data = json.loads(response.read().decode('utf-8'))

    if data.get('result') != 'success':
        error_type = data.get('error-type', 'ukendt fejl')
        raise ValueError(f'API fejl: {error_type}')

    rates = data.get('conversion_rates', {})
    if to_currency not in rates:
        raise ValueError(f'Valutakoden {to_currency} blev ikke fundet i API-responsen')

    return amount * rates[to_currency]


def main():
    args = parse_args()

    api_key = get_api_key(args.key)
    if not api_key:
        print('Ingen API key angivet. Programmet afsluttes.')
        return

    from_currency = args.from_currency.upper()
    to_currency = args.to_currency.upper()

    try:
        converted_amount = convert_currency(api_key, from_currency, to_currency, args.amount)
    except HTTPError as error:
        print(f'HTTP-fejl: {error.code}')
        return
    except URLError as error:
        print(f'Netværksfejl: {error.reason}')
        return
    except ValueError as error:
        print(error)
        return

    print(f'{args.amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}')


main()