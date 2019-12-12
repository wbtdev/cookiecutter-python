.PHONY: format lint test coverage publish

clean-pyc:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

format:
	poetry run isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses --line-width=88 --recursive {{cookiecutter.project_name}}/ tests/
	poetry run black --check -l 88 {{cookiecutter.project_name}}/ tests/

lint: format
	poetry run cruft check
	poetry run mypy --ignore-missing-imports {{cookiecutter.project_name}}/
	poetry run flake8 {{cookiecutter.project_name}}/ tests/ --max-line 8 --ignore F403,F401,W503,E203
	poetry run safety check
	poetry run bandit -r {{cookiecutter.project_name}}/
	poetry run flake8 --ignore=E501,F401,E128,E402,E731,F821 {{cookiecutter.project_name}}

test: lint clean-pyc
	poetry run pytest -s --cov={{cookiecutter.project_name}}/ --cov=tests --cov-report=term-missing ${@-} --cov-report html

coverage: lint clean-pyc
	poetry run pytest --cov={{cookiecutter.project_name}} tests --cov-config .coveragerc --verbose --cov-report term --cov-report xml

publish:
	poetry build
	poetry publish
	rm -rf build dist .egg {{cookiecutter.project_name}}.egg-info

docker-build:
	docker build -f ./Dockerfile -t {{cookiecutter.project_name}} ./

docker-run: docker-build
	docker run -d false -n {{cookiecutter.project_name}} --publish $(HOST):8080 {{cookiecutter.project_name}}

docker-shell: docker-build
	docker run -it -n {{cookiecutter.project_name}} --publish=$(HOST):8080 {{cookiecutter.project_name}} /bin/sh
