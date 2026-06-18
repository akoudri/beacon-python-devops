from beacon.config import Target, load_config
from pathlib import Path

if __name__ == '__main__':
    path = Path("config/targets.yaml")
    targets = load_config(path)
    for t in targets:
        print(f"{t.name} -> {t.host}:{t.port}")

