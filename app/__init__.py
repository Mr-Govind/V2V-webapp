from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)

    app.config["UPLOAD_DIR"] = os.path.join(project_root, "data", "uploads")
    app.config["RESP_DIR"] = os.path.join(project_root, "data", "responses")

    os.makedirs(app.config["UPLOAD_DIR"], exist_ok=True)
    os.makedirs(app.config["RESP_DIR"], exist_ok=True)

    from .pages import pages_bp
    from .api import api_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
