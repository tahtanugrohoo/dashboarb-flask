from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from sqlalchemy import func
from collections import Counter

from . import admin_bp
from .forms import LoginForm
from ...extensions import db
from ...models.admin_user import AdminUser
from ...models.response import QuestionnaireResponse

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    # Jika sudah login, langsung ke dashboard
    # (tanpa current_user import pun aman; kita cek sederhana via session login_user)
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
    total_responses = QuestionnaireResponse.query.count()

    total_respondents = (
        QuestionnaireResponse.query.with_entities(QuestionnaireResponse.respondent_id)
        .distinct()
        .count()
    )

    # 1) Tren respons per tanggal
    rows = (
        QuestionnaireResponse.query
        .with_entities(
            func.date(QuestionnaireResponse.submitted_at).label("d"),
            func.count().label("cnt")
        )
        .group_by("d")
        .order_by("d")
        .all()
    )
    chart_labels = [str(r.d) for r in rows]
    chart_values = [int(r.cnt) for r in rows]

    # 2) Distribusi jawaban Q1 & Q2 (dari answers_json)
    all_resp = QuestionnaireResponse.query.all()

    q1_counter = Counter()
    q2_counter = Counter()

    for r in all_resp:
        a = r.answers_json or {}
        q1 = a.get("q1_when")
        q2 = a.get("q2_use")
        if q1:
            q1_counter[q1] += 1
        if q2:
            q2_counter[q2] += 1

    # urutkan biar grafik rapi (descending)
    q1_items = q1_counter.most_common()
    q2_items = q2_counter.most_common()

    q1_labels = [k for k, _ in q1_items]
    q1_values = [v for _, v in q1_items]
    q2_labels = [k for k, _ in q2_items]
    q2_values = [v for _, v in q2_items]

    return render_template(
        "admin/dashboard.html",
        total_responses=total_responses,
        total_respondents=total_respondents,
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
    # pagination
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    # optional filter tanggal (YYYY-MM-DD)
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