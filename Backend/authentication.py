from flask import Flask
from controllers.auth_controller import auth_bp

app = Flask(__name__)

app.register_blueprint(auth_bp)


@app.route("/", methods=["GET"])
def index():
    return {"message": "Marketplace Backend is running!"}


if __name__ == "__main__":
    app.run(debug=True)
