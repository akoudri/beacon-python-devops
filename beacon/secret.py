import os
import re

ENV_TOKEN = "BEACON_TOKEN"

_BEARER_RE = re.compile(r"(Bearer\s+)\S+", re.IGNORECASE)

class MissingSecretError(RuntimeError):
    """Un secret requis est absent de l'environnement"""


def require_token(env : str = ENV_TOKEN) -> str :
    try:
        return os.environ[env]
    except KeyError as e:
        raise MissingSecretError(f"Variable d'environnement {env} absente")
    

def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def redact(message : str) -> str:
    return _BEARER_RE.sub(r"\1*****", message)

