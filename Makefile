.PHONY: install tailwind messages compilemessages collectstatic migrate setup build render-start

install:
	uv sync

tailwind:
	mkdir -p assets/css
	uv run python manage.py tailwind build --force

messages:
	uv run python manage.py makemessages -l ru

compilemessages:
	@if command -v msgfmt >/dev/null 2>&1; then \
		uv run python manage.py compilemessages; \
	else \
		echo "msgfmt not found, skipping translation compilation"; \
	fi

collectstatic:
	uv run python manage.py collectstatic --no-input --clear

migrate:
	uv run python manage.py migrate

setup: install tailwind compilemessages collectstatic migrate

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi