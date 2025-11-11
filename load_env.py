"""Load .env file into os.environ before app initialization."""
import os
from pathlib import Path

def load_env():
    """Read .env file and set environment variables."""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()

if __name__ == "__main__":
    load_env()
    print(f"OPENAI_API_KEY present: {bool(os.environ.get('OPENAI_API_KEY'))}")
    print(f"PINECONE_API_KEY present: {bool(os.environ.get('PINECONE_API_KEY'))}")
