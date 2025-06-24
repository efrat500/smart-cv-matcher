from flask import Flask
from routes.job_routes import job_bp
from routes.profile_routes import profile_bp

app = Flask(__name__)
app.register_blueprint(job_bp, url_prefix="/jobs")
app.register_blueprint(profile_bp, url_prefix="/profile")


if __name__ == "__main__":
    app.run(debug=True)
