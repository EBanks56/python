from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/new/recipe')
def newRecipe():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template('create.html', user=User.get_one(data))

@app.route('/create/recipe', methods = ['POST'])
def createPost():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'cook_date': request.form['cook_date'],
        'cook_time': request.form['cook_time'],
        'user_id': session['user_id']
    }
    Recipe.save(data)
    return redirect('/home')

@app.route('/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("edit.html", recipe=Recipe.get_one_recipe(data), user=User.get_one(user_data))

@app.route('/update', methods=['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/edit/<int:id>')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'cook_date': request.form['cook_date'],
        'cook_time': request.form['cook_time'],
        'id': request.form['id']
    }
    Recipe.update(data)
    return redirect('/home')

@app.route('/view/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("view.html", recipe=Recipe.get_one_recipe(data), user=User.get_one(user_data))

@app.route('/delete/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Recipe.delete(data)
    return redirect('/home')
