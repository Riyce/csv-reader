import os

from flask import Blueprint, render_template, request, send_file

from config import settings
from utils import CSVWorker, get_file_name

index_bp = Blueprint("index", __name__)


@index_bp.route("/", methods=["POST", "GET"])
def index():
	if request.method == "POST":
		file = request.files["file"]
		if file:
			filename = get_file_name(file.filename)
			file.save(os.path.join(settings.UPLOAD_FOLDER, filename))
			uploaded_file = os.path.join(settings.UPLOAD_FOLDER, filename)
		else:
			uploaded_file = os.path.join(settings.MEDIA_FOLDER, "default", "default.csv")
		updater = CSVWorker(uploaded_file)
		new_file = updater.process()
		return send_file(new_file)
	return render_template("index.html")
