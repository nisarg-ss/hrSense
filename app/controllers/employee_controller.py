from flask import Blueprint,request,jsonify
from app.models.models import Employee
from app.database.connect import sess
import json

bp = Blueprint('bp',__name__)


@bp.route('/employee',methods=['POST'])
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
        return jsonify({"OK":"false","error":str(e),"data":{}}),400


@bp.route('/employee/<int:id>',methods=['DELETE'])
def delete_Employee(id):
    try:
        emp=sess.query(Employee).filter_by(id=id).first()
        if emp==None:
            return jsonify({"OK":"true","error":"User Doesn't Exist!","data":{}}),422
        sess.delete(emp)
        sess.commit()
        return jsonify({"OK":"true","message":"Data Deleted!","data":{}}),200
    except Exception as e:
        sess.rollback()
        return jsonify({"OK":"false","error":str(e),"data":{}}),400


@bp.route('/employee/<int:id>',methods=['PUT'])
def update_data(id):
    try:
        data=request.get_json()

        emp=sess.query(Employee).filter_by(id=id).first()
        if emp==None:
            return jsonify({"OK":"true","error":"User Doesn't Exist!","data":{}}),422

        sess.query(Employee).filter_by(id=id).update(data)
        sess.commit()
        return jsonify({"OK":"true","data":data,"message":"Data Updated!"}),200
    except Exception as e:
        sess.rollback()
        return jsonify({"OK":"false","error":str(e),"data":{}}),400

@bp.route('/employee/<int:id>',methods=['GET'])
def fetch_data(id):
    try:
        emp=sess.query(Employee).filter_by(id=id).first()
        if emp==None:
            return jsonify({"OK":"true","error":"User Doesn't Exist!","data":{}}),422
        
        row2dict = lambda emp: {c.name: str(getattr(emp, c.name)) for c in emp.__table__.columns}
        return jsonify({"OK":"true","data":row2dict(emp)}),200
        
    except Exception as e:
        return jsonify({"OK":"false","error":str(e),"data":{}}),400


@bp.route('/employee/fetchall',methods=['GET'])
def fetch():
    try:
        emp=sess.query(Employee).all()
        if len(emp)==0:
            return jsonify({"OK":"true","Message":"Empty Database","data":{}}),200
        return jsonify({"OK":"true","data":[{"title":i.title,"id":i.id} for i in emp]}),200
    except Exception as e:
        return jsonify({"OK":"false","error":str(e),"data":{}}),400