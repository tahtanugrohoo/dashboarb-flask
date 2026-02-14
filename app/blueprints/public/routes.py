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
        name_optional=form.name_optional.data or None,
        university=form.university.data,
        major=form.major.data,
        semester=form.semester.data,
        used_ai=(form.used_ai.data == "yes"),
        )
        db.session.add(respondent)
        db.session.flush()

        # 2) simpan input kuesioner (sebagai request prediksi)
        answers = {
  "consent": form.consent.data,

  "name_optional": form.name_optional.data,
  "university": form.university.data,
  "major": form.major.data,
  "semester": form.semester.data,
  "used_ai": form.used_ai.data,

  "when_multi": form.when_multi.data,
  "when_other_text": form.when_other_text.data,
  "when_single": form.when_single.data,
  "when_single_other_text": form.when_single_other_text.data,

  "use_multi": form.use_multi.data,
  "use_other_text": form.use_other_text.data,
  "use_single": form.use_single.data,
  "use_single_other_text": form.use_single_other_text.data,

  "portion": form.portion.data,
  "freq": form.freq.data,

  "p1": form.p1.data, "p2": form.p2.data, "p3": form.p3.data, "p4": form.p4.data,
  "i1": form.i1.data, "i2": form.i2.data, "i3": form.i3.data, "i4": form.i4.data,
  "v1": form.v1.data, "v2": form.v2.data, "v3": form.v3.data, "v4": form.v4.data,
  "u1": form.u1.data, "u2": form.u2.data, "u3": form.u3.data, "u4": form.u4.data,
  "e1": form.e1.data, "e2": form.e2.data, "e3": form.e3.data, "e4": form.e4.data,

  "s1": form.s1.data, "s2": form.s2.data, "s3": form.s3.data,
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
