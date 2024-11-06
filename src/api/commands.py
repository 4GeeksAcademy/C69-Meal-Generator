
import click
from api.models import db, User, Ingredient

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
