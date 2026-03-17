import logging
import os
from dotenv import load_dotenv

ENV = os.getenv("ENV", "local")

env_file = ".env" if ENV == "local" else f".env.{ENV}"
load_dotenv(env_file)

BASE_URL = os.getenv("BASE_URL")
UI_USERNAME = os.getenv("UI_USERNAME")
UI_PASSWORD = os.getenv("UI_PASSWORD")

BROWSER = os.getenv("BROWSER", "chromium")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
TIMEOUT_MS = int(os.getenv("TIMEOUT_MS", "10000"))
API_BASE_URL = os.getenv("API_BASE_URL")

# Fail fast for required config
required_vars = {
    "BASE_URL": BASE_URL,
    "UI_USERNAME": UI_USERNAME,
    "UI_PASSWORD": UI_PASSWORD,
    "API_BASE_URL": API_BASE_URL
}

for key, value in required_vars.items():
    if not value:
        raise ValueError(f"{key} is not set in environment configuration")
