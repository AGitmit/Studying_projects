import requests
import os
import json
from flask_smorest import Blueprint, abort
from flask import render_template, session, make_response, request, redirect
from flask.views import MethodView
from schemas.user import PlainUserSchema, LoginFormSchema
from marshmallow import ValidationError

blp = Blueprint('signIn', __name__, description='Sign in operation')

@blp.route('/user/login', methods=['GET','POST'])
class UserLogin(MethodView):
    @blp.response(200)
    def get(self):
        html = render_template('signIn.html')
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html'
        return response

    @blp.response(200)
    def post(self):
        user_data = {
                "username": request.form['username'],
                "password": request.form['password']
            }
        url = 'http://127.0.0.1:5001/user/login'
        try:
            PlainUserSchema().validate(user_data)
            response = requests.post(url, json=user_data)

            if response.status_code == 200:
                # Store JWT in local storage cookie
                session['jwt'] = response.json()['access_token']
                return {'message': 'Successfully logged in.'}
                
            else:
                abort(response.status_code, message=response.json())
                
        except ValidationError as err:
            abort(400, message=err)
