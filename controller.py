#!/usr/bin/env python
import json
from flask import Flask, render_template, request

from model import Meal, Product, Session
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)


##################### BOOKS #################################
@app.route("/")
def main_page():
	s = Session()
	meals = s.query(Meal).all()
	products = s.query(Product).all()
	s.close()

	return render_template('beta.html', meals=meals, products=products)


@app.route("/new_meal")
def new_meal():
	s = Session()
	products = s.query(Product).all()
	s.close()

	return render_template('edit_meal.html', other_products=products)


@app.route("/edit_meal/<_id>")
def edit_meal(_id):
	s = Session()
	b = s.query(Meal).filter_by(id=_id).first()

	current_products = b.products
	products = s.query(Product).all()

	other_products = []
	for a in products:
		if a not in b.products:
			other_products.append(a)
	s.close()

	return render_template('edit_meal.html', meal=b, other_products=other_products, current_products=current_products)

@app.route("/meal_save")
def new_meal_save():
	status, msg = True, ''

	b_name = request.args.get('name')

	s = Session()
	b = Meal(b_name)

	for key, val in request.args.items():
		if key == 'name':
			continue
		a = s.query(Product).filter_by(id=key).first()
		b.products.append(a)

	s.add(b)

	try:
		s.commit()
	except IntegrityError:
		status = False
		msg = 'The meal with name %s already exists' % b_name

	s.close()

	return json.dumps({'ok': status, 'msg': msg})


@app.route("/meal_save/<_id>")
def meal_save(_id):
	status, msg = True, ''
	b_name = request.args.get('name')

	s = Session()
	b = s.query(Meal).filter_by(id=_id).first()

	del b.products[:]

	for key, val in request.args.items():
		if key == 'name':
			continue
		a = s.query(Product).filter_by(id=key).first()
		b.products.append(a)

	b.name = b_name
	try:
		s.commit()
	except IntegrityError:
		status = False
		msg = 'The meal with name %s already exists' % b_name

	s.close()

	return json.dumps({'ok': status, 'msg': msg})


@app.route("/remove_meal")
def remove_meal():
	b_id   = request.args.get('id')

	s = Session()
	b = s.query(Meal).filter_by(id=b_id).first()

	s.delete(b)
	s.commit()
	s.close()

	return json.dumps({'ok': True, 'msg': ''})


@app.route("/search_meal")
def search_meal():
	return render_template('search_meal.html')


@app.route("/search_meal_go")
def search_meal_go():
	b_pattern = request.args.get('meal_pattern')
	a_pattern = request.args.get('product_pattern')

	s = Session()

	if not a_pattern:
		meals = s.query(Meal).filter(Meal.name.like('%' + b_pattern + '%'))
	else:
		meals = s.query(Meal).filter(and_(Meal.name.like('%' + b_pattern + '%'), \
		       Meal.products.any(Product.name.like('%' + a_pattern + '%'))))

	out = []
	for b in meals:
		out.append({'id': b.id, 'name': b.name})

	s.close()

	return json.dumps(out)


##################### AUTHORS #################################
@app.route("/new_product")
def new_product():
	return render_template('edit_product.html')


@app.route("/edit_product/<_id>")
def edit_product(_id):
	s = Session()
	a = s.query(Product).filter_by(id=_id).first()
	s.close()

	return render_template('edit_product.html', product=a)


@app.route("/product_save")
def new_product_save():
	status, msg = True, ''

	a_name = request.args.get('name')

	s = Session()
	s.add(Product(a_name))

	try:
		s.commit()
	except IntegrityError:
		status = False
		msg = 'The product with name %s already exists' % a_name

	s.close()

	return json.dumps({'ok': status, 'msg': msg})


@app.route("/product_save/<_id>")
def product_save(_id):
	status, msg = True, ''

	a_name = request.args.get('name')

	s = Session()
	a = s.query(Product).filter_by(id=_id).first()

	a.name = a_name

	try:
		s.commit()
	except IntegrityError:
		status = False
		msg = 'The product with name %s already exists' % a_name

	s.close()

	return json.dumps({'ok': status, 'msg': msg})

@app.route("/remove_product")
def remove_product():
	a_id   = request.args.get('id')

	s = Session()
	a = s.query(Product).filter_by(id=a_id).first()

	s.delete(a)
	s.commit()

	s.close()

	return json.dumps({'ok': True, 'msg': ''})



