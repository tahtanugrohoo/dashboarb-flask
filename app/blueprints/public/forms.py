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
    # Persetujuan
    consent = BooleanField("Saya bersedia berpartisipasi secara sukarela", validators=[DataRequired()])

    # Profil
    name_optional = StringField("Nama (opsional)", validators=[Optional(), Length(max=150)])
    university = StringField("Universitas", validators=[DataRequired(), Length(max=150)])
    major = StringField("Jurusan/Program Studi", validators=[DataRequired(), Length(max=150)])
    semester = RadioField("Semester", choices=SEMESTER_CHOICES, validators=[DataRequired()])
    used_ai = RadioField("Pernah menggunakan AI generatif untuk kegiatan akademik?", choices=YESNO_CHOICES, validators=[DataRequired()])

    # Pola umum
    when_multi = SelectMultipleField("Kapan biasanya Anda menggunakan AI generatif? (boleh pilih lebih dari satu)",
                                     choices=WHEN_CHOICES, validators=[DataRequired()])
    when_other_text = StringField("Jika memilih 'Lainnya', tuliskan:", validators=[Optional(), Length(max=200)])

    when_single = RadioField("Dari pilihan di atas, mana yang paling sering?", choices=WHEN_CHOICES, validators=[DataRequired()])
    when_single_other_text = StringField("Jika memilih 'Lainnya', tuliskan:", validators=[Optional(), Length(max=200)])

    use_multi = SelectMultipleField("Untuk kebutuhan akademik, AI paling sering Anda gunakan untuk apa saja? (boleh pilih lebih dari satu)",
                                    choices=USE_CHOICES, validators=[DataRequired()])
    use_other_text = StringField("Jika memilih 'Lainnya', tuliskan:", validators=[Optional(), Length(max=200)])

    use_single = RadioField("Dari pilihan di atas, mana yang paling sering?", choices=USE_CHOICES, validators=[DataRequired()])
    use_single_other_text = StringField("Jika memilih 'Lainnya', tuliskan:", validators=[Optional(), Length(max=200)])

    portion = RadioField("Seberapa besar porsi AI dalam pengerjaan tugas saat Anda menggunakannya?", choices=PORTION_CHOICES, validators=[DataRequired()])
    freq = RadioField("Seberapa sering menggunakan AI untuk kegiatan akademik?", choices=FREQ_CHOICES, validators=[DataRequired()])

    # Tujuan & Perencanaan
    p1 = RadioField("Saya menggunakan AI dengan tujuan yang jelas.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    p2 = RadioField("Saya biasanya menuliskan konteks yang cukup saat bertanya ke AI.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    p3 = RadioField("Saya memilih AI sebagai bantuan yang sesuai kebutuhan, bukan untuk semua hal.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    p4 = RadioField("Saya menggunakan AI untuk membantu menyusun langkah belajar.", choices=LIKERT_CHOICES, validators=[DataRequired()])

    # Iterasi & Modifikasi
    i1 = RadioField("Saya sering melakukan beberapa iterasi sampai hasil sesuai.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    i2 = RadioField("Saya mengubah/menyusun ulang output AI dengan kata-kata saya sendiri.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    i3 = RadioField("Saya meminta AI memberi contoh/penjelasan alternatif jika kurang jelas.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    i4 = RadioField("Saya menggunakan AI untuk mengecek struktur/kerapihan jawaban.", choices=LIKERT_CHOICES, validators=[DataRequired()])

    # Verifikasi & Evaluasi
    v1 = RadioField("Saya mengecek kembali jawaban AI menggunakan sumber lain.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    v2 = RadioField("Saya menilai apakah jawaban AI masuk akal sebelum digunakan.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    v3 = RadioField("Saya memeriksa istilah/rumus/kode dari AI sebelum dipakai.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    v4 = RadioField("Jika informasi meragukan, saya mencari pembanding dulu.", choices=LIKERT_CHOICES, validators=[DataRequired()])

    # Orientasi Pemahaman
    u1 = RadioField("AI membantu saya memahami konsep, bukan hanya menghasilkan jawaban.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    u2 = RadioField("Setelah memakai AI, saya masih berusaha menjelaskan ulang.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    u3 = RadioField("Saya menggunakan AI untuk latihan, bukan hanya hasil akhir.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    u4 = RadioField("Saya merasa AI membantu meningkatkan efisiensi belajar.", choices=LIKERT_CHOICES, validators=[DataRequired()])

    # Etika & Kemandirian
    e1 = RadioField("Saya menghindari menyalin output AI secara utuh tanpa revisi.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    e2 = RadioField("Saya mempertimbangkan aturan dosen/kelas terkait penggunaan AI.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    e3 = RadioField("Saya berusaha tetap mandiri sebelum meminta bantuan AI.", choices=LIKERT_CHOICES, validators=[DataRequired()])
    e4 = RadioField("Saya memilih AI sebagai alat bantu, bukan penentu utama.", choices=LIKERT_CHOICES, validators=[DataRequired()])

    # Situasi (opsional)
    s1 = RadioField("Saat waktu terbatas, saya cenderung memilih AI sebagai bantuan utama.", choices=LIKERT_CHOICES, validators=[Optional()])
    s2 = RadioField("Kadang saya memakai jawaban AI jika sudah terasa cukup tanpa mengecek terlalu jauh.", choices=LIKERT_CHOICES, validators=[Optional()])
    s3 = RadioField("Saya menggunakan AI lebih banyak untuk tugas tertentu dibanding yang lain.", choices=LIKERT_CHOICES, validators=[Optional()])

    submit = SubmitField("Kirim")

    # Validasi: jika "Hampir tidak pernah" dipilih, harus berdiri sendiri
    def validate_when_multi(self, field):
        if "never" in field.data and len(field.data) > 1:
            raise ValidationError('Pilihan "Hampir tidak pernah" harus berdiri sendiri.')

    # Validasi "Lainnya" harus diisi kalau dipilih
    def validate_when_other_text(self, field):
        if "other" in (self.when_multi.data or []) and not (field.data or "").strip():
            raise ValidationError("Anda memilih 'Lainnya', mohon isi teksnya.")

    def validate_when_single_other_text(self, field):
        if self.when_single.data == "other" and not (field.data or "").strip():
            raise ValidationError("Anda memilih 'Lainnya', mohon isi teksnya.")

    def validate_use_other_text(self, field):
        if "other" in (self.use_multi.data or []) and not (field.data or "").strip():
            raise ValidationError("Anda memilih 'Lainnya', mohon isi teksnya.")

    def validate_use_single_other_text(self, field):
        if self.use_single.data == "other" and not (field.data or "").strip():
            raise ValidationError("Anda memilih 'Lainnya', mohon isi teksnya.")
