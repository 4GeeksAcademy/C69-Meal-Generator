"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Menu, Dish, Ingredient, DishIngredient, Restriction, Preference, MenuAvailability, UserRestrictions, UserPreferences
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, decode_token, JWTManager
from api.email_util import send_reset_email

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
        return jsonify(response), 404 
    
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

@api.route('/menu/<int:menu_id>/availability', methods=['POST'])
def create_menu_availability(menu_id):
    response = {
        "data": None,
        "error": None,
    }
    
    statusCode = 200

    data = request.get_json()

    start_time = data.get("start_time")
    end_time = data.get("end_time")
    day = data.get("day")

    if not start_time or not end_time or not day:
        response["error"] = "start time or end time or day not specified"
        return jsonify(response), 404

    try:
        menuavailability = MenuAvailability(
            start_time=start_time,
            end_time=end_time,
            day=day,
            menu_id=menu_id,
        )
        db.session.add(menuavailability)
        db.session.commit()
        response["data"] = menuavailability.serialize()

    except Exception as e: 
        response["error"] = "internal server error"
        statusCode = 500
        print(e)

    return jsonify(response), statusCode

@api.route('/dish/<int:dish_id>/ingredient/<int:ingredient_id>/order', methods=['POST'])
def handle_ingredient_order(dish_id, ingredient_id):
    response = {
        "data": None,
        "error": None,
    }
    
    statusCode = 200
    data = request.get_json()

    order = data.get("order")

    if not order:
        response["error"] = "order not specified"
        return jsonify(response), 404
    
    try:
        dishingredient = db.session.execute(
            db.select(DishIngredient)
            .where(
                DishIngredient.dish_id==dish_id,
                DishIngredient.ingredient_id==ingredient_id,
            )
        ).scalar_one()
        dishingredient.ingredient_order = order
        db.session.commit()

    except Exception as e: 
        response["error"] = "internal server error"
        statusCode = 500
        print(e)

    return jsonify(response), statusCode

    


@api.route('/sign-up', methods=['POST'])
def handle_sign_up():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    first_name = request.json.get('first_name', "")
    last_name = request.json.get('last_name', "")
    if User.query.filter_by(email = email).first():
        return jsonify({'msg': 'User already exists'}), 400
    
    hashed_password = generate_password_hash(password)
    new_user = User(email = email, password = hashed_password, is_active = True, first_name = first_name, last_name = last_name)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'msg':'User created successfully'}), 201

@api.route('/log-in', methods=['POST'])
def handle_log_in():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(email = email).first()
    if user is None or not check_password_hash(user.password, password):
        return jsonify({'msg': 'Invalid username or password'}), 401
    
    expiration_delta = datetime.timedelta(days=7)
    access_token = create_access_token(identity = user.email, expires_delta = expiration_delta)
    return jsonify({'token': access_token, "user": user.serialize()}), 200

@api.route('/private', methods = ['GET'])
@jwt_required()
def private_route():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email = current_user).first()
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    
    return jsonify(logged_in_as = current_user), 200
    
@api.route('/forgot-password', methods=['POST'])
def handle_forgot_password():
    email = request.json.get('email', None)
    if not email:
        return jsonify({'msg': 'Email is required'}), 400

    user = User.query.filter_by(email=email).first()

    if user:
        expiration_delta = datetime.timedelta(minutes=30)
        reset_token = create_access_token(identity=user.id, expires_delta=expiration_delta)
        send_reset_email(user.email, reset_token)

    return jsonify({'msg': 'Please check your email to reset your password'}), 200


@api.route('/reset-password', methods= ['POST'])
def handle_reset_password():
    token = request.json.get('token', None)
    if not token:
        return jsonify({'msg':'Token is required'}), 400
    try:
        user_id = decode_token(token)
    except Exception:
        return jsonify({'msg': 'Invalid or expired token'}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg':'Invalid token or user not found'}), 404
    
    password = request.json.get('password', None)
    
    hashed_password = generate_password_hash(password)
    user.password = hashed_password
    
    db.session.commit()

    return jsonify({'msg': 'Your password has been successfully reset'}), 200

@api.route('/get-user-restrictions', methods= ['GET'])
@jwt_required()
def get_user_restrictions():
    user= User.query.filter_by(email=get_jwt_identity()).first()
    restrictions= UserRestrictions.query.filter_by(user_id = user.id).first()

    if not restrictions:
        new_restrictions = UserRestrictions(
            user_id = user.id,
            dairy = False,
            eggs = False,
            seafood = False,
            shellfish = False,
            wheat = False,
            soybeans = False,
            sesame = False,
            tree_nuts = False,
            peanuts = False,
            pork = False,
            beef = False,
            alcohol = False

        )

        db.session.add(new_restrictions)
        db.session.commit()
        return jsonify(new_restrictions.serialize()), 200
    
    return jsonify(restrictions.serialize()), 200

@api.route('/edit-user-restrictions', methods = ['PUT'])
@jwt_required()
def edit_user_restrictions():
    request_body = request.get_json()
    user= User.query.filter_by(email=get_jwt_identity()).first()
    restrictions= UserRestrictions.query.filter_by(user_id = user.id).first()

    if not restrictions:
        new_restrictions = UserRestrictions(**{**request_body, "user_id": user.id})
        db.session.add(new_restrictions)
        db.session.commit()
        return jsonify(new_restrictions.serialize()), 201
    
    for field in request_body: 
        if hasattr(restrictions, field):
            setattr(restrictions, field, request_body[field])

    try:
        db.session.commit()
        return jsonify(restrictions.serialize()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "error updating restrictions", "error": str(e)}), 400
    
@api.route('/get-user-preferences', methods=['GET'])
@jwt_required()
def get_user_preferences():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    preferences = UserPreferences.query.filter_by(user_id = user.id).first()

    if not preferences:
        new_preferences = UserPreferences(
            user_id = user.id,
            no_raw_fish = False,
            vegan = False,
            mercury_sensitivity_pregnancy = False,
            keto_low_carb = False,
            egg_free = False,
            no_seaweed = False,
            vegetarian = False,
            gluten_intolerance = False,
            carnivore = False,
            lactose_intolerance = False,
            soy_free = False,
            low_sodium = False,

        )

        db.session.add(new_preferences)
        db.session.commit()
        return jsonify(new_preferences.serialize()), 200
    
    return jsonify(preferences.serialize()), 200

@api.route('/edit-user-preferences', methods= ['PUT'])
@jwt_required()
def edit_user_preferences():
    request_body = request.get_json()
    user= User.query.filter_by(email=get_jwt_identity()).first()
    preferences= UserPreferences.query.filter_by(user_id = user.id).first()

    if not preferences:
        new_preferences = UserPreferences(**{**request_body, "user_id": user.id})
        try:
            db.session.add(new_preferences)
            db.session.commit()
            return jsonify({"success": True, "data": new_preferences.serialize()}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "error": str(e)}), 500
    for field in request_body: 
        if hasattr(preferences, field):
            setattr(preferences, field, request_body[field])

    try:
        db.session.commit()
        return jsonify({"success": True, "data": preferences.serialize()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "error updating ", "error": str(e)}), 400