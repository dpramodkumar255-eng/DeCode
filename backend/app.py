from flask import Flask, jsonify
from routes.analysis import analysis_bp
from routes.dashboard import dashboard_bp
from routes.profile import profile_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(analysis_bp, url_prefix='/api')
app.register_blueprint(dashboard_bp, url_prefix='/api')
app.register_blueprint(profile_bp, url_prefix='/api')

@app.route("/")
def index():
    return jsonify({
        "status": "online",
        "message": "Placement Readiness Dashboard API is running."
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
