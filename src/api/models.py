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
            # do not serialize the password, its a security breach
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
    
    # class Dish(db.Model):
    #     __tablename__ = "dish"

    #     id = db.Column(db.Integer, primary_key=True)