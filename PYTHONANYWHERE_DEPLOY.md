# Deploy to PythonAnywhere

PythonAnywhere does not use `python manage.py runserver`. Create a Web app in the
PythonAnywhere **Web** tab and point its WSGI file to this Django project.

## 1. Upload the project

Upload `football_team_site-pythonanywhere.zip` to PythonAnywhere, then open a
Bash console and run:

```bash
cd ~
unzip football_team_site-pythonanywhere.zip
cd football_team_site
```

## 2. Create `.env`

Replace `YOUR_USERNAME` with your PythonAnywhere username:

```bash
cat > .env <<'EOF'
SECRET_KEY=change-this-to-a-long-random-secret-key
DEBUG=False
ALLOWED_HOSTS=YOUR_USERNAME.pythonanywhere.com,localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
EOF
```

## 3. Create virtualenv and install dependencies

Use the same Python version when creating the Web app later:

```bash
mkvirtualenv --python=/usr/bin/python3.10 football_team_site-venv
pip install -r requirements-pythonanywhere.txt
```

## 4. Prepare database and static files

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

If you did not upload the local `db.sqlite3`, create a new admin user:

```bash
python manage.py createsuperuser
```

## 5. Configure the Web tab

In PythonAnywhere:

1. Open **Web**.
2. Add a new web app.
3. Choose **Manual configuration**, not the Django wizard.
4. Choose Python 3.10.
5. Set the virtualenv to:

```text
/home/YOUR_USERNAME/.virtualenvs/football_team_site-venv
```

6. Set source code and working directory to:

```text
/home/YOUR_USERNAME/football_team_site
```

7. Edit the WSGI file and use `pythonanywhere_wsgi.py.example` as the template.
   Replace `YOUR_USERNAME` with your PythonAnywhere username.

## 6. Static and media files

In the Web tab, add these static mappings:

```text
/static/ -> /home/YOUR_USERNAME/football_team_site/staticfiles
/media/  -> /home/YOUR_USERNAME/football_team_site/media
```

Then press **Reload**.
