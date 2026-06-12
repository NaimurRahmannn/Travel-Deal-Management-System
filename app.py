from flask import Flask
from config import Config
from routes.deals_route import deals_bp

app = Flask(__name__)
app.register_blueprint(deals_bp, url_prefix="/deals")




if __name__ == "__main__":
    app.run(debug=True)
