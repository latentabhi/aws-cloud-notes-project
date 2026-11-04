import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, send_from_directory
from .database import fetch_all_notes, insert_note, update_note, remove_note
from .s3_service import upload_attachment

routes = Blueprint("routes", __name__)


@routes.route("/")
def index():
    return render_template("index.html")


@routes.route("/notes", methods=["GET"])
def list_notes():
    notes = fetch_all_notes()
    return jsonify(notes)


@routes.route("/notes", methods=["POST"])
def create_note():
    title = request.form.get("title", "").strip()
    body = request.form.get("body", "").strip()

    if not title:
        return jsonify({"error": "Title is required"}), 400

    note_id = str(uuid.uuid4())[:8]
    added_on = datetime.now().strftime("%d-%m-%Y %H:%M")

    file_url = None
    uploaded_file = request.files.get("file")
    if uploaded_file and uploaded_file.filename:
        filename = f"{note_id}_{uploaded_file.filename}"
        file_url = upload_attachment(uploaded_file, filename)

    insert_note(note_id, title, body, file_url, added_on)

    return jsonify({
        "id": note_id,
        "title": title,
        "body": body,
        "file_url": file_url,
        "added_on": added_on
    }), 201


@routes.route("/notes/<note_id>", methods=["POST", "PUT", "DELETE"])
def handle_single_note(note_id):
    if request.method == "DELETE":
        success = remove_note(note_id)
        if not success:
            return jsonify({"error": "Note not found"}), 404
        return jsonify({"message": "Note deleted successfully", "id": note_id})

    title = request.form.get("title", "").strip()
    body = request.form.get("body", "").strip()

    if not title:
        return jsonify({"error": "Title is required"}), 400

    file_url = None
    uploaded_file = request.files.get("file")
    if uploaded_file and uploaded_file.filename:
        filename = f"{note_id}_{uploaded_file.filename}"
        file_url = upload_attachment(uploaded_file, filename)

    success = update_note(note_id, title, body, file_url)
    if not success:
        return jsonify({"error": "Note not found"}), 404

    return jsonify({"message": "Note updated successfully", "id": note_id})


@routes.route("/uploads/<filename>")
def serve_local_upload(filename):
    project_root = os.path.dirname(os.path.dirname(__file__))
    upload_folder = os.path.join(project_root, "uploads")
    return send_from_directory(upload_folder, filename)
