from flask import render_template, redirect, url_for, flash, abort
from . import public_bp
from .forms import QuestionnaireForm

from ...extensions import db
from ...models.respondent import Respondent
from ...models.response import QuestionnaireResponse
from ...models.prediction import PredictionResult
from ...ml_utils import load_artifact

SEGMENT_LABELS = ["Dasar", "Efisien", "Kritis & Bertanggung Jawab"]

@public_bp.get("/")
def index():
    return redirect(url_for("public.predict"))

@public_bp.route("/predict", methods=["GET", "POST"])
def predict():
    form = QuestionnaireForm()
    if form.validate_on_submit():
        # 1) simpan responden anonim (optional)
        respondent = Respondent(
            consent=form.consent.data,
            name_optional=form.a1_name.data or None,
            university=form.a2_univ.data,
            major=form.a3_major.data,
            semester=form.a4_semester.data,
            used_ai=(form.a5_used_ai.data == "yes"),
        )
        db.session.add(respondent)
        db.session.flush()

        # 2) simpan input kuesioner (sebagai request prediksi)
        answers = {
            # consent + profil
            "consent": form.consent.data,
            "a1_name": form.a1_name.data,
            "a2_univ": form.a2_univ.data,
            "a3_major": form.a3_major.data,
            "a4_semester": form.a4_semester.data,
            "a5_used_ai": form.a5_used_ai.data,

            # B
            "b1a_when_multi": form.b1a_when_multi.data,
            "b1a_other_text": form.b1a_other_text.data,
            "b1b_when_single": form.b1b_when_single.data,
            "b1b_other_text": form.b1b_other_text.data,

            "b2a_what_multi": form.b2a_what_multi.data,
            "b2a_other_text": form.b2a_other_text.data,
            "b2b_what_single": form.b2b_what_single.data,
            "b2b_other_text": form.b2b_other_text.data,

            "b3_portion": form.b3_portion.data,
            "b4_freq": form.b4_freq.data,

            # C (Likert)
            "c11": form.c11.data, "c12": form.c12.data, "c13": form.c13.data, "c14": form.c14.data,
            "c21": form.c21.data, "c22": form.c22.data, "c23": form.c23.data, "c24": form.c24.data,
            "c31": form.c31.data, "c32": form.c32.data, "c33": form.c33.data, "c34": form.c34.data,
            "c41": form.c41.data, "c42": form.c42.data, "c43": form.c43.data, "c44": form.c44.data,
            "c51": form.c51.data, "c52": form.c52.data, "c53": form.c53.data, "c54": form.c54.data,

            # D (opsional)
            "d1": form.d1.data, "d2": form.d2.data, "d3": form.d3.data,
        }

        req = QuestionnaireResponse(
            respondent_id=respondent.id,
            answers_json=answers,
            data_version="v1",
        )
        db.session.add(req)
        db.session.flush()

        # 3) mapping sederhana -> fitur numerik (sementara)
        # Nanti saat kamu sudah punya mapping final dari dataset offline, samakan di sini.
        # Contoh minimal: one-hot sederhana memakai index kategori.
        q1_map = {"task":0, "study":1, "exam":2, "present":3, "never":4, "other":5}
        q2_map = {"idea":0, "write":1, "summ":2, "solve":3, "code":4, "data":5, "slide":6, "trans":7, "other":8}
        x = [[q1_map.get(form.q1_when.data, 0), q2_map.get(form.q2_use.data, 0)]]

        # 4) inference RF (tanpa training)
        try:
            rf = load_artifact("rf.joblib")
            # scaler optional
            try:
                scaler = load_artifact("scaler.joblib")
                x_in = scaler.transform(x)
            except FileNotFoundError:
                x_in = x

            pred = rf.predict(x_in)[0]

            # pred bisa berupa label string langsung atau integer
            if isinstance(pred, int):
                pred_label = SEGMENT_LABELS[pred]
            else:
                pred_label = str(pred)

            proba = None
            if hasattr(rf, "predict_proba"):
                p = rf.predict_proba(x_in)[0].tolist()
                proba = {SEGMENT_LABELS[i]: float(p[i]) for i in range(min(len(p), len(SEGMENT_LABELS)))}

            result = PredictionResult(
                response_id=req.id,
                model_version="rf_v1",
                predicted_label=pred_label,
                proba_json=proba
            )
            db.session.add(result)
            db.session.commit()

            return redirect(url_for("public.predict_result", result_id=result.id))

        except FileNotFoundError:
            # MODE STUB: model belum tersedia, pakai hasil dummy agar UI bisa didemo
            pred_label = "Efisien"  # dummy
            result = PredictionResult(
                response_id=req.id,
                model_version="stub",
                predicted_label=pred_label,
                proba_json={"Dasar": 0.2, "Efisien": 0.6, "Kritis & Bertanggung Jawab": 0.2},
            )
            db.session.add(result)
            db.session.commit()

            flash("Model belum tersedia. Sistem menampilkan hasil prediksi dummy untuk demo UI.", "success")
            return redirect(url_for("public.predict_result", result_id=result.id))


    return render_template("public/predict.html", form=form)

@public_bp.get("/predict/result/<string:result_id>")
def predict_result(result_id):
    result = PredictionResult.query.get(result_id)
    if not result:
        abort(404)
    req = QuestionnaireResponse.query.get(result.response_id)
    return render_template("public/predict_result.html", result=result, req=req)
