from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import recipe
from flask_bcrypt import Bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes.users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('recipes').query_db(query, data)
        all_users = []
        for row in results:
            all_users.insert(0, cls(row))
        return all_users

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First Name must be over 2 characters.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name must be over 2 characters.")
            is_valid = False
        if len(user['email']) == 0:
            flash("Email cannot be blank.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be over 8 characters.")
            is_valid = False
        if (user['confirm-password']) != (user['password']):
            flash("Password doesn't match.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.")
            is_valid = False
        return is_valid

    @staticmethod
    def user_exist(user):
        is_valid = True
        query = "SELECT * FROM recipes.users WHERE email = %(email)s;"
        results = connectToMySQL('recipes').query_db(query, user)
        if len(results) > 1:
            flash("Email already taken.")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM recipes.users WHERE email = %(email)s;"
        result = connectToMySQL('recipes').query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes.users WHERE id = %(id)s"
        results = connectToMySQL('recipes').query_db(query,data)
        return cls(results[0])