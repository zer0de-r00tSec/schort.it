# schort.it

Ein einfacher URL-Shortener, gebaut mit FastAPI, SQLAlchemy und Jinja2.

## Features

- URLs kürzen via POST-API
- Kurzlinks weiterleiten
- Admin-View pro Link (Status, Clicks, Erstellungsdatum)
- Aktivieren / Deaktivieren von Links
- Links löschen
- Nginx-Reverse-Proxy ready

## Stack

- **Backend**: Python 3.10+, FastAPI, SQLAlchemy, SQLite
- **Frontend**: Jinja2 Templates, TailwindCSS (CDN)
- **Server**: Uvicorn, Nginx

## Projektstruktur

```
schort.it/
├── shortener_app/
│   ├── __init__.py
│   ├── main.py          # Routes & App
│   ├── crud.py          # DB-Operationen
│   ├── models.py        # SQLAlchemy Models
│   ├── schemas.py       # Pydantic Schemas
│   ├── database.py      # DB-Verbindung
│   ├── config.py        # Settings (.env)
│   ├── keygen.py        # Key-Generierung
│   └── frontend/
│       └── templates/
│           ├── index.html
│           ├── about.html
│           └── admin.html
├── .env
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone https://github.com/deinuser/schort.it.git
cd schort.it
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### .env anlegen

```env
ENV_NAME=Development
BASE_URL=http://127.0.0.1:8000
DB_URL=sqlite:///./shortener.db
```

### Starten

```bash
uvicorn shortener_app.main:app --host 0.0.0.0 --port 8000 --no-access-log
```

## API

### URL kürzen

```bash
POST /url
Content-Type: application/json

{"target_url": "https://example.com"}
```

**Response:**
```json
{
  "url": "https://api.schort.it/ABC123",
  "admin_url": "https://admin.schort.it/ABC123_SECRET"
}
```

### Weiterleitung

```
GET /{key}
```

### Admin-View

```
GET /admin-view/{secret_key}
```

### Link deaktivieren / aktivieren

```
POST /admin-view/{secret_key}/deactivate
POST /admin-view/{secret_key}/reactivate
```

### Link löschen

```
DELETE /admin-view/{secret_key}
```

## Nginx

Die App läuft hinter zwei Nginx-Subdomains:

- `api.schort.it` → FastAPI direkt auf `/`
- `admin.schort.it` → Rewrite `/*` auf `/admin-view/*`

## Lizenz

MIT
