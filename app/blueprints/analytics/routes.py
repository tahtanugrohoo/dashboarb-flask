from flask import render_template
from flask_login import login_required
from sqlalchemy import func

from . import analytics_bp
from ...models.clustering import ClusteringResult
from ...ml_utils import load_metrics

@analytics_bp.get("/segments")
@login_required
def segments():
    # Distribusi segmen dari hasil K-Means yang sudah disimpan (offline -> DB)
    rows = (
        ClusteringResult.query
        .with_entities(ClusteringResult.segment_label, func.count().label("cnt"))
        .group_by(ClusteringResult.segment_label)
        .order_by(func.count().desc())
        .all()
    )
    dist = {label: int(cnt) for label, cnt in rows}
    if not dist:
        dist = {"Dasar": 0, "Efisien": 0, "Kritis & Bertanggung Jawab": 0}

    segments = [
        {"label": "Dasar", "desc": "Pemanfaatan AI untuk kebutuhan dasar, intensitas relatif rendah–sedang."},
        {"label": "Efisien", "desc": "Pemanfaatan AI untuk efisiensi pengerjaan tugas dan belajar, terarah."},
        {"label": "Kritis & Bertanggung Jawab", "desc": "Pemanfaatan AI disertai verifikasi, etika, dan kontrol kualitas."},
    ]

    return render_template("analytics/segments.html", segments=segments, dist=dist)

@analytics_bp.get("/model-eval")
@login_required
def model_eval():
    m = load_metrics()
    metrics = {"accuracy": m.get("accuracy"), "macro_f1": m.get("macro_f1")}
    labels = m.get("labels") or ["Dasar", "Efisien", "Kritis & Bertanggung Jawab"]
    cm = m.get("confusion_matrix") or [[0, 0, 0],[0, 0, 0],[0, 0, 0]]
    model_version = m.get("model_version", "-")

    return render_template(
        "analytics/model_eval.html",
        metrics=metrics,
        labels=labels,
        cm=cm,
        model_version=model_version
    )
