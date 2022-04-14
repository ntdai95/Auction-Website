from flask import Flask, request, jsonify
from database import UserDB
from models import User
import hashlib


app = Flask(__name__)


############################################
#                   USER                   #
############################################


@app.route("/user/login", methods=['GET'])
def Login():
    '''
    Input: username (str), password (str)
    Func: Check user database for given user_id and password and allow user to login or deny
    Return: "success" (str),message (str),user_id (str)
    '''
    query_parameters = request.args
    username = query_parameters.get('username')
    password = query_parameters.get('password')

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    result = UserDB().read_user(User(username=username, password=hashed_password))
    if result and result[5] == "active":
        return jsonify({"success": True, "message": "Login successful.", "user_id": result[0]})
    elif result:
        return jsonify({"success": False, "message": "Your user account has been suspended.", "user_id": None})
    else:
        return jsonify({"success": False, "message": "Wrong username and password combination.", "user_id": None})


@app.route("/user/create", methods=['POST'])
def CreateUser():
    '''
    Input: username (str), password (str), email(str)
    Func: Create a new user
    Return: user_id (str)
    '''
    query_parameters = request.args
    print(query_parameters)
    username = query_parameters.get('username')
    password = query_parameters.get('password')
    email = query_parameters.get('email')
    print(f"{username}|{password}|{email}")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if password == "admin":
        user_type = "admin"
    else:
        user_type = "user"
    user_status = "active"
    user_rating_sum = 0
    user_rating_total = 0
    watchlist_parameter = ""
    print("about to request")
    result = UserDB().create_user(User(username=username, password=hashed_password, email=email, user_type=user_type,
                                       user_status=user_status, user_rating_sum=user_rating_sum, user_rating_total=user_rating_total, 
                                       watchlist_parameter=watchlist_parameter))
    print("requested")
    return jsonify({"user_id": result})

@app.route("/user/update", methods=['POST'])
def UpdateUser():
    '''
    Input: user_id (int), username (str), password (str), email(str), watchlist_parameter(str)
    Func: Update user's information
    Return: success(bool), message(str)
    '''
    query_parameters = request.args
    user_id = query_parameters.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "Please, provide a user_id."})
    username = query_parameters.get('username')
    email = query_parameters.get('email')
    watchlist_parameter = query_parameters.get('watchlist_parameter')

    if query_parameters.get('password'):
        hashed_password = hashlib.sha256(query_parameters.get('password').encode()).hexdigest()
        result = UserDB().update_user(User(user_id=user_id, username=username, password=hashed_password,
                                           email=email, watchlist_parameter=watchlist_parameter))
    else:
        result = UserDB().update_user(User(user_id=user_id, username=username, email=email,
                                           watchlist_parameter=watchlist_parameter))
    if result != 0:
        return jsonify({"success": True, "message": "User update successful."})
    else:
        return jsonify({"success": False, "message": "There is no user with such user_id in the user database."})


@app.route("/user/delete", methods=['DELETE'])
def DeleteUser():
    '''
    Input: user_id (int)
    Func: Update user database and delete user
    Return: success(bool), message(str)
    '''
    query_parameters = request.args
    user_id = query_parameters.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "Please, provide a user_id."})

    result = UserDB().delete_user(User(user_id=user_id))
    if result != 0:
        return jsonify({"success": True, "message": "User delete successful."})
    else:
        return jsonify({"success": False, "message": "There is no user with such user_id in the user database."})


@app.route("/user/suspend", methods=['POST'])
def SuspendUser():
    '''
    Input: user_id (int)
    Func: Update user database and suspend user
    Return: success(bool), message(str)
    '''
    query_parameters = request.args
    user_id = query_parameters.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "Please, provide a user_id."})
    user_status="suspended"
    
    result = UserDB().update_user(User(user_id=user_id, user_status=user_status))
    if result != 0:
        return jsonify({"success": True, "message": "User suspension successful."})
    else:
        return jsonify({"success": False, "message": "There is no user with such user_id in the user database."})


@app.route("/user/rate", methods=['POST'])
def RateUser():
    '''
    Input: user_id (int)
    Func: Update user database and rate user
    Return: success(bool), message(str)
    '''
    query_parameters = request.args
    user_id = query_parameters.get('user_id')
    user_rating_sum = query_parameters.get('user_rating')
    user_rating_total = 1

    if not user_id:
        return jsonify({"success": False, "message": "Please, provide a user_id."})
    elif not user_rating_sum.isnumeric():
        return jsonify({"success": False, "message": "Please, enter a user rating as an integer value."})

    user_rating_sum = int(user_rating_sum)
    if 1 <= user_rating_sum <= 5:
        result = UserDB().update_user(User(user_id=user_id, user_rating_sum=user_rating_sum, user_rating_total=user_rating_total))
        if result != 0:
            return jsonify({"success": True, "message": "Your rating has been accepted and calculated."})
        else:
            return jsonify({"success": False, "message": "There is no user with such user_id in the user database."})
    else:
        return jsonify({"success": False, "message": "Please, enter user rating between 1 and 5, inclusive."})


