"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Task
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200


@app.route('/todos/<username>', methods=['GET'])
def get_todos(username):
    task_results = Task.query.filter_by(username=username)
    serialized_tasks = list(map(lambda x: x.serialize(), task_results))
    # return results, jsonify() on results, status
    return jsonify({
        "message":f"These are the tasks available for user {username}",
        "task":serialized_tasks
    }), 200


@app.route('/todos/<username>', methods=['POST'])
def create_todos(username):
    body = request.get_json()
    user1 = Task(username=username, label=body["label"], done=body["done"])
    db.session.add(user1)
    db.session.commit()
    return jsonify("ok")

@app.route('/todos/<username>', methods=['PUT'])
def update_todos(username):
    pass

@app.route('/todos/<username>', methods=['DELETE'])
def delete_todos(username):
    pass



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

//