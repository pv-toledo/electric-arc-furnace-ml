from pathlib import Path
from typing import Dict, Optional
import yaml
import pandas as pd


def load_datasets_from_yaml(
    yaml_path: str | Path,
    nrows: Optional[int] = None,
) -> Dict[str, pd.DataFrame]:
    
    yaml_path = Path(yaml_path)
    if not yaml_path.exists():
        raise FileNotFoundError(f"Yaml file not found: {yaml_path}")

    with open(yaml_path, "r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f) or {}

    datasets: Dict[str, pd.DataFrame] = {}

    for name, meta in manifest.items():
        path = meta.get("path")

        if path is None:
            datasets[name] = pd.DataFrame()
            continue

        path = Path(path).expanduser()
        if not path.exists():
            msg = f"File for YAML entry '{name}' not found: {path}"
            
            print(f"[WARN] {msg}")
            datasets[name] = pd.DataFrame()
            continue

        try:
            df = pd.read_csv(path,nrows=nrows, dtype="string", low_memory=False, memory_map=True)
        except Exception as e:
            raise RuntimeError(f"Failed to read '{name}' from {path}: {e}") from e
        
        datasets[name] = df

    return datasets
