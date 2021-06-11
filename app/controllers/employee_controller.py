from flask import Blueprint,request,jsonify
from app.models.models import Employee
from app.database.connect import sess

bp = Blueprint('bp',__name__)


@bp.route("/",methods=['GET'])
def index():
    return "Home Page"


@bp.route('/employee/add',methods=['POST'])
def create():
    try:
        data=request.get_json()

        if data.get('title')==None:
            raise Exception('ERROR title is empty')
        if data.get('experience')==None:
            raise Exception('ERROR experience is empty')

        emp=Employee(**data)
        sess.add(emp)
        sess.commit()
        return jsonify({"OK":"true","data":data}),200
    except Exception as e:
        sess.rollback()
        return jsonify({"OK":"false","data":{"error":str(e)}}),422


@bp.route('/employee/<int:id>/delete',methods=['DELETE'])
def delete_Employee(id):
    try:
        emp=sess.query(Employee).filter_by(id=id).first()
        if emp==None:
            return jsonify({"OK":"true","data":{"message":"User Doesn't Exist!"}}),200
        sess.delete(emp)
        sess.commit()
        return jsonify({"OK":"true","data":{"message":"Data Deleted!"}}),200
    except Exception as e:
        sess.rollback()
        return jsonify({"OK":"false","data":{"error":str(e)}}),422



@bp.route('/employee/<int:id>/update',methods=['PUT'])
def update_data(id):
    try:
        data=request.get_json()
        sess.query(Employee).filter_by(id=id).update(data)
        sess.commit()
        return jsonify({"OK":"true","data":data,"message":"Data Updated!"}),200
    except Exception as e:
        sess.rollback()
        return jsonify({"OK":"false","data":{"error":str(e)}}),422

@bp.route('/employee/<int:id>/fetch',methods=['GET'])
def fetch_data(id):
    try:
        emp=sess.query(Employee).filter_by(id=id).first()
        if emp==None:
            return jsonify({"OK":"true","data":{"message":"User Doesn't Exist!"}}),200
        return {"id":id,"OK":"true","data":{"title":emp.title,"dept":emp.department,"country":emp.country,"state":emp.state,"city":emp.city,"remote":emp.remote,"description":emp.description,"requirements":emp.requirements,"benifit":emp.benifits,"comind":emp.company_industry,"job_fun":emp.job_function,"employment_type":emp.employment_type,"experience":emp.experience,"education":emp.education,"keywords":emp.keywords,"salaryFrom":emp.salary_from,"salaryTo":emp.salary_to,"currency":emp.currency}}
    except Exception as e:
        return jsonify({"OK":"false","data":{"error":str(e)}}),422


@bp.route('/employee/fetchall',methods=['GET'])
def fetch():
    try:
        emp=sess.query(Employee).all()
        if len(emp)==0:
            return jsonify({"OK":"true","data":{"Message":"Empty Database"}}),200
        return jsonify({"OK":"true","data":[i.title for i in emp]}),200
    except Exception as e:
        return jsonify({"OK":"false","data":{"error":str(e)}}),422