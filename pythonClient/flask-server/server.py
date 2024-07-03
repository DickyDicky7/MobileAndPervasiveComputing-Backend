from flask import Flask # type: ignore
from aimodel import ai_bp
from arrange import arrange_bp

app = Flask(__name__)
app.register_blueprint(ai_bp)
app.register_blueprint(arrange_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=27018, debug=True)