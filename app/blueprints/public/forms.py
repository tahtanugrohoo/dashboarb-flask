from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired

class QuestionnaireForm(FlaskForm):
    consent = BooleanField("Saya bersedia berpartisipasi", validators=[DataRequired()])

    q1_when = SelectField(
        "Kapan biasanya kamu menggunakan AI generatif?",
        choices=[
            ("task", "Saat ada tugas/PR/proyek"),
            ("study", "Saat belajar memahami materi (di luar tugas)"),
            ("exam", "Saat persiapan ujian/kuis"),
            ("present", "Saat membuat presentasi / Q&A"),
            ("never", "Hampir tidak pernah"),
            ("other", "Lainnya"),
        ],
        validators=[DataRequired()],
    )

    q2_use = SelectField(
        "Untuk kebutuhan perkuliahan, AI paling sering kamu gunakan untuk apa?",
        choices=[
            ("idea", "Membuat ide/topik/outline"),
            ("write", "Menulis/parafrase"),
            ("summ", "Merangkum materi"),
            ("solve", "Menjawab latihan/soal"),
            ("code", "Coding/pemrograman"),
            ("data", "Analisis data/statistik"),
            ("slide", "Membuat slide/presentasi"),
            ("trans", "Terjemahan"),
            ("other", "Lainnya"),
        ],
        validators=[DataRequired()],
    )

    submit = SubmitField("Kirim")
