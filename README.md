# Valuta Omregner

Et simpelt CLI-program til valutaomregning via https://www.exchangerate-api.com/.

## Hurtig start (fra GitHub til kørsel)

1. Klon projektet
```bash
git clone <dit-repository-url>
cd valutaOmregner
```

2. Opret virtual environment
```bash
python -m venv venv
```

3. Aktivér virtual environment

Windows (PowerShell):
```bash
.\venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

4. Installer dependencies
```bash
pip install -r requirements.txt
```

5. Kør programmet
```bash
python app.py --from-currency USD --to-currency DKK --amount 100
```

## API key med argparse

Du kan sætte key direkte ved opstart med `--key`:

```bash
python app.py --key DIN_API_KEY --from-currency USD --to-currency EUR --amount 50
```

Hvis du ikke angiver `--key`, prøver programmet at bruge `API_KEY` fra `.env`.
Findes den ikke, bliver du bedt om at indtaste key i terminalen.

## Noter

- API key gemmes i `.env` som `API_KEY=...`.
- `.env` og `venv/` er i `.gitignore`.
- Du kan skrive `python app.py -help` for at få hjælp.
