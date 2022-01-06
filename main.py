from flask import Flask, request, jsonify, render_template, redirect
import uuid
import json

app = Flask(__name__)

class Item:
    def __init__(self, name, quantity, id = None):
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid1())
        self.name = name
        self.quantity = quantity
    
    def update_quantity(self, quantity):
        self.quantity = quantity

def dumper(obj):
    return obj.__dict__

items = [Item("apple", 5), Item("banana", 88)]

@app.route("/")
def home():
    return render_template("home.html", items=items)

@app.route("/add_item", methods=["POST"])
def add_item():
    name = request.form.get('name')
    quantity = request.form.get('quantity')
    items.append(Item(name, quantity))
    with open("items.json", "w") as f:
        json.dump(items, f, default=dumper)
    return redirect("/", code=302)

@app.route("/update_item/<id>", methods=["POST"])
def update_item(id):
    for item in items:
        if item.id == id:
            if request.form.get('operation') == 'Update':
                item.quantity = request.form.get('quantity')
            else:
                items.remove(item)
            with open("items.json", "w") as f:
                json.dump(items, f, default=dumper)
            break
    return redirect("/", code=302)

if __name__ == "__main__":
    with open('items.json') as f:
        items = json.load(f)
    for i in range(len(items)):
        items[i] = Item(**items[i])
    app.run()

