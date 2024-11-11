from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(100), unique=False, nullable=False)
    last_name = db.Column(db.String(100), unique=False, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    # ingredient_restrictions = db.relationship('Ingredient', secondary="restriction", back_populates="restricted_by_users")
    # ingredient_preferences = db.relationship('Ingredient', secondary="preference", back_populates="preferred_by_users")
    

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active,
            # "ingredient_restrictions": [ingredient.serialize() for ingredient in self.ingredient_restrictions],
            # "ingredient_preferences": [ingredient.serialize() for ingredient in self.ingredient_preferences],

        }
class UserRestrictions(db.Model):
    __tablename__ = "user_restrictions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    dairy = db.Column(db.Boolean, default=False, nullable=True)
    eggs = db.Column(db.Boolean, default=False, nullable=True)
    seafood = db.Column(db.Boolean, default=False, nullable=True)
    shellfish = db.Column(db.Boolean, default=False, nullable=True)
    wheat = db.Column(db.Boolean, default=False, nullable=True)
    soybeans = db.Column(db.Boolean, default=False, nullable=True)
    sesame = db.Column(db.Boolean, default=False, nullable=True)
    tree_nuts = db.Column(db.Boolean, default=False, nullable=True)
    peanuts = db.Column(db.Boolean, default=False, nullable=True)
    pork = db.Column(db.Boolean, default=False, nullable=True)
    beef = db.Column(db.Boolean, default=False, nullable=True)
    alcohol = db.Column(db.Boolean, default=False, nullable=True)
    user = db.relationship("User", backref="restrictions")

    def __repr__(self):
        return f'<UserRestrictions {self.id}:>'
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "dairy": self.dairy,
            "eggs": self.eggs,
            "seafood": self.seafood,
            "shellfish": self.shellfish,
            "wheat": self.wheat,
            "soybeans": self.soybeans,
            "sesame": self.sesame,
            "tree_nuts": self.tree_nuts,
            "peanuts": self.peanuts,
            "pork": self.pork,
            "beef": self.beef,
            "alcohol": self.alcohol
        }

class UserPreferences(db.Model):
    __tablename__ = "user_preferences"

    id = db.Column(db.Integer, primary_key=True)
    user_id =db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    no_raw_fish = db.Column(db.Boolean, default=False, nullable=True)
    vegan = db.Column(db.Boolean, default=False, nullable=True)
    mercury_sensitivity_pregnancy = db.Column(db.Boolean, default=False, nullable=True)
    keto_low_carb = db.Column(db.Boolean, default=False, nullable=True)
    egg_free = db.Column(db.Boolean, default=False, nullable=True)
    no_seaweed = db.Column(db.Boolean, default=False, nullable=True)
    vegetarian = db.Column(db.Boolean, default=False, nullable=True)
    gluten_intolerance = db.Column(db.Boolean, default=False, nullable=True)
    carnivore = db.Column(db.Boolean, default=False, nullable=True)
    lactose_intolerance = db.Column(db.Boolean, default=False, nullable=True)
    soy_free = db.Column(db.Boolean, default=False, nullable=True)
    low_sodium = db.Column(db.Boolean, default=False, nullable=True)
    user = db.relationship("User", backref="preferences")

    def __repr__(self):
            return f'<Preferences {self.id}:>'
    
    def serialize(self):
         return {
              "id": self.id,
              "user_id": self.user_id,
              "no_raw_fish": self.no_raw_fish,
              "vegan": self.vegan,
              "mercury_sensitivity_pregnancy": self.mercury_sensitivity_pregnancy,
              "keto_low_carb": self.keto_low_carb,
              "egg_free": self.egg_free,
              "no_seaweed": self.no_seaweed,
              "vegetarian": self.vegetarian,
              "gluten_intolerance": self.gluten_intolerance,
              "carnivore": self.carnivore,
              "lactose_intolerance": self.lactose_intolerance,
              "soy_free": self.soy_free,
              "low_sodium": self.low_sodium

         }

class Menu(db.Model):
    __tablename__ = "menu"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    type = db.Column(db.String(120), unique=True, nullable=False)
    availability = db.relationship('MenuAvailability')
    dishes = db.relationship("Dish")
    
    def __repr__(self):
        return f'<Menu {self.type}:>'
    
    def serialize(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "type": self.type,
            "availability": [availability.serialize() for availability in self.availability],
        }

class MenuAvailability(db.Model):
    __tablename__ = "menu_availability"

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(120), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    menu_id = db.Column(db.Integer,db.ForeignKey('menu.id'), nullable=False)

    def __repr__(self):
        return f'<MenuAvailability {self.day}: {self.start_time} to {self.end_time}>'
    

    def serialize(self):
        return {
            "id": self.id,
            "day": self.day,
            "start_time": str(self.start_time),
            "end_time": str(self.end_time),
            "menu_id": self.menu_id,
        }
    
