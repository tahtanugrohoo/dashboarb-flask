from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, RadioField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, ValidationError

LIKERT_CHOICES = [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")]

SEMESTER_CHOICES = [
    ("1","1"),("2","2"),("3","3"),("4","4"),("5","5"),("6","6"),("7","7"),("8","8"),(">8",">8")
]

YESNO_CHOICES = [("yes","Ya"), ("no","Tidak")]

WHEN_CHOICES = [
    ("task", "Saat ada tugas/PR/proyek"),
    ("study", "Saat belajar memahami materi (di luar tugas)"),
    ("exam", "Saat persiapan ujian/kuis"),
    ("present", "Saat membuat presentasi / Q&A"),
    ("never", "Hampir tidak pernah"),
    ("other", "Lainnya"),
]

USE_CHOICES = [
    ("idea", "Membuat ide/topik/outline"),
    ("write", "Menulis/parafrase"),
    ("summ", "Merangkum materi"),
    ("solve", "Menjawab latihan/soal"),
    ("code", "Coding/pemrograman"),
    ("data", "Analisis data/statistik"),
    ("slide", "Membuat slide/presentasi"),
    ("trans", "Terjemahan"),
    ("other", "Lainnya"),
]

PORTION_CHOICES = [
    ("very_small", "Sangat kecil (sekadar tanya 1–2 hal)"),
    ("small", "Kecil (membantu sebagian kecil)"),
    ("medium", "Sedang (membantu sekitar setengah)"),
    ("large", "Besar (membantu sebagian besar)"),
    ("very_large", "Sangat besar (hampir seluruhnya)"),
]

FREQ_CHOICES = [
    ("daily", "Hampir setiap hari"),
    ("weekly", "Beberapa kali seminggu"),
    ("monthly", "Beberapa kali sebulan"),
    ("rare", "Jarang"),
    ("never", "Hampir tidak pernah"),
]

class QuestionnaireForm(FlaskForm):
    consent = BooleanField("Saya bersedia berpartisipasi secara sukarela", validators=[DataRequired()])

    # Profil (tanpa A1/A2 dst)
    a1_name = StringField("Nama (opsional)", validators=[Optional(), Length(max=150)])
    a2_univ = StringField("Universitas", validators=[DataRequired(), Length(max=150)])
    a3_major = StringField("Jurusan/Program Studi", validators=[DataRequired(), Length(max=150)])
    a4_semester = RadioField("Semester", choices=SEMESTER_CHOICES, validators=[DataRequired()])
    a5_used_ai = RadioField("Pernah menggunakan AI generatif untuk kegiatan akademik?", choices=YESNO_CHOICES, validators=[DataRequired()])

    # Pola umum (tanpa B1/B2 dst)
    b1a_when_multi = SelectMultipleField("Kapan Anda menggunakan AI generatif? (boleh pilih lebih dari satu)", choices=WHEN_CHOICES, validators=[DataRequired()])
    b1a_other_text = StringField("Lainnya (isi jika memilih Lainnya)", validators=[Optional(), Length(max=200)])

    b1b_when_single = RadioField("Dari pilihan di atas, mana yang paling sering? (pilih satu)", choices=WHEN_CHOICES, validators=[DataRequired()])
    b1b_other_text = StringField("Lainnya (isi jika memilih Lainnya)", validators=[Optional(), Length(max=200)])

    b2a_what_multi = SelectMultipleField("AI digunakan untuk apa saja? (boleh pilih lebih dari satu)", choices=USE_CHOICES, validators=[DataRequired()])
    b2a_other_text = StringField("Lainnya (isi jika memilih Lainnya)", validators=[Optional(), Length(max=200)])

    b2b_what_single = RadioField("Dari pilihan di atas, mana yang paling sering? (pilih satu)", choices=USE_CHOICES, validators=[DataRequired()])
    b2b_other_text = StringField("Lainnya (isi jika memilih Lainnya)", validators=[Optional(), Length(max=200)])

    b3_portion = RadioField("Seberapa besar porsi AI dalam pengerjaan tugas saat Anda menggunakannya?", choices=PORTION_CHOICES, validators=[DataRequired()])
    b4_freq = RadioField("Seberapa sering menggunakan AI untuk akademik?", choices=FREQ_CHOICES, validators=[DataRequired()])

    # Pernyataan (Likert) — label tanpa C1/C2 di depan
    # Tujuan & Perencanaan
    c11 = RadioField("Saya menggunakan AI dengan tujuan yang jelas.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c12 = RadioField("Saya biasanya menuliskan konteks yang cukup saat bertanya ke AI.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c13 = RadioField("Saya memilih AI sebagai bantuan yang sesuai kebutuhan, bukan untuk semua hal.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c14 = RadioField("Saya menggunakan AI untuk membantu menyusun langkah belajar.", choices=LIKERT_CHOICES, validators=[DataRequired()])

    # Iterasi & Modifikasi
    c21 = RadioField("Saya sering melakukan beberapa iterasi sampai hasil sesuai.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c22 = RadioField("Saya mengubah/menyusun ulang output AI dengan kata-kata saya sendiri.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c23 = RadioField("Saya meminta AI memberi contoh/penjelasan alternatif jika kurang jelas.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c24 = RadioField("Saya menggunakan AI untuk mengecek struktur/kerapihan jawaban.", choices=LIKERT_CHOICES, validators=[DataRequired()])

    # Verifikasi & Evaluasi
    c31 = RadioField("Saya mengecek kembali jawaban AI menggunakan sumber lain.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c32 = RadioField("Saya menilai apakah jawaban AI masuk akal sebelum digunakan.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c33 = RadioField("Saya memeriksa istilah/rumus/kode dari AI sebelum dipakai.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c34 = RadioField("Jika informasi meragukan, saya mencari pembanding dulu.", choices=LIKERT_CHOICES, validators=[DataRequired()])

    # Orientasi Pemahaman
    c41 = RadioField("AI membantu saya memahami konsep, bukan hanya menghasilkan jawaban.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c42 = RadioField("Setelah memakai AI, saya masih berusaha menjelaskan ulang.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c43 = RadioField("Saya menggunakan AI untuk latihan, bukan hanya hasil akhir.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c44 = RadioField("Saya merasa AI membantu meningkatkan efisiensi belajar.", choices=LIKERT_CHOICES, validators=[DataRequired()])

    # Etika & Kemandirian
    c51 = RadioField("Saya menghindari menyalin output AI secara utuh tanpa revisi.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c52 = RadioField("Saya mempertimbangkan aturan dosen/kelas terkait penggunaan AI.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c53 = RadioField("Saya berusaha tetap mandiri sebelum meminta bantuan AI.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c54 = RadioField("Saya memilih AI sebagai alat bantu, bukan penentu utama.", choices=LIKERT_CHOICES, validators=[DataRequired()])

    # Situasi (opsional)
    d1 = RadioField("Saat waktu terbatas, saya cenderung memilih AI sebagai bantuan utama.", choices=LIKERT_CHOICES, validators=[Optional()])
    d2 = RadioField("Kadang saya memakai jawaban AI jika sudah terasa cukup tanpa mengecek terlalu jauh.", choices=LIKERT_CHOICES, validators=[Optional()])
    d3 = RadioField("Saya menggunakan AI lebih banyak untuk tugas tertentu dibanding yang lain.", choices=LIKERT_CHOICES, validators=[Optional()])

    submit = SubmitField("Kirim")

    def validate_b1a_when_multi(self, field):
        if "never" in field.data and len(field.data) > 1:
            raise ValidationError('Pilihan "Hampir tidak pernah" harus berdiri sendiri.')

        if "other" in field.data and not (self.b1a_other_text.data or "").strip():
            raise ValidationError('Anda memilih "Lainnya", mohon isi kolom Lainnya.')

    def validate_b1b_when_single(self, field):
        if field.data == "other" and not (self.b1b_other_text.data or "").strip():
            raise ValidationError('Anda memilih "Lainnya", mohon isi kolom Lainnya.')

    def validate_b2a_what_multi(self, field):
        if "other" in field.data and not (self.b2a_other_text.data or "").strip():
            raise ValidationError('Anda memilih "Lainnya", mohon isi kolom Lainnya.')

    def validate_b2b_what_single(self, field):
        if field.data == "other" and not (self.b2b_other_text.data or "").strip():
            raise ValidationError('Anda memilih "Lainnya", mohon isi kolom Lainnya.')
