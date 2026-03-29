# Databáze autodílů (Flask demo)

Jednoduchá webová aplikace v Pythonu (Flask + SQLAlchemy) pro evidenci:

- **výrobců a modelů aut**
- **motorů**
- **dílů a jejich kategorií**
- **vazby motor – díl (kompatibilita)**
- **nabídek z e‑shopů s autodíly (API placeholdery pro české obchody)**

## 1. Instalace

Předpoklady:

- Python 3.11+ (doporučeno)

```bash
cd "Databáze - autodíly"
python -m venv .venv
.venv\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt
```

## 2. Inicializace databáze

Aplikace používá SQLite soubor `car_parts.db` v kořenové složce projektu (dá se změnit v `config.py`).

V interaktivní konzoli Pythonu nebo v krátkém skriptu můžete vytvořit tabulky:

```python
from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()
```

Sem také můžete doplnit první data (výrobce, modely, motory, díly, kompatibilitu).

## 3. Spuštění aplikace

```bash
.venv\Scripts\activate
python run.py
```

Aplikace poběží na `http://127.0.0.1:5000/`.

## 4. Struktura projektu

- `run.py` – start aplikace Flask
- `config.py` – konfigurace (DB, režimy)
- `app/__init__.py` – vytvoření Flask aplikace a SQLAlchemy
- `app/models.py` – datový model (výrobci, modely, motory, díly, obchody, nabídky)
- `app/routes.py` – základní stránky (seznam modelů, detail motoru, vyhledávání dílů)
- `app/services/search.py` – jednoduchá logika vyhledávání
- `app/api_clients/` – rozhraní a ukázkový klient pro API obchodů (Auto Kelly / LKQ styl)
- `app/templates/` – HTML šablony (Jinja2)
- `app/static/styles.css` – jednoduchý moderní vzhled

## 5. Napojení na české e‑shopy (API)

Ve složce `app/api_clients/` jsou pouze **ukázkové klienty**:

- `base.py` – abstraktní třída `ShopAPIClient` (společné rozhraní)
- `autokelly_like.py` – příklad klienta pro API podobné Auto Kelly / LKQ

Protože veřejná dokumentace API českých obchodů (Auto Kelly, LKQ, ACI atd.) není běžně dostupná,
je potřeba:

- získat přístup / dokumentaci od konkrétního dodavatele
- doplnit v `AutoKellyLikeAPI` správné endpointy, parametry a mapování odpovědí
- doplnit uložení cen a dostupnosti do modelu `ShopOffer`

Můžeme pak například:

1. Najít díl podle OEM v naší DB (`Part`)
2. Pro daný díl zavolat API klienta (`search_part_by_oem`)
3. Výsledky uložit jako `ShopOffer` (cena, dostupnost, URL)
4. Zobrazit v detailu dílu nebo motoru.

## 6. Další možné rozšíření

- jednoduché administrační rozhraní (přidávání modelů, motorů, dílů přes web)
- filtrování podle roku výroby, paliva, výkonu
- napojení na více e‑shopů a porovnání cen
- přihlášení uživatelů a vlastní seznam oblíbených dílů

