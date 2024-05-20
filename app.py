from flask import Flask
from controller.admin_controller import admin_bp
from controller.user_controller import user_bp


app = Flask(__name__)
# Register blueprint
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == '__main__':
    app.run(debug=True)
