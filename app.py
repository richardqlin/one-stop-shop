from flask import Flask

from flask import *
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo

from bson.objectid import ObjectId
app = Flask('One-Stop-Shop')



app.config['SECRET_KEY'] ='sOmE_rAnDom_woRd'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/one-stop-ship-db'

Bootstrap(app)
mongo = PyMongo(app)


@app.route('/',methods=['GET','POST'])
def stop_one():
    return render_template('home.html')

@app.route('/add', methods=['GET','POST'])
def add():

    if request.method == 'GET':
        print('get')
        return render_template('add-product.html')
    elif request.method == 'POST':
        doc = {}
        #print(request.form)
        for item in request.form:
            doc[item] = request.form[item]
        mongo.db.products.insert_one(doc)
        return redirect('/')


@app.route('/buy', methods = ['GET','POST'])
def buy():
    if request.method == 'GET':
        session['cart-items'] = {}
        found_products = mongo.db.products.find()
        #print(found_products)
        return render_template('buy-products.html', products = found_products)
    elif request.method  == 'POST':
        doc ={}

        data = request.form
        print('data',data)
        for item in request.form:
            # Only adding those products whose chosen quantity is non zero
            if int(request.form[item])!=0:
                doc[item] = request.form[item]
        session['cart-items'] = doc
        return redirect('/checkout')

@app.route('/checkout')

def checkout():
    total = 0
    cart_items = []
    stored_info = session['cart-items']
    for ID in stored_info:
        found_item = mongo.db.products.find_one({'_id': ObjectId(ID)})
        found_item['quantity_limited'] = stored_info[ID]
        found_item['item_total'] = int(found_item['price'])*int(found_item['quantity_limited'])
        cart_items.append(found_item)
        total += found_item['item_total']

    return render_template('checkout.html', products = cart_items,total=total)



app.run(debug=True)