from google import genai
import os
from openai import OpenAI


def load_dotenv_from_file(path: str = ".env") -> bool:
    """Minimal .env loader that sets environment variables from a file.

    - Ignores blank lines and comments starting with '#'.
    - Supports lines like `KEY=VALUE` and `export KEY=VALUE`.
    - Strips surrounding single or double quotes from values.
    - Does not overwrite existing environment variables (uses setdefault).

    Returns True if the file was found and read, False if the file does not exist.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip()
                # support `export KEY=VALUE`
                if key.lower().startswith("export "):
                    key = key[7:].strip()
                # strip surrounding quotes if present
                if (val.startswith('"') and val.endswith('"')) or (
                    val.startswith("'") and val.endswith("'")
                ):
                    val = val[1:-1]
                # don't overwrite existing environment variables
                os.environ.setdefault(key, val)
        return True
    except FileNotFoundError:
        return False


# Load .env from project root (looks for a file named `.env`)
load_dotenv_from_file()

# Read and validate the API key from environment (populated from .env)
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not set in environment or .env file")

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
# genai.Client reads it from the environment, so we can call it as before.
#client = genai.Client()
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta"
)

# response = client.models.generate_content(
#     model="gemini-2.5-flash", contents="Explain how AI works in a few words"
# )
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "user", "content": "Explain how AI works in a few words"}
    ]
)
print(response.choices[0].message.content)