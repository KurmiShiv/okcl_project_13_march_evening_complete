from flask import Flask , request , jsonify,  url_for, request, session, redirect, render_template
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import datetime
import pymongo
import re
import bcrypt

app = Flask(__name__)
# connection with Mongo
app.secret_key = "secret"
app.config['MONGO_URI'] = "mongodb://localhost:27017/OKCL"
mongo = PyMongo(app)

# connection to MongoDB for login
client =pymongo.MongoClient("mongodb://localhost:27017/")
db =client['OKCL']
collection =db['login']



# flask call
app = Flask(__name__)




# Validate the email address using a regex.
def is_email_address_valid(email):
    
    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
        return False
    return True
# home page
@app.route('/')
def home():
    return render_template('login.html')
# add customer
@app.route('/add_customer')
def add_customer():
    return render_template('customer_registeration.html')
# register user
@app.route('/register', methods=['POST'])
def register():
    if request.method=='POST':
        _email = request.json['email']
        _password = request.json['password']
        _role = request.json['Role']

        # Validate the email address and raise an error if it is invalid
        if not is_email_address_valid(_email):
            return jsonify("Please enter a valid email address")

        # check if email already exist or not
        if collection.find_one({'email': _email}):
            return jsonify("Email Id already exist , Enter any other valid Email...")
            
        # validate the received values
        if  _email and _password and _role and request.method == 'POST':
            _hash_password = bcrypt.hashpw(_password.encode('utf-8'), bcrypt.gensalt())
            id = collection.insert_one({ 'email': _email, 'password': _hash_password , 'Role' : _role })
            return jsonify("Added Successfully") ,200
        
      
# login authentication
@app.route('/login', methods=['POST'])
def login():
    _email = request.form.get('email')
    _password = request.form.get('password')
    _role = request.form.get('Role')
    authenticate = False
    
	# check for user exist or not
    if collection.count_documents({'email':_email})==0:
        return jsonify("User not exist")
    login_user = collection.find({"email":_email})
    if login_user[0]['email'] == _email and login_user[0]['Role'] == _role:
        # password matching
        if bcrypt.hashpw(_password.encode('utf-8'), login_user[0]['password']) == login_user[0]['password']:
            authenticate = True
            #return jsonify("Login Successful"),200
            if(_role=="admin"):
                return render_template("admin.html")
            elif(_role=="manager"):
                return render_template("manager.html")
            elif(_role=="employee"):
                return render_template("employee.html")
            else: return "invalid role"
            
    if authenticate==False:
        return jsonify("Email or Password not matched")
    return render_template('login.html')
    

@app.route('/customer_registeration',methods = ['POST'])
def customer():
    _first_name = request.form.get('First Name')
    _middle_name = request.form.get('Middle Name')
    _last_name = request.form.get('Last Name')
    _dob = request.form.get('DOB')
    _gender = request.form.get('Gender')
    _mobile_no = request.form.get('Mobile Number')
    _emailid = request.form.get('Email')
    _city = request.form.get('City')
    _pin = request.form.get('PIN')
    
    
    now = datetime.now()
    data = mongo.db.Testing.find()
    if len(_mobile_no)<10 or len(_mobile_no)>10:
        return jsonify("Enter valid mobile no")
    if len(_pin)!=6:
        return jsonify("Enter 6 digit valid pin")
    for d in data:
        if d['Mobile Number'] == _mobile_no and d['Email'] == _emailid:
            return jsonify("User Mobile and Email already exist , Try with another Number and Email")
        if d['Mobile Number'] == _mobile_no:
            return jsonify("User Mobile already exist , Try with another Number")
        if d['Email'] == _emailid:
            return jsonify("User Email already exist , Try with another Number")
        

    id  = mongo.db.Testing.insert_one({'First Name':_first_name ,'Middle Name':_middle_name ,'Last Name':_last_name ,'DOB':_dob ,'Gender':_gender ,'Mobile Number':_mobile_no ,'Email':_emailid ,'City':_city ,'PIN':_pin , 'Date' : now.strftime("%d/%m/%Y %H:%M:%S") })
    resp = jsonify("Employee Added Successfully") , 200
    return resp

