# Import Json
import json

# Initializer
from initializer import redis

# Import Resource from Flask Restful
from flask_restful import Resource

# Import Flask
from flask import request

# Import DB Function
from database.utils import create_hash
from database.functions import getAllBeers, getBeerByUser, newBeerToUser, newUser, checkUser

# Init Redis
redis = redis.connect()


class getAllAvailableBeers(Resource):

    def get(self):
        return {
            "status": "Success",
            "is_successful": True,
            "data": getAllBeers()
        }


class loginUser(Resource):

    def __init__(self):
        self.error = False
        self.error_message = None

    def post(self):
        data = request.json

        if data is None:
            self.error = True
            self.error_message = "Request body cannot be null"
        elif 'username' not in data:
            self.error = True
            self.error_message = "Parameter username is not found"
        elif 'password' not in data:
            self.error = True
            self.error_message = "Parameter password is not found"

        if self.error:
            return {
                "status": self.error_message,
                "is_sucess": False
            }, 400

        try:
            user_id = checkUser(
                data['username'],
                data['password']
            )
        except Exception:
            return {
                "status": "Check username and password",
                "is_sucess": False
            }, 400

        if user_id is None:
            return {
                "status": "Check username and password",
                "is_sucess": False
            }, 400

        session_token = create_hash({
            "username": data['username'],
            "password": data['password']
        })

        redis.set(session_token, str(user_id))

        return {
            "status": "Login successfully",
            "is_sucess": True
        }, 200, {"token_api": session_token}


class getBeerDetail(Resource):

    def __init__(self):
        self.error = False
        self.error_message = None

    def post(self):
        data = request.json
        token_api = request.headers.get('token_api')

        if token_api is None:
            self.error = True
            self.error_message = "token_api is required. Not found in headers"
        elif data is None:
            self.error = True
            self.error_message = "Request body cannot be null"
        elif 'beer_id' not in data:
            self.error = True
            self.error_message = "Parameter beer_id is not found"

        if self.error:
            return {
                "status": self.error_message,
                "is_sucess": False
            }, 400

        session_data = eval(redis.get(token_api).decode('utf-8'))

        try:
            db_response = getBeerByUser(
                data['beer_id'],
                session_data['id']
            )

            return {
                "status": "Success",
                "is_successful": True,
                "data": db_response
            }, 200
        except Exception as e:
            return {
                "status": str(e),
                "is_successful": False
            }, 400


class addNewBeerToUser(Resource):

    def __init__(self):
        self.error = False
        self.error_message = None

    def post(self):
        data = request.json
        token_api = request.headers.get('token_api')

        if token_api is None:
            self.error = True
            self.error_message = "token_api is required. Not found in headers"
        elif data is None:
            self.error = True
            self.error_message = "Request body cannot be null"
        elif 'beer_id' not in data:
            self.error = True
            self.error_message = "Parameter beer_id is not found"

        if self.error:
            return {
                "status": self.error_message,
                "is_sucess": False
            }, 400

        session_data = eval(redis.get(token_api).decode('utf-8'))

        try:
            newBeerToUser(
                data['beer_id'],
                session_data['id']
            )
            return {"status": "Update successfully", "is_sucess": True}
        except Exception as e:
            return {"status": "Error", "is_sucess": False, "error_message": str(e)}


class addUser(Resource):

    def __init__(self):
        self.error = False
        self.error_message = None

    def post(self):
        data = request.json

        if data is None:
            self.error = True
            self.error_message = "Request body cannot be null"
        elif 'username' not in data:
            self.error = True
            self.error_message = "Parameter username is not found"
        elif 'password' not in data:
            self.error = True
            self.error_message = "Parameter password is not found"

        if self.error:
            return {
                "status": self.error_message,
                "is_sucess": False
            }, 400

        try:
            user_id = newUser(
                data['username'],
                data['password']
            )[0]["user_id"]

            session_token = create_hash({
                "username": data['username'],
                "password": data['password']
            })

            redis.set(session_token, str(user_id))

            return {
                "status": "New user created",
                "is_sucess": True
            }, 201, {"token_api": session_token}
        except Exception as e:
            return {"status": "Error", "is_sucess": False, "error_message": str(e)}