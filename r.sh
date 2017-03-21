#!/bin/bash

set -xe

if ! [ -v VIRTUAL_ENV ]; then
   echo Activating virtualenv
   source .env/bin/activate
fi

source environment.sh
python sync.py