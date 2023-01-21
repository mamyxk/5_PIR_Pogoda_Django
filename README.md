### To setup venv and requirements

```
py -m venv venv
venv/scripts/activate
```

```
pip install -r requirements.txt
```

### To seed db with sample data

```
python manage.py loaddata sensors
python manage.py seedsenorlogs 30
```

### To run dev server

```
python manage.py runserver
```

