from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

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
    
    def __repr__(self):
        return f'<Menu {self.type}:>'
    
    def serialize(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "type": self.type,
        }

class MenuAvailability(db.Model):
    __tablename__ = "menu_availability"

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(120), unique=True, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    menu_id = db.Column(db.Integer,db.ForeignKey('menu.id'))

    def __repr__(self):
        return f'<MenuAvailability {self.day}: {self.start_time} to {self.end_time}>'
    

    def serialize(self):
        return {
            "id": self.id,
            "day": self.day,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "menu_id": self.menu_id,
        }
    
    class Dish(db.Model):
        __tablename__ = "dish"

        id = db.Column(db.Integer, primary_key=True)
        menu_id = db.Column(db.Integer,db.ForeignKey('menu.id'))
        name = db.Column(db.String(120), unique=True, nullable=False)
        created_at = db.Column(db.DateTime, nullable=False, default=func.now())

        def __repr__(self):
            return f'<Dish {self.type}:>'
        
        def serialize(self):
            return {
            "id": self.id,
            "menu_id": self.menu_id,
            "name": self.name,
            "created_at": self.created_at,
        }

class Ingredient(db.Model):
    __tablename__ = "ingredient"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    calories = db.Column(db.Float(precision=2),unique=True, nullable=False)

    def __repr__(self):
            return f'<Ingredient {self.type}:>'
    
    def serialize(self):
            return {
            "id": self.id,
            "name": self.name,
            "calories": self.calories,
        }
    
class DishIngredient(db.Model):
    
    __tablename__ = "dish_ingredient"

    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer,db.ForeignKey('dish.id'))
    ingredient_id = db.Column(db.Integer,db.ForeignKey('ingredient.id'))

    def __repr__(self):
            return f'<DishIngredient {self.type}:>'
    
    def serialize(self):
            return {
            "id": self.id,
            "dish_id": self.dish_id,
            "ingredient_id": self.ingredient_id,
        }