class Dish(db.Model):
    __tablename__ = "dish"

    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    ingredients = db.relationship('Ingredient', secondary="dish_ingredient", back_populates="dishes", order_by="DishIngredient.ingredient_order")
    restriction = db.relationship('Restriction', uselist=False, backref="dish", lazy='joined')
    preference = db.relationship('Preference', uselist=False, backref="dish", lazy='joined')

    def __repr__(self):
        return f'<Dish {self.name}:>'
    
    def serialize(self):
        # sorted_ingredients = sorted(ingredients, key=lambda ingredient : ingredient["ingredient_order"])
        restriction_data = self.restriction.serialize() if self.restriction else None
        preference_data = self.preference.serialize() if self.preference else None
        return {
            "id": self.id,
            "menu_id": self.menu_id,
            "name": self.name,
            "created_at": self.created_at,
            # "ingredients": sorted_ingredients, 
            "ingredients": [ingredient.serialize() for ingredient in self.ingredients],
            "restriction": restriction_data,
            "preference": preference_data
        }

class Ingredient(db.Model):
    __tablename__ = "ingredient"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    calories = db.Column(db.Float(precision=2),unique=False, nullable=True)
    dishes = db.relationship('Dish', secondary="dish_ingredient", back_populates="ingredients")
    # restricted_by_users = db.relationship('User', secondary='restriction', back_populates="ingredient_restrictions")
    # preferred_by_users = db.relationship('User', secondary="preference", back_populates="ingredient_preferences")
    # add protein

    def __repr__(self):
            return f'<Ingredient {self.name}:>'
    
    def serialize(self):
            return {
            "id": self.id,
            "name": self.name,
            "calories": self.calories,
        }
    
class DishIngredient(db.Model):
    
    __tablename__ = "dish_ingredient"

    id = db.Column(db.Integer, primary_key=True)
    ingredient_order = db.Column(db.Integer, nullable=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)

    def __repr__(self):
            return f'<DishIngredient {self.id}:>'

class Restriction(db.Model):
    __tablename__ = "restriction"

    id = db.Column(db.Integer, primary_key=True)
    # user_id =db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    # ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    dairy = db.Column(db.Boolean, default=False, nullable=True)
    eggs = db.Column(db.Boolean, default=False, nullable=True)
    seafood = db.Column(db.Boolean, default=False, nullable=True)
    shellfish = db.Column(db.Boolean, default=False, nullable=True)
    wheat = db.Column(db.Boolean, default=False, nullable=True)
    soybeans = db.Column(db.Boolean, default=False, nullable=True)
    sesame = db.Column(db.Boolean, default=False, nullable=True)
    tree_nuts = db.Column(db.Boolean, default=False, nullable=True)
    peanuts = db.Column(db.Boolean, default=False, nullable=True)
    pork = db.Column(db.Boolean, default=False, nullable=True)
    beef = db.Column(db.Boolean, default=False, nullable=True)
    alcohol = db.Column(db.Boolean, default=False, nullable=True)

    def __repr__(self):
        return f'<Restriction {self.id}:>'
    
    def serialize(self):
        return {
            "id": self.id,
            "dish_id": self.dish_id,
            "dairy": self.dairy,
            "eggs": self.eggs,
            "seafood": self.seafood,
            "shellfish": self.shellfish,
            "wheat": self.wheat,
            "soybeans": self.soybeans,
            "sesame": self.sesame,
            "tree_nuts": self.tree_nuts,
            "peanuts": self.peanuts,
            "pork": self.pork,
            "beef": self.beef,
            "alcohol": self.alcohol
        }
     

class Preference(db.Model):
    __tablename__ = "preference"

    id = db.Column(db.Integer, primary_key=True)
    #  user_id =db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    #  ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    no_raw_fish = db.Column(db.Boolean, default=False, nullable=True)
    vegan = db.Column(db.Boolean, default=False, nullable=True)
    mercury_sensitivity_pregnancy = db.Column(db.Boolean, default=False, nullable=True)
    keto_low_carb = db.Column(db.Boolean, default=False, nullable=True)
    egg_free = db.Column(db.Boolean, default=False, nullable=True)
    no_seaweed = db.Column(db.Boolean, default=False, nullable=True)
    vegetarian = db.Column(db.Boolean, default=False, nullable=True)
    gluten_intolerance = db.Column(db.Boolean, default=False, nullable=True)
    carnivore = db.Column(db.Boolean, default=False, nullable=True)
    lactose_intolerance = db.Column(db.Boolean, default=False, nullable=True)
    soy_free = db.Column(db.Boolean, default=False, nullable=True)
    low_sodium = db.Column(db.Boolean, default=False, nullable=True)

    def __repr__(self):
            return f'<Preferences {self.id}:>'
    
    def serialize(self):
         return {
              "id": self.id,
              "dish_id": self.dish_id,
              "no_raw_fish": self.no_raw_fish,
              "vegan": self.vegan,
              "mercury_sensitivity_pregnancy": self.mercury_sensitivity_pregnancy,
              "keto_low_carb": self.keto_low_carb,
              "egg_free": self.egg_free,
              "no_seaweed": self.no_seaweed,
              "vegetarian": self.vegetarian,
              "gluten_intolerance": self.gluten_intolerance,
              "carnivore": self.carnivore,
              "lactose_intolerance": self.lactose_intolerance,
              "soy_free": self.soy_free,
              "low_sodium": self.low_sodium

         }
    

