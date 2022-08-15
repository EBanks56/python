from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.cook_date = data['cook_date']
        self.cook_time = data['cook_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes.recipes (name, description, instructions, cook_date, cook_time, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(cook_date)s, %(cook_time)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes.recipes;"
        results = connectToMySQL('recipes').query_db(query)
        all_recipes = []
        for row in results:
            print(row['cook_date'])
            all_recipes.insert(0, cls(row))
        return all_recipes

    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes.recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, cook_date=%(cook_date)s, cook_time=%(cook_time)s, updated_at=NOW(), WHERE id=%(id)s"
        return connectToMySQL('recipes').query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes.recipes WHERE id=%(id)s"
        return connectToMySQL('recipes').query_db(query,data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Recipe name must be over 3 characters.")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Recipe description must be over 3 characters.")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Recipe instructions must be over 3 characters.")
            is_valid = False
        if recipe['cook_date'] == "":
            flash("Date Cooked field is required.")
            is_valid = False
        if recipe['cook_time'] == "":
            flash("Under 30 minutes field is required.")
            is_valid = False
        return is_valid
