from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
from sqlalchemy import or_, and_
import time
import datetime
import json
from operator import  itemgetter,attrgetter

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)


@app.route('/users', methods=['GET'])
def get_users():
    session = db.getSession(engine)
    dbResponse = session.query(entities.User)
    data = []
    for user in dbResponse:
        data.append(user)
    message = {'data': data}
    return Response(json.dumps(message, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { 'status': 404, 'message': 'Not Found'}
    return Response(message, status=404, mimetype='application/json')

@app.route('/users', methods = ['POST'])
def create_user():
    c = json.loads(request.form['values'])
    user = entities.User(
        username=c['username'],
        name=c['name'],
        fullname=c['fullname'],
        password=c['password']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return 'Created User'

@app.route('/messages', methods = ['POST'])
def create_message():
    c =  json.loads(request.form['values'])
    message = entities.Message(
        content=c['content'],
        user_from_id=c['user_from_id'],
        user_to_id=c['user_to_id'],
    )
    session = db.getSession(engine)
    session.add(message)
    session.commit()
    return 'Created Message'


@app.route('/messagesjs', methods = ['POST'])
def create_message_with_js():
    c =  json.loads(request.data)
    message = entities.Message(
        content=c['content'],
        user_from_id=c['user_from_id'],
        user_to_id=c['user_to_id'],
    )
    session = db.getSession(engine)
    session.add(message)
    session.commit()
    return 'Created Message'

@app.route('/authenticate', methods = ["POST"])
def authenticate():
    message = json.loads(request.data)
    username = message['username']
    password = message['password']
    # 2. look in database
    db_session = db.getSession(engine)
    try:
        user = db_session.query(entities.User
                                ).filter(entities.User.username == username
                                         ).filter(entities.User.password == password
                                                  ).one()
        session['logged_user'] = user.id
        message = {'message': 'Authorized', 'user_id':user.id, 'username':user.username}
        message1 = json.dumps(message, cls=connector.AlchemyEncoder)
        return Response(message1, status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        message1 = json.dumps(message, cls=connector.AlchemyEncoder)
        return Response(message1, status=401, mimetype='application/json')



@app.route('/users', methods = ['PUT'])
def update_user():
    session = db.getSession(engine)
    id = request.form['key']
    user = session.query(entities.User).filter(entities.User.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(user, key, c[key])
    session.add(user)
    session.commit()
    return 'Updated User'

@app.route('/users', methods = ['DELETE'])
def delete_user():
    id = request.form['key']
    session = db.getSession(engine)
    users = session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        session.delete(user)
    session.commit()
    return "Deleted User"


@app.route('/messages', methods = ['DELETE'])
def delete_message():
    id = request.form['key']
    session = db.getSession(engine)
    messages = session.query(entities.Message).filter(entities.Message.id == id)
    for message in messages:
        session.delete(message)
    session.commit()
    return "Deleted Message"


@app.route('/messages', methods = ['PUT'])
def update_message():
    session = db.getSession(engine)
    id = request.form['key']
    message = session.query(entities.Message).filter(entities.Message.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(message, key, c[key])
    session.add(message)
    session.commit()
    return 'Updated Message'\

@app.route('/messages', methods = ['GET'])
def get_messages():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Message)
    data = []
    for message in dbResponse:
        data.append(message)
    return Response (json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/chats/<user_id>', methods = ['GET'])
def get_chats(user_id):
    sessiondb = db.getSession(engine)
    data = []
    users=sessiondb.query(entities.User).filter(entities.User.id != user_id)
    for user in users:
        data.append(user)
    return Response(json.dumps({'response' : data}, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/chats/<user_from_id>/<user_to_id>', methods = ['GET'])
def get_chat(user_from_id, user_to_id):
    session = db.getSession(engine)
    messages = session.query(entities.Message).filter(
            entities.Message.user_from_id == user_from_id).filter(entities.Message.user_to_id==user_to_id)

    messages2 = session.query(entities.Message).filter(
            entities.Message.user_from_id == user_to_id).filter(entities.Message.user_to_id==user_from_id)

    data = []
    for message in messages:
        data.append(message)
    for message2 in messages2:
        data.append(message2)
    data = sorted(data,key=attrgetter('sent_on'),reverse=False)

    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/messages/<user_from_id>/and/<user_to_id>', methods = ['GET'])
def get_mobile_messages(user_from_id, user_to_id):
    db_session = db.getSession(engine)
    chats = db_session.query(entities.Message).filter(
        or_(
            and_(entities.Message.user_from_id == user_from_id, entities.Message.user_to_id == user_to_id),
            and_(entities.Message.user_from_id == user_to_id, entities.Message.user_to_id == user_from_id),
        )
    )
    data = []
    for chat in chats:
        data.append(chat)
    message = {'response' : data}
    return Response(json.dumps(message, cls=connector.AlchemyEncoder), status=200, mimetype='application/json')

@app.route('/current', methods = ['GET'])
def current():
    sessiondb = db.getSession(engine)
    user = sessiondb.query(entities.User).filter(entities.User.id == session['logged']).first()
    js = json.dumps(user, cls=connector.AlchemyEncoder)
    return Response(js, status=200, mimetype='application/json')

@app.route('/messages/postMessage', methods = ['POST'])
def new_message():
    try:
        c = json.loads(request.data)
        message = entities.Message(
            content=c['content'],
            user_from_id=c['user_from_id'],
            user_to_id=c['user_to_id']
        )
        session = db.getSession(engine)
        session.add(message)
        session.commit()
        message = {'message': 'Authorized'}
        return Response(message, status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')

@app.route('/users/allExcept/<id>', methods = ['GET'])
def get_user_allExceptMobile(id):
    db_session = db.getSession(engine)
    try:
        dbResponse = db_session.query(entities.User).filter(entities.User.id != id)
        data = []
        for user in dbResponse:
            data.append(user)
        message = {'data': data}
        return Response(json.dumps(message, cls=connector.AlchemyEncoder), status=200, mimetype='application/json')
    except Exception:
        message = { 'status': 404, 'message': 'Not Found'}
        return Response(message, status=404, mimetype='application/json')

@app.route('/postLearn', methods = ['POST'])
def new_Learn():
    try:
        c = json.loads(request.data)
        message = entities.Learn(
            user_from_id=c['user_from_id'],
            user_from_name=c['user_from_name'],
            Tema=c['tema'],
            Curso=c['curso'],
            Lugar=c['lugar'],
            Hora=c['hora'],
            Tiempo=c['tiempo']
        )
        session = db.getSession(engine)
        session.add(message)
        session.commit()
        message = {'message': 'Authorized'}
        return Response(message, status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')

@app.route('/getLearn', methods=['GET'])
def get_Learn():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Learn)
    data = []
    for learn in dbResponse:
        data.append(learn)
    message = {'data': data}
    return Response(json.dumps(message, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/postTeach', methods = ['POST'])
def new_Teach():
    try:
        c = json.loads(request.data)
        message = entities.Teach(
            user_from_id_t=c['user_from_id_t'],
            name_t=c['name_t'],
            curso_t=c['curso_t']
        )
        session = db.getSession(engine)
        session.add(message)
        session.commit()
        message = {'message': 'Authorized'}
        return Response(message, status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')

@app.route('/getTeach', methods=['GET'])
def get_Teach():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Teach)
    data = []
    for teach in dbResponse:
        data.append(teach)
    message = {'data': data}
    return Response(json.dumps(message, cls=connector.AlchemyEncoder), mimetype='application/json')

if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=5000, threaded=True, host=('127.0.0.1'))