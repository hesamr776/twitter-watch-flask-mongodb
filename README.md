# Flask MongoDB

## Using Docker

- Run `docker-compose up --build`. If there's a timeout error, you can restart the Flask container.
- Head over to `http://localhost:5001` on your browser
- Run tests by doing `docker-compose run --rm web poetry run pytest -s`

## Production

- Use Gunicorn `gunicorn --bind 0.0.0.0:$PORT --reload wsgi:app`

## Vercel

- If you add any new packages on Poetry, re-generate `requirements.txt` as follows: `poetry export -f requirements.txt --output requirements.txt`
