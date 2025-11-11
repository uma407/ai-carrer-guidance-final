import json
import os
from pathlib import Path
from typing import Dict, List

STORE_DIR = Path(__file__).parent / 'data'
STORE_FILE = STORE_DIR / 'saved_resources.json'


def _ensure_store():
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    if not STORE_FILE.exists():
        with STORE_FILE.open('w', encoding='utf-8') as f:
            json.dump([], f)


def save_resource(resource: Dict) -> Dict:
    """Append a resource dict to the persistent saved-resources JSON.

    Returns the saved record (with an assigned id and timestamp).
    """
    _ensure_store()
    with STORE_FILE.open('r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception:
            data = []

    # Basic normalization
    resource = dict(resource)
    import time
    resource.setdefault('id', int(time.time() * 1000))
    resource.setdefault('saved_at', time.ctime())

    data.append(resource)

    # atomic write
    tmp = STORE_FILE.with_suffix('.tmp')
    with tmp.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp.replace(STORE_FILE)
    return resource


def list_resources() -> List[Dict]:
    _ensure_store()
    with STORE_FILE.open('r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            return []


if __name__ == '__main__':
    # Quick manual test
    print('Saved resources path:', STORE_FILE)
    print('Current resources:', list_resources())
