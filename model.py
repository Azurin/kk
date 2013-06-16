#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *

import config


db = create_engine(config.app.db.url, echo_pool=True)

Session = sessionmaker(bind=db)
Base = declarative_base()


meals_products = Table(
	'meals_products', Base.metadata,
	Column('meal_id', Integer, ForeignKey('meals.id'), primary_key=True),
	Column('products_id', Integer, ForeignKey('products.id'), primary_key=True),
	Column('weight', Integer),
	)

"""
class Book(Base):
	__tablename__ = 'books'

	id = Column(Integer, primary_key=True)
	name = Column(String, unique=True)

	authors = relation('Author', secondary=books_authors, backref='wrote')

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return "<Book('%s')>" % (self.name)


class Author(Base):
	__tablename__ = 'authors'

	id = Column(Integer, primary_key=True)
	name = Column(String, unique=True)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return "<Author('%s')>" % (self.name)
"""

class Meal(Base):
	__tablename__ = 'meals'

	id = Column(Integer, primary_key=True)
	name = Column(String, unique=True)

	products = relation('Product', secondary=meals_products, backref='is_used_in')

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return "<Meal('%s')>" % (self.name)


class Product(Base):
	__tablename__ = 'products'

	id = Column(Integer, primary_key=True)
	name = Column(String, unique=True)
	prot = Column(Float)
	fats = Column(Float)
	hydr = Column(Float)
	kkal = Column(Integer)
	gi   = Column(Integer)

	def __init__(self, name, prot, fats, hydr, kkal, gi):
		self.name = name
		self.prot = prot
		self.fats = fats
		self.hydr = hydr
		self.kkal = kkal
		self.gi   = gi

	def __repr__(self):
		return "<Product('%s')>" % (self.name)



def createDB():
	'''Create DB if it doesn't exist'''
	if db.has_table('meals'):
		return

	Base.metadata.create_all(db)
	s = Session()

	m = Meal(u'Tuesday')
	p = Product(u'Яйцо куриное', 12.7, 10.9, 0.7, 157, 10)
	m.products.append(p)
	p = Product(u'Говядина отварная', 25.8, 16.8, 0, 254, 10)
	m.products.append(p)
	#import pdb; pdb.set_trace()
	s.add(m)

	"""
	a = Author('Mark Twain')
	b = Book('Tom Sawyer')
	b.authors.append(a)
	s.add(b)

	a = Author('Herbert Wells')
	gogol = Author('Nicolay Gogol')
	b = Book('Time Machine')
	b.authors.append(a)
	b.authors.append(gogol)
	s.add(b)

	b = Book('Taras Bulba')
	b.authors.append(gogol)
	s.add(b)
	"""
	
	s.commit()
	s.close()

