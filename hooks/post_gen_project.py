#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Post gen hook to ensure that the generated project
has only one package management, either pipenv or pip."""
import logging
import os
import shutil
import sys

LOGGER = logging.getLogger()


def clean_extra_package_management_files():
    """Removes either requirements files and folder or the Pipfile."""
    use_pipenv = "{{cookiecutter.use_pipenv}}"
    use_heroku = "{{cookiecutter.use_heroku}}"
    to_delete = []

    if use_pipenv == "yes":
        to_delete = to_delete + ["requirements.txt", "requirements"]
    else:
        to_delete.append("Pipfile")

    if use_heroku == "no":
        to_delete = to_delete + ["Procfile", "app.json"]

    try:
        for file_or_dir in to_delete:
            if os.path.isfile(file_or_dir):
                os.remove(file_or_dir)
            else:
                shutil.rmtree(file_or_dir)
        shutil.copy(".env.example", ".env")
    except OSError as e:
        LOGGER.warning("While attempting to remove file(s) an error occurred")
        LOGGER.warning(f"Error: {e}")
        sys.exit(1)


import os

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == '__main__':

    if '{{ cookiecutter.create_author_file }}' != 'y':
        remove_file('AUTHORS.rst')
        remove_file('docs/authors.rst')

    if 'no' in '{{ cookiecutter.command_line_interface|lower }}':
        cli_file = os.path.join('{{ cookiecutter.project_slug }}', 'cli.py')
        remove_file(cli_file)

    if 'Not open source' == '{{ cookiecutter.open_source_license }}':
        remove_file('LICENSE')


if __name__ == "__main__":
    clean_extra_package_management_files()