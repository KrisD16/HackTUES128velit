from flask import Flask, redirect
from flasgger import Swagger
from controllers.auth_controller import auth_bp
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "your_secret_key_change_in_production"
)
swagger = Swagger(app)

app.register_blueprint(auth_bp)


@app.route("/", methods=["GET"])
def index():
    return redirect("/apidocs")


@app.errorhandler(404)
def not_found(error):
    return {"error": "Not found"}, 404


@app.errorhandler(500)
def internal_error(error):
    return {"error": "Internal server error"}, 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
