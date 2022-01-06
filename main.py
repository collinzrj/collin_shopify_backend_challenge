from flask import Flask, request, send_file, render_template, redirect
import uuid
import csv

app = Flask(__name__)

class Item:
    # generate a uuid when add new item
    # load old id when read from csv
    def __init__(self, name, quantity, id = None):
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid1())
        self.name = name
        self.quantity = quantity
    
    def update_quantity(self, quantity):
        self.quantity = quantity

items = []

@app.route("/")
def home():
    return render_template("home.html", items=items)

@app.route("/add_item", methods=["POST"])
def add_item():
    name = request.form.get('name')
    quantity = request.form.get('quantity')
    items.append(Item(name, quantity))
    # update csv when items are updated for data persistence
    update_csv()
    return redirect("/", code=302)

@app.route("/update_item/<id>", methods=["POST"])
def update_item(id):
    # iterate over items to find item for update
    for item in items:
        if item.id == id:
            # check update or remove according to button tapped
            if request.form.get('operation') == 'Update':
                item.quantity = request.form.get('quantity')
            else:
                items.remove(item)
            update_csv()
            break
    return redirect("/", code=302)

@app.route("/export")
def export():
    # send the csv file to user 
    return send_file('inventory.csv')

# update csv according to current items
def update_csv():
    with open('inventory.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['id', 'name', 'quantity'])
        for item in items:
            writer.writerow([item.id, item.name, item.quantity])

# read csv as items list
def read_csv():
    items = []
    with open('inventory.csv') as f:
        spamreader = csv.reader(f)
        for index, row in enumerate(spamreader):
            if index == 0:
                pass 
            else:
                items.append(Item(row[1], row[2], id=row[0]))
    return items

if __name__ == "__main__":
    items = read_csv()
    app.run()
