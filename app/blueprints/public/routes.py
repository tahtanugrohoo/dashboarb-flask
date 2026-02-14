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
        respondent = Respondent(consent=form.consent.data)
        db.session.add(respondent)
        db.session.flush()

        # 2) simpan input kuesioner (sebagai request prediksi)
        answers = {
            "consent": form.consent.data,
            "q1_when": form.q1_when.data,
            "q2_use": form.q2_use.data,
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

        except FileNotFoundError as e:
            db.session.commit()
            flash(f"Model artifact belum tersedia: {e}", "danger")
            return redirect(url_for("public.predict"))

    return render_template("public/predict.html", form=form)

@public_bp.get("/predict/result/<string:result_id>")
def predict_result(result_id):
    result = PredictionResult.query.get(result_id)
    if not result:
        abort(404)
    req = QuestionnaireResponse.query.get(result.response_id)
    return render_template("public/predict_result.html", result=result, req=req)