# by employee
@app.route('/employee',methods = ['GET'])
def employee():
    if request.method == 'GET':
        data = mongo.db.Testing.find()
        return render_template("employee.html",data=data)
 
# by manager       
@app.route('/manager',methods = ['GET' , 'POST'])
def manager():
    if request.method == 'GET':
        data = mongo.db.Testing.find()
        return render_template("manager.html",data=data)
    # for add new customer's details by manager
    if request.method=='POST':
        _first_name = request.json['First Name']
        _middle_name = request.json['Middle Name']
        _last_name = request.json['Last Name']
        _dob = request.json['DOB']
        _gender = request.json['Gender']
        _mobile_no = request.json['Mobile Number']
        _emailid = request.json['Email']
        _city = request.json['City']
        _pin = request.json['PIN']
        
        now = datetime.now()
        if len(_pin)!=6:
            return jsonify("Enter 6 digit valid pin")
        data = mongo.db.Testing.find()
        if len(_mobile_no)<10 or len(_mobile_no)>10:
            return jsonify("Enter valid mobile no")
        for d in data:
            if d['Mobile Number'] == _mobile_no and d['Email'] == _emailid:
                return jsonify("User Mobile and Email already exist , Try with another Number and Email")
            if d['Mobile Number'] == _mobile_no:
                return jsonify("User Mobile already exist , Try with another Number")
            if d['Email'] == _emailid:
                return jsonify("User Email already exist , Try with another Number")
            

        id  = mongo.db.Testing.insert_one({'First Name':_first_name ,'Middle Name':_middle_name ,'Last Name':_last_name ,'DOB':_dob ,'Gender':_gender ,'Mobile Number':_mobile_no ,'Email':_emailid ,'City':_city ,'PIN':_pin , 'Date' : now.strftime("%d/%m/%Y %H:%M:%S") })
        resp = jsonify("Employee Added Successfully") , 200
        return resp
    
# for edit details of customer by manager
"""@app.route('/manager/<email>' , methods =['PUT'])
def manager1(email):
    if request.method == 'PUT':
        _first_name = request.json['First Name']
        _middle_name = request.json['Middle Name']
        _last_name = request.json['Last Name']
        _dob = request.json['DOB']
        _gender = request.json['Gender']
        _mobile_no = request.json['Mobile Number']
        _emailid = request.json['Email']
        _city = request.json['City']
        _pin = request.json['PIN']
        
        if len(_pin)>0:
            if len(_pin)!=6:
                return jsonify("Enter 6 digit valid pin")
        
        data = mongo.db.Testing.find()
        for d in data:
            if d['Email'] == email:
                if len(_first_name)>0:
                    mongo.db.Testing.update_one({"Email":d['Email']} , {"$set":{"First Name":_first_name}})
                if len(_middle_name)>0:
                    mongo.db.Testing.update_one({"Email":d['Email']} , {"$set":{"Middle Name":_middle_name}})
                if len(_last_name)>0:
                    mongo.db.Testing.update_one({"Email":d['Email']} , {"$set":{"Last Name":_last_name}})
                if len(_dob)>0:
                    mongo.db.Testing.update_one({"Email":d['Email']} , {"$set":{"DOB":_dob}})
                if len(_gender)>0:
                    mongo.db.Testing.update_one({"Email":d['Email']} , {"$set":{"Gender":_gender}})
                if len(_mobile_no)>0:
                    mongo.db.Testing.update_one({"Email":d['Email']} , {"$set":{"Mobile Number":_mobile_no}})
                if len(_emailid)>0:
                    mongo.db.Testing.update_one({"Email":d['Email']} , {"$set":{"Email":_emailid}})
                if len(_city)>0:
                    mongo.db.Testing.update_one({"Email":d['Email']} , {"$set":{"City":_city}})
                if len(_pin)>0:
                    mongo.db.Testing.update_one({"Email":d['Email']} , {"$set":{"PIN":_pin}})
                    
        return jsonify("User Updated Successfully") , 200"""
    
