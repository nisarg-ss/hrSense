from flask import Flask
from app.controllers.employee_controller import bp as employee_bp
import os

app=Flask(__name__)
app.config['SECRET_KEY']=os.environ.get('secret_key')
app.register_blueprint(employee_bp)

@app.route("/",methods=['GET'])
def index():
    return "Home Page"


if __name__=="__main__":
    app.run(debug=True)