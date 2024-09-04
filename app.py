from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Load inventory data
def load_inventory():
    try:
        with open('inventory.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save inventory data
def save_inventory(data):
    with open('inventory.json', 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    inventory = load_inventory()
    return render_template('index.html', inventory=inventory)

@app.route('/add', methods=['POST'])
def add_item():
    name = request.form['name']
    quantity = int(request.form['quantity'])
    
    inventory = load_inventory()
    if name in inventory:
        inventory[name] += quantity
    else:
        inventory[name] = quantity
    
    save_inventory(inventory)
    return redirect(url_for('index'))

@app.route('/remove', methods=['POST'])
def remove_item():
    name = request.form['name']
    quantity = int(request.form['quantity'])
    
    inventory = load_inventory()
    if name in inventory:
        inventory[name] -= quantity
        if inventory[name] <= 0:
            del inventory[name]
    
    save_inventory(inventory)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)