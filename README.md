# Django Boilerplate
Base para Django + TailwindCSS

## Requerimientos
1) **Python 3.10+**
2) **Redis Server** (https://redis.io)
3) **NodeJS +v16** (https://redis.io)
4) PostgreSQL (https://www.postgresql.org)

##Instalación:
1) Creación de entorno virtual e instalación de dependencias

```shell
python3 -m venv .venv
pip install -r requirements.txt
# para TailwindCSS
npm i
```

2) Configuración de fichero de entorno:
```shell
cp .env.example .env
```
los valores siguen el formato definito por [django-environ](https://django-environ.readthedocs.io/en/latest/)

*considerar que las variables definidas en el fichero .env 
se sobreescriben automáticamente por los valores de las variables
de entorno del SO


## Levantar servidor de desarrollo
```shell
source .venv/bin/activate
python ./manage.py runserver 0:8000
```


## Levantar TailwindCSS
```shell
npx tailwindcss -i ./static/tailwind/main.css -o ./static/css/main.css --watch
```


## Levantar Celery Worker
```shell
source .venv/bin/activate
celery -A webapp worker -n celery@localhost --loglevel=INFO
```

## Levantar Celery Beat
```shell
source .venv/bin/activate
celery -A webapp beat --loglevel=INFO
```