from flask import render_template, redirect, url_for, flash
from . import public_bp
from .forms import QuestionnaireForm
from ...extensions import db
from ...models.respondent import Respondent
from ...models.response import QuestionnaireResponse

@public_bp.get("/")
def index():
    return redirect(url_for("public.questionnaire"))

@public_bp.route("/questionnaire", methods=["GET", "POST"])
def questionnaire():
    form = QuestionnaireForm()
    if form.validate_on_submit():
        # 1) simpan responden anonim
        respondent = Respondent(
            consent=form.consent.data,
            university=None,
            major=None,
            education_level=None,
            batch_year=None,
        )
        db.session.add(respondent)
        db.session.flush()  # dapat respondent.id tanpa commit dulu

        # 2) simpan jawaban
        answers = {
            "consent": form.consent.data,
            "q1_when": form.q1_when.data,
            "q2_use": form.q2_use.data,
        }
        resp = QuestionnaireResponse(
            respondent_id=respondent.id,
            answers_json=answers,
            data_version="v1",
        )
        db.session.add(resp)

        db.session.commit()
        flash("Terima kasih! Respons kamu sudah tersimpan.", "success")
        return redirect(url_for("public.thank_you"))

    return render_template("public/questionnaire.html", form=form)

@public_bp.get("/thank-you")
def thank_you():
    return render_template("public/thankyou.html")