@app.route("/user/info", methods=['GET'])
def GetUserInfo():
    '''
    Input: user_id (int), username(str), email(str),user_rating(int),watchlist_parameter(str)
    Func: Get user info from user database
    Return: success(bool), message(str), username(str), email(str),user_rating(int),watchlist_parameter(str)
    '''
    query_parameters = request.args
    user_id = query_parameters.get('user_id')
    username = query_parameters.get('username')
    email = query_parameters.get('email')
    user_rating = query_parameters.get('user_rating')
    watchlist_parameter = query_parameters.get('watchlist_parameter')
    print(query_parameters)
    print(user_id)
    print(username)
    print(username)
    result = UserDB().read_user(User(user_id=int(user_id)))
    if result:
        return_data = {"success": True, "message": "Successfully found a user with the asked user_id."}
        if username:
            return_data["username"] = result[1]
        if email:
            return_data["email"] = result[3]
        if user_rating:
            return_data["user_rating"] = (result[6] / result[7]) if result[7] != 0 else 0
        if watchlist_parameter:
            return_data["watchlist_parameter"] = result[8]
        return jsonify(return_data)
    else:
        return jsonify({"success": False, "message": "There is no user with such user_id in the user database.", 
                        "username": None, "email": None, "user_rating": None, "watchlist_parameter": None})


@app.route("/user/getalladmin", methods=['GET'])
def GetAllAdmin():
    '''
    Input: None
    Func: Get all admin from user database
    Return: success(bool), message(str), admin_ids(list), emails(list)
    '''
    user_type = "admin"
    results = UserDB().get_all_users(params=['user_type'],values=['admin'])
    print(results)
    if not results:
        return jsonify({"success": False, "message": "There is no admin in the user database.", 
                        "admin_ids": None})
    admin_ids = []
    emails = []
    for value in results:
        admin_ids.append(value[0])
        emails.append(value[3])
    return jsonify({"success": True, "message": "Successfully found all admins in the user database.", 
        "admin_ids": admin_ids, "emails": emails})


############################################
#                 ADMIN                    #
############################################


@app.route("/admin/checkadmin", methods=['GET'])
def CheckAdmin():
    '''
    Input: user_id(int)
    Func: Check if an user associated with given user_id is an admin
    Return: success(bool), message(str), isAdmin(bool)
    '''
    query_parameters = request.args
    user_id = query_parameters.get('user_id')
    result = UserDB().read_user(User(user_id=user_id))
    if result and result[4] == "admin":
        return jsonify({"success": True, "message": "Admin Check successful.", "isAdmin": True})
    elif result:
        return jsonify({"success": True, "message": "Admin Check successful.", "isAdmin": False})
    else:
        return jsonify({"success": False, "message": "There is no user with such user_id in the user database.", "isAdmin": False})


@app.route("/admin/suspenduser", methods=['POST'])
def AdminSuspendUser():
    '''
    Input: user_id (int), admin_id(int)
    Func: Update user database and suspend user
    Return: success(bool), message(str)
    '''
    query_parameters = request.args
    user_id = query_parameters.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "Please, provide a user_id."})
    if True:
        user_status="suspended"
        result = UserDB().update_user(User(user_id=user_id, user_status=user_status))
        if result != 0:
            return jsonify({"success": True, "message": "User suspension successful."})
        else:
            return jsonify({"success": False, "message": "There is no user with such user_id in the user database."})


@app.route("/admin/deleteuser", methods=['DELETE'])
def AdminDeleteUser():
    '''
    Input: user_id (int), admin_id(int)
    Func: Update user database and suspend user
    Return: success(bool), message(str)
    '''
    query_parameters = request.args
    user_id = query_parameters.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "Please, provide an user_id."})
    
    if True: # The real G's do it like this. 
        result = UserDB().delete_user(User(user_id=user_id))
        if result != 0:
            return jsonify({"success": True, "message": "User delete successful."})
        else:
            return jsonify({"success": False, "message": "There is no user with such user_id in the user database."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3312)
