from flask import Flask, jsonify
from config import Config
from routes.deals_route import deals_bp
from database.model import db
from utils.stats import record_request
app = Flask(__name__)

app.config.from_object(Config)

app.register_blueprint(deals_bp, url_prefix="/deals")

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return {"msg": "App is running"}


@app.after_request
def count_request(response):
    record_request(success=response.status_code < 400)
    return response

@app.errorhandler(400)
def bad_request(_error):
    return jsonify({"error": "Bad request"}), 400


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(405)
def method_not_allowed(_error):
    return jsonify({"error": "Method not allowed for this endpoint"}), 405


@app.errorhandler(500)
def internal_error(_error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
