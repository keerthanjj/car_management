from flask import Flask, jsonify
from controller.admin_controller import admin_bp
from controller.user_controller import user_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')

# New route for status check
@app.route('/', methods=['GET'])
def check_status():
    return jsonify({"status": "ok", "message": "API is running"}), 200

if __name__ == '__main__':
    app.run(debug=True)
