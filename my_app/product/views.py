#from my_app import app
from my_app import db
from flask import Blueprint, get_flashed_messages, flash, redirect, render_template, abort, request, url_for
from sqlalchemy import not_, or_
from my_app.product.model.products import PRODUCTS
from my_app.product.model.product import Product, ProductForm


product = Blueprint('product',__name__)


@product.route('/product')
@product.route('/product/<int:page>')
def index(page):
   return render_template('product/index.html', products=Product.query.paginate(page=1, per_page=5))

@product.route('/product/<int:id>')
def show(id):
    product = Product.query.get(id)
    if not product:
      abort(404)
    #consult
    return render_template('product/show.html', product= product)

@product.route('/product_delete/<int:id>', methods=['GET'])
def delete(id):
    product = Product.query.get(id)
    if not product:
      abort(404)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully")
    return redirect(url_for('product.index'))

@product.route('/product_create', methods=['POST', 'GET'])
def create():
    form = ProductForm(meta={'csrf':False})

    if form.validate_on_submit():
       #create
       register = Product(request.form['name'], request.form['price'])
       db.session.add(register)
       db.session.commit()
       flash("Product created successfully")
       return redirect(url_for('product.create'))
    if form.errors:
      flash(form.errors,'danger')
    
    return render_template('product/create.html', form=form)

@product.route('/product_update/<int:id>', methods=['POST', 'GET'])
def update(id):
    product = Product.query.get(id)
    if not product:
      abort(404)

    form = ProductForm(meta={'csrf':False})

    if request.method == 'GET':
      #view data
      form.name.data = product.name
      form.price.data = product.price
    if form.validate_on_submit():
      #update:
      product.name = form.name.data
      product.price = form.price.data
      db.session.add(product)
      db.session.commit()
      flash("Product updated successfully")
      return redirect(url_for('product.index', id=product.id))
    if form.errors:
      flash(form.errors,'danger')   
    return render_template('product/edit.html', product = product, form=form)


@product.route('/test')
def test():
    #consult
    #product_test =  Product.query.all() 
    #product_test =  Product.query.first()
    #product_test =  Product.query.limit(2).all()
    #product_test =  Product.query.get({"id":1})
    #product_test =  Product.query.filter(Product.id > 1).all()
    #product_test =  Product.query.filter_by(name ="Product4").all()
    #product_test =  Product.query.filter_by(name ="Product1", id = 1).all()
    #product_test =  Product.query.filter(Product.name.like('P%')).all()
    #product_test =  Product.query.filter(not_(Product.id > 1)).all()
    #product_test =  Product.query.filter(or_(Product.id > 1, Product.name=="Product1")).all()
    #product_test =  Product.query.order_by(Product.id.desc()).all()
    #print(product_test)

   #create
   #register_test = Product("Product5", 60.8)
   #db.session.add(register_test)
   #db.session.commit()

   #update
   #update_test =  Product.query.filter_by(name ="Product1", id = 1).first()
   #update_test.name = "Update Product1"
   #db.session.add(update_test)
   #db.session.commit()

   #delete
   #delete_test =  Product.query.filter_by(id = 1).first()
   #db.session.delete(delete_test)
   #db.session.commit()
   
   return "Test"

@product.route('/filter/<int:id>')
def filter(id):
   product = Product.query.get(id)
   return render_template('product/filter.html', product= product)