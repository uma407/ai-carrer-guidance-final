import os
import importlib

# Check environment variable presence (do NOT print the key)
has_key = bool(os.environ.get('OPENAI_API_KEY'))

# Check that the installed openai package can be imported
openai_importable = False
try:
    import openai  # noqa: F401
    openai_importable = True
except Exception:
    openai_importable = False

# Check our wrapper
wrapper_ok = False
try:
    oc = importlib.import_module('openai_client')
    wrapper_ok = True
    wrapper_has_key = bool(getattr(oc.OpenAIClient(), 'api_key', None))
except Exception:
    wrapper_ok = False
    wrapper_has_key = False

print('HAS_ENV_KEY' if has_key else 'NO_ENV_KEY')
print('OPENAI_IMPORTABLE' if openai_importable else 'OPENAI_NOT_IMPORTABLE')
print('WRAPPER_OK' if wrapper_ok else 'WRAPPER_FAIL')
print('WRAPPER_HAS_KEY' if wrapper_has_key else 'WRAPPER_NO_KEY')
