#!/bin/bash

echo "Setting up the development environment..."

export FLASK_APP=app.py
export FLASK_ENV=development
export DATABASE_URL="postgresql://username:password@localhost/aiblockchain_dev_db"
export WEB3_PROVIDER_URL="http://testnet-rpc.evire.io:8545"
export SECRET_KEY="your_secret_key"

echo "Development environment set up successfully."
