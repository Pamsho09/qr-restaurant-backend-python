from flask import request, Blueprint,jsonify
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from flask_httpauth import HTTPTokenAuth
from config.default import SECRET_KEY
restaurant_v1_0_bp = Blueprint('restaurant_v1_0_bp', __name__)
from py_jwt_validator import PyJwtValidator, PyJwtException
from app.db import mongoQuery
auth = HTTPTokenAuth(scheme='Bearer')

api = Api(restaurant_v1_0_bp)
@auth.verify_token
def verify_token(token):
    try:
        jwt.decode(token, SECRET_KEY)
        return True
    except jwt.ExpiredSignatureError:
        return False

class addUser(Resource):
 
    def post(self):
       
        username=request.json['username']
        password=request.json['password']
        email=request.json['email']
        nameRestaurant=request.json['nameRestaurant']
        address=request.json['address']

        if username and email and password and nameRestaurant and address:
            hashed_password=generate_password_hash(password)
            mongoQuery.save({'username':username,'password':hashed_password,'email':email,'restaurant':nameRestaurant,'address':address } ,"users")
        
            response={
           'username':username,
           'password':hashed_password,
           'email':email,
           'restaurant':nameRestaurant,
           'address':address
            }
            return  response,201
        else:
            response= {'messege':'error'}
            return response,401       

class login(Resource):
   
    def post(self):
        password=request.json['password']
        email=request.json['email']
        data= mongoQuery.get({"email":email,},"users")
        print(data)
        if data:
         
            if check_password_hash(data['password'],password):
                print('llego2')
                token=jwt.encode({'user':data['username'],'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=1440)},SECRET_KEY)
                return jsonify({'token':token})
        else:
            return { 'messege':'no se pudo'}
        
        print(data)

def uncodeToken(tokenU):
    
    return jwt.decode(tokenU[1],SECRET_KEY)

class dashBoardMenu(Resource):
    @auth.login_required 
    def post(self):
        default=""
        data= request.files['file']
       


        return jsonify({"messege":data}) 

class verifyToken(Resource):
    def post(self):
        token = request.json
      
        try:
            jwt.decode(token, SECRET_KEY)
            return {'status':200,'pass':True,'messege':'verify token :)'},200
          
        except jwt.ExpiredSignatureError:
            return {'status':401,'pass':False,'messege':'invalid token :('},401
       

api.add_resource(addUser, '/api/v1.0/addUser/', endpoint='add_user',)
api.add_resource(login, '/api/v1.0/login/', endpoint='login')
api.add_resource(dashBoardMenu, '/api/v1.0/dashBoard/Menu', endpoint='dashBoard')
api.add_resource(verifyToken,'/api/v1.0/verifyToken/',endpoint="verifyToken")