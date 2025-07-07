from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import secrets
import string
from datetime import datetime, timezone

app = Flask(__name__)

# CREATE Base
class Base(DeclarativeBase):
    pass

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_database.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

#Create Database
class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    shortCode = db.Column(db.String(12), unique=True, nullable=False)
    created = db.Column(db.String(20), nullable=False)
    updated = db.Column(db.String, nullable=True, default="null")
    accessCount = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

def generate_short(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


def generate_unique_short():
    while True:
        short_url = generate_short()
        if not db.session.query(Url).filter_by(shortCode=short_url).first():
            return short_url


def get_url_item(short_code):
    return db.session.execute(db.select(Url).where(Url.shortCode == short_code)).scalar()


def url_to_json(item):
    return {
        "id": item.id,
        "url": item.url,
        "shortCode": item.shortCode,
        "createdAt": item.created,
        "updated": item.updated,
        "accessCount":item.accessCount
    }

@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.form.get("url")
    short_code = generate_unique_short()
    new_url = Url(url=data, shortCode=short_code, created=datetime.now(timezone.utc).isoformat())
    db.session.add(new_url)
    db.session.commit()
    item = get_url_item(short_code)
    return jsonify(url_to_json(item)), 201

@app.route("/shorten/<short_url>", methods=["GET"])
def get_url(short_url):
    try:
        item = get_url_item(short_url)
        item.accessCount+=1
        db.session.commit()
        return  jsonify(url_to_json(item)), 200
    except AttributeError:
        return "", 404

@app.route("/shorten/<short_url>", methods=["PUT"])
def update_url(short_url):
    try:
        data = request.form.get("url")
        item=get_url_item(short_url)
        item.url=data
        item.updated=datetime.now(timezone.utc).isoformat()
        db.session.commit()
        return jsonify(url_to_json(item)), 200
    except AttributeError:
        return "", 404

@app.route("/shorten/<short_url>", methods=["DELETE"])
def delete_url(short_url):
    try:
        item = get_url_item(short_url)
        db.session.delete(db.get_or_404(Url, item.id))
        db.session.commit()
        return "", 204
    except AttributeError:
        return "", 404

@app.route("/shorten/<short_url>/stats", methods=["GET"])
def url_stats(short_url):
    item = get_url_item(short_url)
    return jsonify(url_to_json(item)), 200


if __name__=="__main__":
    app.run()