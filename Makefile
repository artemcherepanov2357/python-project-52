install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --no-input

migrate:
	uv run python manage.py migrate

setup: install collectstatic migrate

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi