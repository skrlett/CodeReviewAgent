import os
import dotenv

dotenv.load_dotenv()

GITHUB_BASE_URL = "https://api.github.com"

GITHUB_USER_AGENT = "@CodeAgent"

GITHUB_ACCEPT_JSON_HEADER = "application/vnd.github.v3+json"

GITHUB_ACCEPT_DIFF_HEADER = "application/vnd.github.diff"

GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
