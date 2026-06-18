from beacon.config import Target, load_config
from pathlib import Path
from beacon.probe import ProbeResult, probe_all

if __name__ == '__main__':
    path = Path("config/targets.yaml")
    targets = load_config(path)
    for p in probe_all(targets=targets):
        print(f"{p.target} has status {p.status}")

