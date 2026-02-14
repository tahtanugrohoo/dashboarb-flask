import csv
import sys
from app import create_app
from app.extensions import db
from app.models.clustering import ClusteringResult

def main(csv_path: str, model_version: str = "kmeans_v1"):
    app = create_app()
    with app.app_context():
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            n = 0
            for row in reader:
                obj = ClusteringResult(
                    response_id=row["response_id"].strip(),
                    model_version=model_version,
                    cluster_id=int(row["cluster_id"]),
                    segment_label=row["segment_label"].strip(),
                )
                db.session.add(obj)
                n += 1
            db.session.commit()
        print(f"Imported {n} clustering rows into clustering_results")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/import_kmeans_results.py path/to/results.csv [model_version]")
        sys.exit(1)
    csv_path = sys.argv[1]
    model_version = sys.argv[2] if len(sys.argv) >= 3 else "kmeans_v1"
    main(csv_path, model_version)
