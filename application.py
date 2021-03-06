from flask import Flask, render_template, url_for, request, redirect, \
                  flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"

# Connects to the database and creates a database session
engine = create_engine('sqlite:///catalog.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create an anti-forgery state token


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON API to view the catalog information


@app.route('/catalog.json')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(category=[c.serialize for c in categories])

# JSON API to view a single item

@app.route('/mainpage/<string:category>/<string:item>/item.json')
def itemJSON(category, item):
    categoryjson = session.query(Category).filter_by(name=category).one()
    itemjson = session.query(Item).filter_by(name=item, category_id=categoryjson.id).one()
    return jsonify(item=itemjson.serialize)

# Shows all the categories and the latest items added


@app.route('/')
@app.route('/mainpage/')
def mainPage():
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.id.desc()).limit(8)
    if 'username' not in login_session:
        return render_template('publicmainpage.html',
                               categories=categories, items=items)
    else:
        return render_template('mainpage.html',
                               categories=categories, items=items)

# Shows all the items of a selected category


@app.route('/mainpage/<string:category>')
def showCategory(category):
    categories = session.query(Category).all()
    selectedcat = session.query(Category).filter_by(name=category).first()
    items = session.query(Item).filter_by(category_id=selectedcat.id).all()
    if 'username' not in login_session:
        return render_template('publicshowcategory.html',
                               categoryToDisplay=selectedcat,
                               categories=categories, items=items)
    else:
        return render_template('showcategory.html',
                               categoryToDisplay=selectedcat,
                               categories=categories, items=items)

# Shows certain information about the selected item of certain category


@app.route('/mainpage/<string:category>/<string:item>')
def showItem(category, item):
    categoryselected = session.query(Category).filter_by(name=category).one()
    itemToShow = session.query(Item).filter_by(
                                     name=item,
                                     category_id=categoryselected.id).one()
    userid = itemToShow.user_id
    creator = getUserInfo(userid)
    if 'username' not in login_session or \
       creator.id != login_session['user_id']:
        return render_template('publicshowitem.html',
                               category=categoryselected, item=itemToShow,
                               creator=creator)
    else:
        return render_template('showitem.html',
                               category=categoryselected,
                               item=itemToShow, creator=creator)

# makes a new item of the selected category


@app.route('/mainpage/item/new', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        category_selected = session.query(Category).filter_by\
                            (name=request.form['category']).one()
        newItem = Item(name=request.form['name'],
                       user_id=login_session['user_id'],
                       description=request.form['description'],
                       price=request.form['price'],
                       category_id=category_selected.id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('mainPage'))
    else:
        return render_template('newitem.html')

# edits the details of the selected item


@app.route('/mainpage/<string:category>/<string:item>/edit',
           methods=['GET', 'POST'])
def editItem(category, item):
    category_selected = session.query(Category).filter_by(name=category).one()
    itemToEdit = session.query(Item).filter_by(
                 name=item, category_id=category_selected.id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if itemToEdit.user_id != login_session['user_id']:
        return "<script>function myFunction() \
                {alert('You are not authorized to delete this item. \
                Please create your own item in order \
                to delete.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            itemToEdit.name = request.form['name']
        if request.form['description']:
            itemToEdit.description = request.form['description']
        if request.form['price']:
            itemToEdit.price = request.form['price']
        session.add(itemToEdit)
        session.commit()
        return redirect(url_for('showCategory', category=category))
    else:
        return render_template('edititem.html',
                               category=category_selected, item=itemToEdit)
# deletes the selected item


@app.route('/mainpage/<string:category>/<string:item>/delete',
           methods=['GET', 'POST'])
def deleteItem(category, item):
    category_selected = session.query(Category).filter_by(name=category).one()
    itemToDelete = session.query(Item).filter_by(
                   name=item, category_id=category_selected.id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if itemToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() \
                {alert('You are not authorized to delete this item. \
                Please create your own item in order \
                to delete.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showCategory', category=category))
    else:
        return render_template('deleteitem.html',
                               category=category_selected, item=itemToDelete)

@app.route('/disconnect')
def disconnect():
    gdisconnect()
    del login_session['gplus_id']
    del login_session['access_token']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['provider']
    flash("You have successfully been logged out.")
    return redirect(url_for('mainPage'))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
