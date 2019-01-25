#!/bin/bash -e

if [[ -z "$PYPI_USERNAME" || -z "$PYPI_PASSWORD" ]]; then
    echo "You must set PYPI_USERNAME and PYPI_PASSWORD to run this script"
    exit 1
fi

# Create distribution
python setup.py sdist bdist_wheel

twine upload --repository-url https://test.pypi.org/legacy/ -u ${PYPI_USERNAME} -p ${PYPI_PASSWORD} dist/*

# Upload to PyPi
twine upload -u ${PYPI_USERNAME} -p ${PYPI_PASSWORD} dist/*
