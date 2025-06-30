from flask import Flask, render_template, request, redirect, url_for, session
import json, random, os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session use

# Load recipes from JSON file
def load_recipes():
    if os.path.exists('recipes.json'):
        with open('recipes.json', 'r') as f:
            return json.load(f)
    return []

# Save recipes to JSON file
def save_recipes(data):
    with open('recipes.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    recipes = load_recipes()
    return render_template('index.html', recipes=recipes)

@app.route('/recipe/<int:id>')
def recipe(id):
    recipes = load_recipes()
    if 0 <= id < len(recipes):
        return render_template('recipe.html', recipe=recipes[id])
    return "Recipe not found", 404


@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        new_recipe = {
            "title": request.form['title'],
            "ingredients": request.form['ingredients'],
            "instructions": request.form['instructions'],
            "cuisine": request.form['cuisine'],
            "image": request.form['image'] or "https://source.unsplash.com/600x400/?food"
        }
        recipes = load_recipes()
        recipes.append(new_recipe)
        save_recipes(recipes)
        return redirect('/')
    return render_template('add_recipe.html')


@app.route('/save/<int:id>')
def save_to_favorites(id):
    if 'favorites' not in session:
        session['favorites'] = []
    if id not in session['favorites']:
        session['favorites'].append(id)
    return redirect(url_for('home'))

@app.route('/favorites')
def favorites():
    recipes = load_recipes()
    fav_ids = session.get('favorites', [])
    fav_recipes = [recipes[i] for i in fav_ids if i < len(recipes)]
    return render_template('index.html', recipes=fav_recipes)

@app.route('/random')
def random_recipe():
    recipes = load_recipes()
    if recipes:
        rand_id = random.randint(0, len(recipes) - 1)
        return redirect(url_for('recipe', id=rand_id))
    return "No recipes available", 404

if __name__ == '__main__':
    app.run(debug=True)
