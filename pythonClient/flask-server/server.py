from flask import Flask # type: ignore
from aimodel import ai_bp
from arrange import arrange_bp
from hub import hub_bp
from order import order_bp
from staff import staff_bp
from user import user_bp
from momo import momo_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This allows all domains to make requests to your server
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(ai_bp)
app.register_blueprint(arrange_bp)
app.register_blueprint(hub_bp)
app.register_blueprint(order_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(user_bp)
app.register_blueprint(momo_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=27018, debug=True)
