from flask import Flask
from config import Config
from routes.deals_route import deals_bp
from database.model import db

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(deals_bp, url_prefix="/deals")
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return {"msg": "App is running"}


if __name__ == "__main__":
    app.run(debug=True)
