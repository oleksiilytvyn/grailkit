#!/bin/bash -e

if [[ "$PYPI_USERNAME" || -z "$PYPI_PASSWORD" ]]; then
    echo "You must set PYPI_USERNAME and PYPI_PASSWORD to run this script"
    exit 1
fi

cat << EOF > /root/.pypirc
[distutils]
index-servers =
  pypi

[pypi]
repository=https://upload.pypi.org/legacy/
username=${PYPI_USERNAME}
password=${PYPI_PASSWORD}
EOF

python setup.py sdist upload -r pypi
