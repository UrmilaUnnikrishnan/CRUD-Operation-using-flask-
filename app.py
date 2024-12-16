from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Setup SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications

# Initialize the database
db = SQLAlchemy(app)

# Define the Item model (representing the 'items' table in the database)
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Item {self.name}>'

    # Method to convert the item to a dictionary (for JSON response)
    def to_dict(self):
        return {"id": self.id, "name": self.name}



# Route to get all items (GET)
@app.route('/api/items', methods=['GET'])
def get_items():
    items = Item.query.all()  # Get all items from the database
    return jsonify([item.to_dict() for item in items])  # Return items as JSON

# Route to add a new item (POST)
@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json()  # Get the JSON data from the request
    name = data.get('name')  # Extract the 'name' from the request data

    if name:
        new_item = Item(name=name)  # Create a new Item instance
        db.session.add(new_item)  # Add the new item to the session
        db.session.commit()  # Commit the transaction to the database
        return jsonify(new_item.to_dict()), 201  # Return the created item as JSON with 201 status

    return jsonify({"error": "Name is required"}), 400  # Return error if 'name' is not provided

# Route to edit an item (PUT)
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)  # Fetch the item by ID
    data = request.get_json()  # Get the JSON data from the request
    name = data.get('name')  # Extract the 'name' from the request data

    if name:
        item.name = name  # Update the item's name
        db.session.commit()  # Commit the changes to the database
        return jsonify(item.to_dict())  # Return the updated item as JSON

    return jsonify({"error": "Name is required"}), 400  # Return error if 'name' is not provided

# Route to delete an item (DELETE)
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)  # Fetch the item by ID
    db.session.delete(item)  # Delete the item
    db.session.commit()  # Commit the deletion to the database
    return jsonify({"message": "Item deleted successfully"}), 200  # Return success message

# Ensure that the database and tables are created when the app starts
@app.before_request
def create_tables():
    db.create_all()

# Create the database tables (if they don't exist already)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=9090)
