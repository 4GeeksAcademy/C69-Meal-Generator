import click
from api.models import db, User, Ingredient, Dish, Menu, Restriction, Preference, DishIngredient

"""
In this file, you can add as many commands as you want using the @app.cli.command decorator
Flask commands are usefull to run cronjobs or tasks outside of the API but sill in integration 
with youy database, for example: Import the price of bitcoin every night as 12am
"""
def setup_commands(app):
    
    """ 
    This is an example command "insert-test-users" that you can run from the command line
    by typing: $ flask insert-test-users 5
    Note: 5 is the number of users to add 
    """
    @app.cli.command("insert-test-users") # name of our command
    @click.argument("count") # argument of out command
    def insert_test_users(count):
        print("Creating test users")
        for x in range(1, int(count) + 1):
            user = User()
            user.email = "test_user" + str(x) + "@test.com"
            user.password = "123456"
            user.is_active = True
            db.session.add(user)
            db.session.commit()
            print("User: ", user.email, " created.")

        print("All test users created")

    @app.cli.command("insert-test-data")
    def insert_test_data():
        pass


    @app.cli.command("populate-menus")
    def generate_menus_list():
        menu_list = [
            {
                "id": "1",
                "type": "Dinner",
            },
            {
                "id": "2",
                "type": "Brunch",
            },
        ]

        for menu in menu_list:
            new_menu = Menu(
                id=menu['id'],
                type=menu['type'],
            )

            db.session.add(new_menu)
            db.session.commit()

    @app.cli.command("populate-ingredients")   
    def generate_ingredients_list(): 
        ingredient_list = [
            {
                "id": "13",
                "name": "Grilled miso marinated salmon",
            },
            {
                "id": "14", 
                "name": "Shiitake mushrooms",
            },
            {
                "id": "15",
                "name": "Shimeji mushrooms",
            },
            {
                "id": "16",
                "name": "Maitake mushrooms"
            },
            {
                "id": "17",
                "name": "Grilled black cod	",
            },
            {
                "id": "18",
                "name": "Yuzu soy sauce",
            },
            {
                "id": "19",
                "name": "Sweet soy sauce soup",
            },
            {
                "id": "20",
                "name": "Washu beef",
            },
            {
                "id": "21",
                "name": "Tofu",
            },
            {
                "id": "22",
                "name": "Nappa cabbage",
            },
            {
                "id": "23",
                "name": "Burdock",
            },
            {
                "id": "24",
                "name": "Carrot",
            },
            {
                "id": "25",
                "name": "Scallion",
            },
            {
                "id": "26",
                "name": "A5 wagyu beef",
            },
            {
                "id": "27",
                "name": "Vegetables",
            },
            {
                "id": "28",
                "name": "Wasabi",
            },
            {
                "id": "29",
                "name": "Yuzu kosho",
            },
            {
                "id": "30",
                "name": "Miso",
            },
            {
                "id": "31",
                "name": "Soy Sauce",
            },
            {
                "id": "32",
                "name": "Grilled fish collar of the day",
            },
            {
                "id": "33",
                "name": "Rice",
            },
            {
                "id": "34",
                "name": "Grilled eel served with sweet soy sauce",
            },
            {
                "id": "35",
                "name": "Buckwheat noodle soup with grilled duck breast",
            },
            {
                "id": "36",
                "name": "Yuzu Zest",
            },
            {
                "id": "37",
                "name": "Assorted Vegtables",
            },
            {
                "id": "38",
                "name": "Shrimp tempura",
            },
            {
                "id": "39",
                "name": "Grilled free-range organic chicken thigh",
            },
            {
                "id": "40",
                "name": "Sliced wagyu beef",
            },
            {
                "id": "41",
                "name": "Duck sauce",
            },
        ]

        for ingredient in ingredient_list:
            new_ingredient=Ingredient(
                id=ingredient['id'],
                name=ingredient['name']
            )
            db.session.add(new_ingredient)
            db.session.commit()


    @app.cli.command("populate-dishes")  
    def populate_dishes_command():
        """Command wrapper for generate_dishes_list""" 
        generate_dishes_list()

    def generate_dishes_list(): 
        dish_list = [
            {
                "id": "12",
                "name": "Salmon and Mushroom Toban Yaki",
                "ingredients": ["Grilled miso marinated salmon", "Maitake mushrooms", "Shiitake mushrooms", "Shimeji mushrooms"],
                "created_at": "2024-10-11 23:52:53",
                "menu_id": "1",
                "restrictions": {"seafood": True, "soybeans": True},
                "preferences": {"no_raw_fish": True, "vegan": True, "vegetarian": True, "carnivore": True, "low_sodium": True, "soy_free": True}
            },
            {
                "id": "13",
                "name": "Gindara Yuan Yaki",
                "ingredients": ["Grilled black cod", "Yuzu soy sauce"],
                "created_at": "2024-10-11 23:52:53",
                "menu_id": "2",
                "restrictions": {"seafood": True, "soybeans": True},
                "preferences": {"no_raw_fish": True, "vegan": True, "vegetarian": True, "carnivore": True, "low_sodium": True, "soy_free": True}
            },
            {
                "id": "14",
                "name": "Dish Testing 1",
                "ingredients": ["Grilled black cod", "Yuzu soy sauce"],
                "created_at": "2024-10-11 23:52:53",
                "menu_id": "2",
                "restrictions": {},
                "preferences": {}
            },
            
        ]

        # for dish in dish_list:
        #     new_dish=Dish(
        #         id=dish['id'],
        #         name=dish['name'],
        #         ingredients=dish['ingredients'],
        #         created_at=dish['created_at'],
        #         menu_id=dish['menu_id'],
        #     )

        #     for ingredient_name in dish['ingredients']:
        #         ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
        #         if ingredient:
        #             new_dish.ingredients.append(ingredient)

        for dish in dish_list:
            new_dish = Dish(
                id=dish['id'],
                name=dish['name'],
                created_at=dish['created_at'],
                menu_id=dish['menu_id'],
            )

            for ingredient_name in dish['ingredients']:
                ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
                if ingredient:
                    new_dish.ingredients.append(ingredient)
                else:
                    new_ingredient = Ingredient(name=ingredient_name)
                    db.session.add(new_ingredient)
                    db.session.commit()
                    db.session.refresh(new_ingredient)
                    new_dish.ingredients.append(new_ingredient)
            
            db.session.add(new_dish)
            db.session.commit()
            db.session.refresh(new_dish)

            dish_restriction = Restriction(**{**dish['restrictions'], "dish_id":new_dish.id})
            db.session.add(dish_restriction)
            db.session.commit()

            dish_preference = Preference(**{**dish['preferences'], "dish_id":new_dish.id})
            db.session.add(dish_preference)
            db.session.commit()

    @app.cli.command("reset-dishes")
    def reset_dishes():
        """Delete all dishes and their restrictions, then repopulate them"""
        try:
            # First delete all restrictions (due to foreign key constraints)
            print("Deleting existing restrictions...")
            Restriction.query.delete()
            
            # Then delete all dish_ingredient associations
            print("Deleting dish-ingredient associations...")
            DishIngredient.query.delete()
            
            # Then delete all dishes
            print("Deleting existing dishes...")
            Dish.query.delete()
            
            db.session.commit()
            print("All dishes and related data deleted successfully")

            # Call the populate-dishes command
            print("Repopulating dishes...")
            generate_dishes_list()
            
            print("Dishes reset and repopulated successfully!")

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            db.session.rollback()
            raise e