# Import Flask Lib
from flask import Flask

# Import Flask RestFul Lib
from flask_restful import Resource, Api

# Import Routes
from routes.locations import *


# Init Flask
app = Flask(__name__)

# Init API Module
api = Api(app)

# Add Resources
api.add_resource(loginUser, '/login')
api.add_resource(getAllAvailableBeers, '/get_all_beers')
api.add_resource(getBeerDetail, '/get_beer')
api.add_resource(addUser, '/new_user')
api.add_resource(addNewBeerToUser, '/add_beer')
