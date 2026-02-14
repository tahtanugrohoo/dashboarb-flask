from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required
from sqlalchemy import func
from collections import Counter

from . import admin_bp
from .forms import LoginForm

from ...models.admin_user import AdminUser
from ...models.response import QuestionnaireResponse
from ...models.clustering import ClusteringResult
from ...models.prediction import PredictionResult

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_url = request.args.get("next")
            return redirect(next_url or url_for("admin.dashboard"))
        flash("Login gagal. Periksa username/password.", "danger")
    return render_template("admin/login.html", form=form)

@admin_bp.post("/logout")
@login_required
def logout():
    logout_user()
    flash("Anda sudah logout.", "success")
    return redirect(url_for("admin.login"))

@admin_bp.get("/dashboard")
@login_required
def dashboard():
    total_requests = QuestionnaireResponse.query.count()
    total_predictions = PredictionResult.query.count()
    total_clustered = ClusteringResult.query.count()

    # tren request prediksi per tanggal
    rows = (
        QuestionnaireResponse.query
        .with_entities(func.date(QuestionnaireResponse.submitted_at).label("d"), func.count().label("cnt"))
        .group_by("d")
        .order_by("d")
        .all()
    )
    chart_labels = [str(r.d) for r in rows]
    chart_values = [int(r.cnt) for r in rows]

    # distribusi jawaban Q1/Q2 dari request prediksi
    all_resp = QuestionnaireResponse.query.all()
    q1_counter = Counter()
    q2_counter = Counter()
    for r in all_resp:
        a = r.answers_json or {}
        if a.get("q1_when"): q1_counter[a["q1_when"]] += 1
        if a.get("q2_use"): q2_counter[a["q2_use"]] += 1

    q1_items = q1_counter.most_common()
    q2_items = q2_counter.most_common()

    q1_labels = [k for k, _ in q1_items]
    q1_values = [v for _, v in q1_items]
    q2_labels = [k for k, _ in q2_items]
    q2_values = [v for _, v in q2_items]

    return render_template(
        "admin/dashboard.html",
        total_requests=total_requests,
        total_predictions=total_predictions,
        total_clustered=total_clustered,
        chart_labels=chart_labels,
        chart_values=chart_values,
        q1_labels=q1_labels,
        q1_values=q1_values,
        q2_labels=q2_labels,
        q2_values=q2_values,
    )

@admin_bp.get("/responses")
@login_required
def responses_list():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    date_from = request.args.get("from")
    date_to = request.args.get("to")

    q = QuestionnaireResponse.query.order_by(QuestionnaireResponse.submitted_at.desc())
    if date_from:
        q = q.filter(func.date(QuestionnaireResponse.submitted_at) >= date_from)
    if date_to:
        q = q.filter(func.date(QuestionnaireResponse.submitted_at) <= date_to)

    pagination = q.paginate(page=page, per_page=per_page, error_out=False)
    return render_template(
        "admin/responses_list.html",
        pagination=pagination,
        items=pagination.items,
        page=page,
        per_page=per_page,
        date_from=date_from or "",
        date_to=date_to or "",
    )

@admin_bp.get("/responses/<string:response_id>")
@login_required
def response_detail(response_id):
    resp = QuestionnaireResponse.query.get(response_id)
    if not resp:
        abort(404)
    return render_template("admin/response_detail.html", resp=resp)
