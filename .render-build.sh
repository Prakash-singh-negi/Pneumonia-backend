#!/usr/bin/env bash

# Force Python 3.10
echo "Forcing Python 3.10 for TensorFlow compatibility"
pyenv install 3.10.12
pyenv global 3.10.12

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
