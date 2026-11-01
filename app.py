"""
Serveur du portfolio d'Emmanuel Ajavon (tous les fichiers à la racine).

Local :        python app.py        -> http://localhost:8000
Production :   gunicorn app:app
"""
import os
from flask import Flask, send_from_directory

BASE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=None)

# Seuls ces fichiers sont publics (app.py et requirements.txt restent privés)
PUBLICS = {"index.html", "style.css", "app.js", "photo.jpg", "jang.jpg",
           "poster.jpg", "robots.txt"}


@app.route("/")
def accueil():
    return send_from_directory(BASE, "index.html")


@app.route("/<nom>")
def fichier(nom):
    if nom in PUBLICS:
        return send_from_directory(BASE, nom)
    return send_from_directory(BASE, "index.html")


@app.after_request
def entetes(rep):
    if rep.mimetype and rep.mimetype.startswith("image/"):
        rep.headers["Cache-Control"] = "public, max-age=2592000"
    else:
        rep.headers["Cache-Control"] = "public, max-age=300"
    rep.headers["X-Content-Type-Options"] = "nosniff"
    rep.headers["X-Frame-Options"] = "DENY"
    rep.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return rep


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
