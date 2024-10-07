"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Menu, Dish, Ingredient, DishIngredient, Restriction, Preference
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

@api.route('/user', methods=['GET'])
def get_users():

    users = User.query.all()

    return jsonify([user.serialize() for user in users]), 200


@api.route('/menu', methods=['GET'])
def get_the_menu():

    food = Menu.query.all()

    return jsonify([menu.serialize() for menu in food]), 200

@api.route('/menu/<int:menu_id>/dish', methods=['GET'])
def get_menu_dishes(menu_id):
    response = {
        "data": None,
        "error": None,
    }

    statusCode = 200

    try:
        menu = Menu.query.get(menu_id)

        if not menu:
            response["error"] = "no menu with this id"
            return jsonify(response), 404
        
        dishes = menu.dishes

        response["data"] = [dish.serialize() for dish in dishes]
        
    except Exception as e: 
        response["error"] = "internal server error"
        statusCode = 500
        print(e)
        

    return jsonify(response), statusCode

@api.route('/dish', methods=['GET'])
def get_the_dish():

    plate = Dish.query.all()

    finishedPlates = [dish.serialize()for dish in plate]

    return jsonify({"data": finishedPlates}), 200

@api.route('/dish', methods=['POST'])
def create_dish():
    response = {
        "data": None,
        "error": None,
    }

    statusCode = 200

    data = request.get_json()

    dishName = data.get("name")
    menuId = data.get("menu_id")

    if not dishName or not menuId:
        response["error"] = "name or menu id not specified"
        return jsonify(response), 
    
    try: 
        dish = Dish(
            name=dishName, 
            menu_id=menuId
        )
        db.session.add(dish)
        db.session.commit()
        response["data"] = dish.serialize()

    except Exception as e: 
        response["error"] = "internal server error"
        statusCode = 500
        print(e)

    return jsonify(response), statusCode

@api.route('/ingredient', methods=['GET'])
def get_the_ingredient():

    ingredients = Ingredient.query.all()

    return jsonify([ingredient.seralize()for ingredient in ingredients]), 200

@api.route('/menu/<int:menu_id>/availability', methods=['GET'])
def get_menu_availability(menu_id):

    menu = Menu.query.get(menu_id)
    if menu is None:
        return jsonify({"error": "menu not found"}), 404
    
    availability = menu.availability

    return jsonify([i.seralize()for i in availability ]), 200
    


@api.route('/sign-up', methods=['POST'])
def handle_sign_up():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if User.query.filter_by(email = email).first():
        return jsonify({'msg': 'User already exists'}), 400
    
    hashed_password = generate_password_hash(password)
    new_user = User(email = email, password = hashed_password, is_active = True)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'msg':'User created successfully'}), 201

@api.route('/login', methods=['POST'])
def handle_log_in():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(email = email).first()
    if user is None or not check_password_hash(user.password, password):
        return jsonify({'msg': 'Invalid username or password'}), 401
    
    expiration = datetime.time.delta(days = 7)
    access_token = create_access_token(identity = user.email, expires_delta = expiration)
    return jsonify({'Token': access_token}), 200

@api.route('private', methods = ['GET'])
@jwt_required()
def private_route():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email = current_user).first()
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    
    return jsonify(logged_in_as = current_user), 200
    
