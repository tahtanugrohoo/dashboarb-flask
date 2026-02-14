import csv
from io import StringIO
from flask import Response
from flask_login import login_required
from . import export_bp
from ...models.response import QuestionnaireResponse

@export_bp.get("/summary.csv")
@login_required
def export_summary_csv():
    # Export ringkasan sederhana (tidak mengekspor jawaban mentah sensitif)
    total = QuestionnaireResponse.query.count()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["metric", "value"])
    writer.writerow(["total_responses", total])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=summary.csv"},
    )
