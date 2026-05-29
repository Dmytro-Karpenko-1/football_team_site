# Football Team Site

Професійний сайт футбольної команди на Django.

## Функціональність

- 📱 Інформація про команду та гравців
- ⚽ Управління матчами та результатами
- 🏆 Таблиця результатів ліги
- 📰 Блог з новинами команди
- 👥 Управління спонсорами
- 📝 Форма для приєднання до команди

## Структура проєкту

```
football_team_site/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── config/                # Django configuration
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI application
├── team/                  # Main Django app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # App URL routing
│   ├── forms.py           # Django forms
│   └── admin.py           # Admin interface
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── home.html          # Home page
│   └── team/              # Team-related templates
├── static/                # Static files
│   ├── css/               # CSS files
│   ├── js/                # JavaScript files
│   └── images/            # Images
└── media/                 # User uploads
    ├── team/
    ├── players/
    ├── coaches/
    └── blog/
```

## Встановлення та запуск

### 1. Активація віртуального оточення
```bash
source .venv/bin/activate
```

### 2. Встановлення залежностей
```bash
pip install -r requirements.txt
```

### 3. Застосування міграцій
```bash
python manage.py migrate
```

### 4. Створення суперюзера
```bash
python manage.py createsuperuser
```

### 5. Запуск розробницького сервера
```bash
python manage.py runserver
```

Сайт буде доступний за адресою: http://localhost:8000/
Адміністративна панель: http://localhost:8000/admin/

## Моделі

- **Team** - Інформація про команду
- **Player** - Гравці команди
- **Coach** - Тренери
- **Match** - Матчі та результати
- **Standing** - Таблиця результатів
- **BlogPost** - Статті блогу
- **Sponsor** - Спонсори команди

## Вимоги

- Python 3.8+
- Django 5.0+
- Pillow (для роботи з зображеннями)
- python-dotenv (для змінних оточення)

## Ліцензія

MIT License
