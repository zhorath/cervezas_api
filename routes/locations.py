# Import Resource from Flask Restful
from flask_restful import Resource

# Import Flask
from flask import request

# Import DB Function
from database.functions import getAllBeers, getBeerByUser, newBeerToUser, newUser


class getAllAvailableBeers(Resource):

    def get(self):
        return {
            "status": "Success",
            "is_successful": True,
            "data": getAllBeers()
        }


class getBeerDetail(Resource):

    def post(self):
        data = request.json

        if data is None:
            return {
                "status": "Error",
                "is_successful": False,
                "error_message": "Request body cannot be null"
            }
        if 'beer_id' not in data:
            return {
                "status": "Error",
                "is_successful": False,
                "error_message": "Parameter beer_id is missing"
            }
        if 'user_id' not in data:
            return {
                "status": "Error",
                "is_successful": False,
                "error_message": "Parameter user_id is missing"
            }

        return {
            "status": "Success",
            "is_successful": True,
            "data": getBeerByUser(
                data['beer_id'],
                data['user_id']
            )
        }


class addNewBeerToUser(Resource):

    def post(self):
        data = request.json

        if data is None:
            return {
                "status": "Error",
                "is_successful": False,
                "error_message": "Request body cannot be null"
            }
        if 'beer_id' not in data:
            return {
                "status": "Error",
                "is_successful": False,
                "error_message": "Parameter beer_id is missing"
            }
        if 'user_id' not in data:
            return {
                "status": "Error",
                "is_successful": False,
                "error_message": "Parameter user_id is missing"
            }

        try:
            newBeerToUser(
                data['beer_id'],
                data['user_id']
            )
            return {"status": "Update successfully", "is_sucess": True}
        except Exception as e:
            return {"status": "Error", "is_sucess": False, "error_message": str(e)}


class addUser(Resource):

    def post(self):
        data = request.json

        if data is None:
            return {
                "status": "Error",
                "is_successful": False,
                "error_message": "Request body cannot be null"
            }
        if 'username' not in data:
            return {
                "status": "Error",
                "is_successful": False,
                "error_message": "Parameter username is missing"
            }
        if 'password' not in data:
            return {
                "status": "Error",
                "is_successful": False,
                "error_message": "Parameter password is missing"
            }

        try:
            return {
                "status": "New user created",
                "is_sucess": True,
                "user_id": newUser(
                    data['username'],
                    data['password']
                )[0]["user_id"]
            }, 201
        except Exception as e:
            return {"status": "Error", "is_sucess": False, "error_message": str(e)}