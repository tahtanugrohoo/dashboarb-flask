from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, StringField, RadioField, SelectMultipleField, SubmitField
)
from wtforms.validators import DataRequired, Optional, Length, ValidationError

LIKERT_CHOICES = [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")]

SEMESTER_CHOICES = [
    ("1","1"),("2","2"),("3","3"),("4","4"),("5","5"),("6","6"),("7","7"),("8","8"),(">8",">8")
]

YESNO_CHOICES = [("yes","Ya"), ("no","Tidak")]

B1_CHOICES = [
    ("task", "Saat ada tugas/PR/proyek"),
    ("study", "Saat belajar memahami materi (di luar tugas)"),
    ("exam", "Saat persiapan ujian/kuis"),
    ("present", "Saat membuat presentasi / Q&A"),
    ("never", "Hampir tidak pernah"),
    ("other", "Lainnya"),
]

B2_CHOICES = [
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

B3_CHOICES = [
    ("very_small", "Sangat kecil (sekadar tanya 1–2 hal)"),
    ("small", "Kecil (membantu sebagian kecil)"),
    ("medium", "Sedang (membantu sekitar setengah)"),
    ("large", "Besar (membantu sebagian besar)"),
    ("very_large", "Sangat besar (hampir seluruhnya)"),
]

B4_CHOICES = [
    ("daily", "Hampir setiap hari"),
    ("weekly", "Beberapa kali seminggu"),
    ("monthly", "Beberapa kali sebulan"),
    ("rare", "Jarang"),
    ("never", "Hampir tidak pernah"),
]

class QuestionnaireForm(FlaskForm):
    # Consent
    consent = BooleanField("Saya bersedia berpartisipasi secara sukarela", validators=[DataRequired()])

    # A. Profil
    a1_name = StringField("A1. Nama (opsional)", validators=[Optional(), Length(max=150)])
    a2_univ = StringField("A2. Universitas", validators=[DataRequired(), Length(max=150)])
    a3_major = StringField("A3. Jurusan/Program Studi", validators=[DataRequired(), Length(max=150)])
    a4_semester = RadioField("A4. Semester", choices=SEMESTER_CHOICES, validators=[DataRequired()])
    a5_used_ai = RadioField("A5. Pernah menggunakan AI generatif untuk kegiatan akademik?", choices=YESNO_CHOICES, validators=[DataRequired()])

    # B. Pola Umum
    b1a_when_multi = SelectMultipleField("B1a. Kapan Anda menggunakan AI generatif? (boleh pilih >1)", choices=B1_CHOICES, validators=[DataRequired()])
    b1a_other_text = StringField("B1a. Lainnya (isi jika pilih Lainnya)", validators=[Optional(), Length(max=200)])

    b1b_when_single = RadioField("B1b. Dari pilihan B1a, mana yang paling sering? (pilih 1)", choices=B1_CHOICES, validators=[DataRequired()])
    b1b_other_text = StringField("B1b. Lainnya (isi jika pilih Lainnya)", validators=[Optional(), Length(max=200)])

    b2a_what_multi = SelectMultipleField("B2a. Untuk kebutuhan akademik, AI digunakan untuk apa saja? (boleh pilih >1)", choices=B2_CHOICES, validators=[DataRequired()])
    b2a_other_text = StringField("B2a. Lainnya (isi jika pilih Lainnya)", validators=[Optional(), Length(max=200)])

    b2b_what_single = RadioField("B2b. Dari pilihan B2a, mana yang paling sering? (pilih 1)", choices=B2_CHOICES, validators=[DataRequired()])
    b2b_other_text = StringField("B2b. Lainnya (isi jika pilih Lainnya)", validators=[Optional(), Length(max=200)])

    b3_portion = RadioField("B3. Seberapa besar porsi AI dalam pengerjaan tugas?", choices=B3_CHOICES, validators=[DataRequired()])
    b4_freq = RadioField("B4. Seberapa sering menggunakan AI untuk akademik?", choices=B4_CHOICES, validators=[DataRequired()])

    # C. Pernyataan (Likert 1–5)
    # C1 Tujuan & Perencanaan
    c11 = RadioField("C1.1 Saya menggunakan AI dengan tujuan yang jelas.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c12 = RadioField("C1.2 Saya biasanya menuliskan konteks yang cukup saat bertanya ke AI.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c13 = RadioField("C1.3 Saya memilih AI sebagai bantuan yang sesuai kebutuhan, bukan untuk semua hal.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c14 = RadioField("C1.4 Saya menggunakan AI untuk membantu menyusun langkah belajar.", choices=LIKERT_CHOICES, validators=[DataRequired()])

    # C2 Iterasi & Modifikasi
    c21 = RadioField("C2.1 Saya sering melakukan beberapa iterasi sampai hasil sesuai.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c22 = RadioField("C2.2 Saya mengubah/menyusun ulang output AI dengan kata-kata saya sendiri.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c23 = RadioField("C2.3 Saya meminta AI memberi contoh/penjelasan alternatif jika kurang jelas.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c24 = RadioField("C2.4 Saya menggunakan AI untuk mengecek struktur/kerapihan jawaban.", choices=LIKERT_CHOICES, validators=[DataRequired()])

    # C3 Verifikasi & Evaluasi
    c31 = RadioField("C3.1 Saya mengecek kembali jawaban AI menggunakan sumber lain.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c32 = RadioField("C3.2 Saya menilai apakah jawaban AI masuk akal sebelum digunakan.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c33 = RadioField("C3.3 Saya memeriksa istilah/rumus/kode dari AI sebelum dipakai.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c34 = RadioField("C3.4 Jika informasi meragukan, saya mencari pembanding dulu.", choices=LIKERT_CHOICES, validators=[DataRequired()])

    # C4 Orientasi Pemahaman
    c41 = RadioField("C4.1 AI membantu saya memahami konsep, bukan hanya menghasilkan jawaban.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c42 = RadioField("C4.2 Setelah memakai AI, saya masih berusaha menjelaskan ulang.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c43 = RadioField("C4.3 Saya menggunakan AI untuk latihan, bukan hanya hasil akhir.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c44 = RadioField("C4.4 Saya merasa AI membantu meningkatkan efisiensi belajar.", choices=LIKERT_CHOICES, validators=[DataRequired()])

    # C5 Etika & Kemandirian
    c51 = RadioField("C5.1 Saya menghindari menyalin output AI secara utuh tanpa revisi.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c52 = RadioField("C5.2 Saya mempertimbangkan aturan dosen/kelas terkait penggunaan AI.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c53 = RadioField("C5.3 Saya berusaha tetap mandiri sebelum meminta bantuan AI.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    c54 = RadioField("C5.4 Saya memilih AI sebagai alat bantu, bukan penentu utama.", choices=LIKERT_CHOICES, validators=[DataRequired()])

    # D. Situasi (opsional)
    d1 = RadioField("D1 Saat waktu terbatas, saya cenderung memilih AI sebagai bantuan utama.", choices=LIKERT_CHOICES, validators=[Optional()])
    d2 = RadioField("D2 Kadang saya memakai jawaban AI jika sudah terasa cukup tanpa mengecek terlalu jauh.", choices=LIKERT_CHOICES, validators=[Optional()])
    d3 = RadioField("D3 Saya menggunakan AI lebih banyak untuk tugas tertentu dibanding yang lain.", choices=LIKERT_CHOICES, validators=[Optional()])

    submit = SubmitField("Kirim")

    # Validasi eksklusif: jika pilih "never" tidak boleh bareng opsi lain (B1a & B2a)
    def validate_b1a_when_multi(self, field):
        if "never" in field.data and len(field.data) > 1:
            raise ValidationError('Pada B1a, pilihan "Hampir tidak pernah" harus berdiri sendiri.')

    def validate_b2a_what_multi(self, field):
        # B2a tidak punya "never", jadi tidak perlu eksklusif.
        # (Sesuai dokumen, eksklusif terutama untuk B1a/B2a jika ada "Hampir tidak pernah".)
        pass
