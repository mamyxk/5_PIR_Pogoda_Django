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
python3 manage.py loaddata sensors
python3 manage.py seedsensorlogs 30
```

### To run dev server

```
python3 manage.py runserver
```

### Before deployment:
```
python3 manage.py collectstatic
```
