  
import os
from flask_admin import Admin
from .models import db, User, Menu, Dish, MenuAvailability, Ingredient, DishIngredient, Restriction, Preference, UserRestrictions, UserPreferences
from flask_admin.contrib.sqla import ModelView

class ChildView(ModelView):
    column_display_pk = True # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = ('id', 'name', 'parent', 'first_name', 'last_name', 'email')

class MenuView(ModelView):
    column_display_pk = True # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = ('id', 'type', 'created_at')

class DishIngredientView(ModelView):
    column_display_pk = True # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = ('id', 'ingredient_order', 'dish_id', 'ingredient_id')

class DishRestrictionsView(ModelView):
    column_display_pk = True # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = ('id', 'dish_id', 'dish_name', 'dairy', 'eggs', 'seafood', 
                  'shellfish', 'wheat', 'soybeans', 'sesame', 
                  'tree_nuts', 'peanuts', 'pork', 'beef', 'alcohol')
    def _dish_name_formatter(view, context, model, name): return model.dish.name if model.dish else None
    column_formatters = {"dish_name": _dish_name_formatter}


class DishPreferencesView(ModelView):
    column_display_pk = True # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = ('id', 'dish_id', 'dish_name', 'no_raw_fish', 'vegan', 'mercury_sensitivity_pregnancy', 'keto_low_carb', 'egg_free', 'no_seaweed', 'vegetarian', 'gluten_intolerance', 'carnivore', 'lactose_intolerance', 'soy_free', 'low_sodium')
    def _dish_name_formatter(view, context, model, name): return model.dish.name if model.dish else None
    column_formatters = {"dish_name": _dish_name_formatter}

class UserRestrictionsView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = ('id', 'user_id', 'user_email', 'dairy', 'eggs', 'seafood', 
                  'shellfish', 'wheat', 'soybeans', 'sesame', 
                  'tree_nuts', 'peanuts', 'pork', 'beef', 'alcohol')
    # Add user email formatter
    def _user_email_formatter(view, context, model, name):
        return model.user.email if model.user else None
    column_formatters = {
        "user_email": _user_email_formatter
    }
     # Add sorting capabilities
    column_sortable_list = ['id', 'user_id', ('user_email', 'user.email')]
class UserPreferencesView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = ('id', 'user_id', 'user_email', 'no_raw_fish', 'vegan', 'mercury_sensitivity_pregnancy', 'keto_low_carb', 'egg_free', 'no_seaweed', 'vegetarian', 'gluten_intolerance', 'carnivore', 'lactose_intolerance', 'soy_free', 'low_sodium')
    # Add user email formatter
    def _user_email_formatter(view, context, model, name):
        return model.user.email if model.user else None
    column_formatters = {
        "user_email": _user_email_formatter
    }
     # Add sorting capabilities
    column_sortable_list = ['id', 'user_id', ('user_email', 'user.email')]

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ChildView(User, db.session))
    admin.add_view(MenuView(Menu, db.session))
    admin.add_view(ChildView(Dish, db.session))
    admin.add_view(ChildView(Ingredient, db.session))
    admin.add_view(ChildView(MenuAvailability, db.session))
    admin.add_view(DishIngredientView(DishIngredient, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
    admin.add_view(DishRestrictionsView(Restriction, db.session))
    admin.add_view(UserRestrictionsView(UserRestrictions, db.session))
    admin.add_view(DishPreferencesView(Preference, db.session))
    admin.add_view(UserPreferencesView(UserPreferences, db.session))