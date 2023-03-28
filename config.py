import os

from dotenv import load_dotenv

DOTENV_PATH = ".env"

# Enviornment variables
load_dotenv(dotenv_path=DOTENV_PATH)

ENV = os.environ

OPENAI_API_KEY = ENV["OPENAI_API_KEY"]
SLACK_BOT_TOKEN = ENV["SLACK_BOT_TOKEN"]
