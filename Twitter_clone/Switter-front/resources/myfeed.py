import requests
import json
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import render_template, session, make_response, request, redirect


blp = Blueprint('feed', __name__, description="Feed operations")


@blp.route('/myfeed')
class UserFeed(MethodView):
    @blp.response(200)
    def get(self):
        if "jwt" in session:
            headers = {
                    "Authorization": "Bearer " + session.get('jwt'),
                    "Content-Type": "application/json"
                }
            
            url = "http://127.0.0.1:5001/post"
            user_posts = requests.get(url, headers=headers).json()
            
            url = "http://127.0.0.1:5001/followedcontent"
            followed_content = requests.get(url, headers=headers).json()
            
            feed_content = {"user_content": user_posts, "followed_content": followed_content}
                        
            html = render_template('feed.html', content = feed_content)
            response = make_response(html)
            response.headers['Content-Type'] = 'text/html'
            return response
            
        else:
            abort(400, message="You havn't logged in yet.")
    
    @blp.response(201)        
    def post(self):
        if 'jwt' in session:
            new_tweet = {
                "content": request.form['new_content']
            }
            
            url = "http://127.0.0.1:5001/post"            
            headers = {
                "Authorization": "Bearer " + session.get('jwt'),
                "Content-Type": "application/json"
            }
            try:
                response = requests.post(url, headers=headers, json=new_tweet)
            except:
                return {"message": "Couldn't proccess the request."}
            else:
                if response.status_code == 201:
                    return {"message": "new post created successfully. please refresh page."}
    
        else:
            abort(400, message="You are not logged in.")