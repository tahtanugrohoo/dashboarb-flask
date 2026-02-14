import json
from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"

ARTIFACT_DIR = INSTANCE_DIR / "artifacts"
METRICS_PATH = INSTANCE_DIR / "metrics.json"

def load_artifact(name: str):
    path = ARTIFACT_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Artifact not found: {path}")
    return joblib.load(path)

def load_metrics() -> dict:
    if not METRICS_PATH.exists():
        # fallback kosong agar halaman tidak crash
        return {
            "model_version": "-",
            "accuracy": None,
            "macro_f1": None,
            "labels": ["Dasar", "Efisien", "Kritis & Bertanggung Jawab"],
            "confusion_matrix": [[0, 0, 0],[0, 0, 0],[0, 0, 0]],
        }
    return json.loads(METRICS_PATH.read_text(encoding="utf-8"))
