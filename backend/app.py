from flask import Flask
from flask_cors import CORS
from api.analyze import analyze_bp

def create_app():
    """
    Application factory for Cognicode Backend.
    Ensures modularity and easy testing.
    """
    app = Flask(__name__)
    CORS(app)

    # Register Blueprints
    app.register_blueprint(analyze_bp)

    @app.route('/health', methods=['GET'])
    def health():
        return {"status": "healthy"}, 200

    return app

if __name__ == "__main__":
    app = create_app()
    # Design Note: Using host='0.0.0.0' for accessibility in dev environments
    app.run(host='0.0.0.0', port=5000, debug=True)