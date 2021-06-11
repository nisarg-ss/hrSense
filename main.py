from flask import Flask,request,jsonify
from app.controllers.employee_controller import bp

app=Flask(__name__)
app.register_blueprint(bp)

@app.route("/",methods=['GET'])
def index():
    return "Home Page"


if __name__=="__main__":
    app.run(debug=True)