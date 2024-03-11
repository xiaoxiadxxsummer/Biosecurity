from flask import Flask
from controller.DefaultController import bp as default_bp
from controller.EmployeeController import bp as employee_bp
from controller.ApiaristController import bp as apiarist_bp
from GuideController import bp as guide_bp

app = Flask(__name__)
app.static_folder = 'static'
app.static_url_path = ''


def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp



app.after_request(after_request)
app.register_blueprint(default_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(apiarist_bp)
app.register_blueprint(guide_bp)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3001, debug=True)
