from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        message_dict = [message.to_dict() for message in Message.query.all()]
        return make_response(message_dict, 200)
    elif request.method == 'POST':
        message = request.json
        new_message = Message(
            body = message.get("body"),
            username = message.get("username")
        )
        db.session.add(new_message)
        db.session.commit()
        response = new_message.to_dict()
        return make_response(response, 200)
        
@app.route('/messages/<int:id>', methods= ['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if request.method == 'PATCH':
        for attr in request.json:
            setattr(message, attr, request.json.get(attr))
        response = message.to_dict()
        status = 200
        

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        response = {}
        status = 200
        
    return make_response(response, status)

if __name__ == '__main__':
    app.run(port=5555)
