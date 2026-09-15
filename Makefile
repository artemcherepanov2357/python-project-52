install:
	uv sync

tailwind:
	mkdir -p assets/css
	uv run python manage.py tailwind build --force

messages:
	uv run python manage.py makemessages -l ru

compilemessages:
	uv run python manage.py compilemessages

collectstatic:
	uv run python manage.py collectstatic --no-input --clear

migrate:
	uv run python manage.py migrate

setup: install tailwind compilemessages collectstatic migrate

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi