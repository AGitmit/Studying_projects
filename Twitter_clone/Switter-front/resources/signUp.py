import requests
import os
import json
from flask_smorest import Blueprint, abort
from flask import render_template, session, make_response, request
from flask.views import MethodView
from schemas.user import PlainUserSchema
from marshmallow import ValidationError

blp = Blueprint('signUp', __name__, description='Sign up operation')

@blp.route('/user/register', methods=['GET','POST'])
class UserRegister(MethodView):
    @blp.response(200)
    def get(self):
        html = render_template('register.html')
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html'
        return response

    @blp.response(200)
    def post(self):
        user_data = {
                "username": request.form['username'],
                "password": request.form['password']
            }
        url = 'http://127.0.0.1:5001/user/register'
        try:
            PlainUserSchema().validate(user_data)
            response = requests.post(url, json=user_data)

            if response.status_code == 200:
                return response.json()
    
            else:
                abort(response.status_code, message=response.json())
                
        except ValidationError as err:
            abort(400, message=err)
