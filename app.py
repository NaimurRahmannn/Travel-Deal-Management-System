from flask import Flask
from config import Config
app=Flask(__name__)

@app.route("/")
def home():
    return {"msg": "App is running"}

if __name__ == "__main__":
    app.run(debug=True)