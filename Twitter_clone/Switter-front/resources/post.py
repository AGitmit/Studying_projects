import requests
from flask.views import MethodView
from schemas.post import PlainPostSchema
from flask_smorest import Blueprint, abort
from flask import render_template, session, make_response, request, redirect

blp = Blueprint('post', __name__)

@blp.route('/post')
class PostTweet(MethodView):
    def post(self, post_data):
        print(post_data)
        if 'jwt' in session:
            try:
                new_tweet = {
                    "content": post_data
                }
            except:
                new_tweet = {
                    "content": request.form['new_content']
                }
            finally:
                url = 'http://127.0.0.1:50001/post'
                
                headers = {
                    "Authorization": session.get('jwt'),
                    "Accept": "application/json"
                }
                
                response = requests.post(url, headers=headers, json=new_tweet)
                if response.status_code == 201:
                    redirect('/myfeed')
        else:
            abort(400, message="You are not logged in.")