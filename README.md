# Scrape_articles

Zadanie rekrutacyjne - Junior Python Developer | Take Group

## Instalacja


### Wymagania 

- Python 3.10+
- Django 5.x
- Django REST Framework
- PosgreSQL / Sqlite
- Playwright
- Docker / Lokalnie 

### Kroki bez dockera (Niezalecane)
***

1. **Sklonuj repozytorium**:
    ```sh
    git clone https://github.com/CrazyMonkey0/scrape_articles.git
    cd scrape_articles
    ```

2. **Utwórz i aktywuj środowisko wirtualne**:
    ```sh
    python -m venv venv
    # Linux
    source venv/bin/activate  
    # Windows CMD
    source venv\Scripts\activate
    # Windows PowerShell
    .\venv\Scripts\Activate.ps1
    ```

3. **Zainstaluj zależności**:
    ```sh
    pip install -r requirements.txt
    playwright install firefox
    ```

4. **Skonfiguruj bazę danych**:
    ```sh
    # Przejdź do scrapearticles/settings
    # Wyszukaj 
    DATABASES = {
        "default": {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': 'db',
            'PORT': 5432,
            }
    }

    # Zmień Name, User, Password, Host, Port pod twoją konfigurację bazy danych

    # Lub 

    # Użyj Sqlite
    # Wystarczy zakomentować powyższą konfigurację(#) 
    # I odkomentować ten kawałek kodu 
    DATABASES = {
                'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
  
    ```

5. **Zastosuj migrację**:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Wyscrapuj treści ze strony**:
    ```sh
    python manage.py scrape_articles
    ```

7. **Wystartuj serwer (Tylko w fazie deweloperskiej!)**:
    ```sh
    python manage.py runserver
    ```

8. **Dostęp do aplikacji**:
    - Api: `http://localhost:8000/api`
    - Admin: `http://localhost:8000/admin`

### Kroki (Docker)
***

1. **Sklonuj repozytorium**:
    ```sh
    git clone https://github.com/CrazyMonkey0/scrape_articles.git
    cd scrape_articles
    ```

2. **Stwórz i uruchom obraz dockera**:
    ```sh
    # Wszystko robi się automatycznie wraz z scrapowaniem :>
    docker-compose up --build
    ```

3. **Dostęp do aplikacji**:
    - Api: `http://localhost:8000/api`
    - Admin: `http://localhost:8000/admin`


## Endpointy API 


- **Endpoint**: `GET api/articles/` - Wyświetla wszystkie artykuły
**Request Body**:
    ```json
    {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 5,
            "title": "asads",
            "content": "asdasda",
            "content_html": "asdasd",
            "url": "https://take-group.github.io/example-blog-without-ssr/co-mozna-zrobic-ze-schabu-oprocz-kotletow-5-zaskakujacych-przepis",
            "published_date": "2111-12-23T21:12:00Z"
        },
    ]
}
    ```
**Opowiedzi**
- `201 Created`
- `400 Bad Request`

***

- **Endpoint**: `POST api/articles/` - Tworzy nowy artykuł
**Request Body**:
    ```json

    {
        "id": 5,
        "title": "asads",
        "content": "asdasda",
        "content_html": "asdasd",
        "url": "https://take-group.github.io/example-blog-without-ssr/co-mozna-zrobic-ze-schabu-oprocz-kotletow-5-zaskakujacych-przepis",
        "published_date": "2111-12-23T21:12:00Z"
    }
    ```
**Opowiedzi**
- `200 OK`

***

- **Endpoint**: `GET api/articles/{id}/` - wyświetla dany artykuł
**Request Body**:
    ```json
    {
        "id": 5,
        "title": "asads",
        "content": "asdasda",
        "content_html": "asdasd",
        "url": "https://take-group.github.io/example-blog-without-ssr/co-mozna-zrobic-ze-schabu-oprocz-kotletow-5-zaskakujacych-przepis",
        "published_date": "2111-12-23T21:12:00Z"
    }
    ```
**Opowiedzi**
- `200 OK`
- `404 Not Found`

***

- **Endpoint**: `PUT api/articles/{id}/` - Zmienia wartość wdanym polu
**Request Body**:
    ```json
    {
        "id": 5,
        "title": "zmienione",
        "content": "pole",
        "content_html": ":>",
        "url": "https://take-group.github.io/Zmienione",
        "published_date": "2111-12-23T21:12:00Z"
    }
    ```
**Opowiedzi**
- `200 OK`
- `400 Bad Request`
- `404 Not Found`

***

- **Endpoint**: `DELETE api/articles/{id}/` - Usuwa dany artykuł

**Opowiedzi**
- `200 OK`
- `204 No Content`
- `404 Not Found`

***

- **Endpoint**: `GET api/articles/?source=take-group.github.io` - wyświetla artykuły o podanym url
**Request Body**:
    ```json
    {
        "id": 5,
        "title": "asads",
        "content": "asdasda",
        "content_html": "asdasd",
        "url": "https://take-group.github.io/example-blog-without-ssr/co-mozna-zrobic-ze-schabu-oprocz-kotletow-5-zaskakujacych-przepis",
        "published_date": "2111-12-23T21:12:00Z"
    }
    ```
**Opowiedzi**
- `200 OK`