# by admin   
@app.route('/admin',methods=['GET' , 'POST'])
def admin1():
    if request.method == 'GET':# getting all customer list
        data = mongo.db.Testing.find()
        return render_template("admin.html",data=data)
    # adding new customer by admin
    if request.method=='POST':
        _first_name = request.json['First Name']
        _middle_name = request.json['Middle Name']
        _last_name = request.json['Last Name']
        _dob = request.json['DOB']
        _gender = request.json['Gender']
        _mobile_no = request.json['Mobile Number']
        _emailid = request.json['Email']
        _city = request.json['City']
        _pin = request.json['PIN']
        
        now = datetime.now()
        data = mongo.db.Testing.find()
        if len(_mobile_no)<10 or len(_mobile_no)>10:
            return jsonify("Enter valid mobile no")
        for d in data:
            if d['Mobile Number'] == _mobile_no and d['Email'] == _emailid:
                return jsonify("User Mobile and Email already exist , Try with another Number and Email")
            if d['Mobile Number'] == _mobile_no:
                return jsonify("User Mobile already exist , Try with another Number")
            if d['Email'] == _emailid:
                return jsonify("User Email already exist , Try with another Number")
            

        id  = mongo.db.Testing.insert_one({'First Name':_first_name ,'Middle Name':_middle_name ,'Last Name':_last_name ,'DOB':_dob ,'Gender':_gender ,'Mobile Number':_mobile_no ,'Email':_emailid ,'City':_city ,'PIN':_pin , 'Date' : now.strftime("%d/%m/%Y %H:%M:%S") })
        resp = jsonify("Employee Added Successfully") , 200
        return resp
# update route    
@app.route('/update_customer/<id>') 
def update_customer(id):
    return render_template("update_details.html",id=id) 

#updating customer's details 
@app.route('/update/<id>' , methods=['POST'])
def update(id):
    if request.method == 'POST':# for updation
        _first_name = request.form.get('First Name')# we are getting data from form
        _middle_name = request.form.get('Middle Name')
        _last_name = request.form.get('Last Name')
        _dob = request.form.get('DOB')
        _gender = request.form.get('Gender')
        _mobile_no = request.form.get('Mobile Number')
        _emailid = request.form.get('Email')
        _city = request.form.get('City')
        _pin = request.form.get('PIN')
        
        if len(_pin)>0:
            if len(_pin)!=6:
                return jsonify("Enter 6 digit valid pin")
        
        data = mongo.db.Testing.find()
        for d in data:
            if d['_id'] == ObjectId(id):
                if len(_first_name)>0:
                    mongo.db.Testing.update_one({"_id":d['_id']} , {"$set":{"First Name":_first_name}})
                if len(_middle_name)>0:
                    mongo.db.Testing.update_one({"_id":d['_id']} , {"$set":{"Middle Name":_middle_name}})
                if len(_last_name)>0:
                    mongo.db.Testing.update_one({"_id":d['_id']} , {"$set":{"Last Name":_last_name}})
                if len(_dob)>0:
                    mongo.db.Testing.update_one({"_id":d['_id']} , {"$set":{"DOB":_dob}})
                #if len(_gender)>0:
                mongo.db.Testing.update_one({"_id":d['_id']} , {"$set":{"Gender":_gender}})
                if len(_mobile_no)>0:
                    mongo.db.Testing.update_one({"_id":d['_id']} , {"$set":{"Mobile Number":_mobile_no}})
                if len(_emailid)>0:
                    mongo.db.Testing.update_one({"_id":d['_id']} , {"$set":{"Email":_emailid}})
                if len(_city)>0:
                    mongo.db.Testing.update_one({"_id":d['_id']} , {"$set":{"City":_city}})
                if len(_pin)>0:
                    mongo.db.Testing.update_one({"_id":d['_id']} , {"$set":{"PIN":_pin}})
                return jsonify("User Updated Successfully") , 200   
        return jsonify("User not updated")   
    
@app.route('/delete_by_admin/<id>' , methods=['POST'])
def delete_by_admin(id):
    if request.method=='POST': #deleting by email of customer
        data = mongo.db.Testing.find()
        for d in data:
            if d['_id']== ObjectId(id):
                query = {"_id":ObjectId(id)}
                mongo.db.Testing.delete_one(query)
                resp = jsonify("User Deleted") , 200
                return resp
        resp = jsonify("User not exist") , 200
        return resp
    
if __name__ == '__main__':
    app.run(debug = True)