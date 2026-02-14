from flask import render_template
from flask_login import login_required
from . import analytics_bp

@analytics_bp.get("/segments")
@login_required
def segments():
    # DATA STATIK / DUMMY (sementara)
    segments = [
        {"label": "Dasar", "desc": "Pemanfaatan AI cenderung untuk kebutuhan dasar, intensitas relatif rendah-sedang."},
        {"label": "Efisien", "desc": "Pemanfaatan AI untuk efisiensi pengerjaan tugas dan belajar, dengan pola penggunaan terarah."},
        {"label": "Kritis & Bertanggung Jawab", "desc": "Pemanfaatan AI disertai verifikasi, pertimbangan etika, dan kontrol kualitas."},
    ]

    # contoh ringkasan dummy yang bisa ditampilkan sebagai chart
    dist = {"Dasar": 40, "Efisien": 35, "Kritis & Bertanggung Jawab": 25}

    return render_template("analytics/segments.html", segments=segments, dist=dist)

@analytics_bp.get("/model-eval")
@login_required
def model_eval():
    # DATA STATIK / DUMMY (sementara)
    metrics = {"accuracy": 0.78, "macro_f1": 0.74}
    labels = ["Dasar", "Efisien", "Kritis & Bertanggung Jawab"]

    # confusion matrix dummy (3x3)
    cm = [
        [52, 8, 5],
        [10, 44, 6],
        [6, 7, 42],
    ]

    return render_template("analytics/model_eval.html", metrics=metrics, labels=labels, cm=cm)
