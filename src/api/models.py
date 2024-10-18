from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    ingredident_restrictions = db.relationship('Ingredient', secondary="restriction", back_populates="restricted_by_users")
    ingredient_preferences = db.relationship('Ingredient', secondary="preference", back_populates="preferred_by_users")
    

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
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

    def __repr__(self):
        return f'<Dish {self.name}:>'
    
    def serialize(self):
        ingredients = [ingredient.serialize() for ingredient in self.ingredients]
        # sorted_ingredients = sorted(ingredients, key=lambda ingredient : ingredient["ingredient_order"])
        return {
        "id": self.id,
        "menu_id": self.menu_id,
        "name": self.name,
        "created_at": self.created_at,
        # "ingredients": sorted_ingredients, 
        "ingredients": ingredients,
    }

class Ingredient(db.Model):
    __tablename__ = "ingredient"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    calories = db.Column(db.Float(precision=2),unique=False, nullable=False)
    dishes = db.relationship('Dish', secondary="dish_ingredient", back_populates="ingredients")
    restricted_by_users = db.relationship('User', secondary='restriction', back_populates="ingredident_restrictions")
    preferred_by_users = db.relationship('User', secondary="preference", back_populates="ingredient_preferences")
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
     user_id =db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
     ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)

     def __repr__(self):
            return f'<Restriction {self.id}:>'
     

class Preference(db.Model):
     __tablename__ = "preference"

     id = db.Column(db.Integer, primary_key=True)
     user_id =db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
     ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)

     def __repr__(self):
            return f'<Preferences {self.id}:>'
    

