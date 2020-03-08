# Import Flask Lib
from flask import Flask, abort, request

# Import Flask RestFul Lib
from flask_restful import Api

# Import Routes
from routes.locations import *


# Init Flask
app = Flask(__name__)

# Init API Module
api = Api(app)


# Add Resources
api.add_resource(Home, '/')
api.add_resource(getAllAvailableBeers, '/get_all_beers')
api.add_resource(getBeerDetail, '/get_beer')
api.add_resource(addNewBeerToClient, '/add_beer')
