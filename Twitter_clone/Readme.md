# Switter (Twitter simple clone)
### REST API project using Flask framework. 
  
This small back-end project is supposed to clone the basic behavior of Twitter -   
* Handle user registration. 
* User login and authentication. 
* User deletion (need to be authenticated).
* User posting a tweet. 
* User following other users.
* User feed - viewing his tweets, as well as tweets from people the users follows.
* Get followed.  
  
I've used SQLite database for this project, since its a small project is it a good fit, quick to setup, and reliable.  
The authentication system is implementing a JWT token system, a fresh token is mandatory for posting new tweets, deleting the user etc.  
In addition, both of these micro-services, the front-end and the back-end, have docker files, and can be built and run as containers to communicate with each other;   
but for this simple learning example - I have it configures so it is running on 2 different ports, so the front-end is sending HTTP requests to the backend,   
the back-end queries the database, and sends back the response to the front-end. The front-end then dynamically implementing this into the HTML templates using Jinja2.  

The main emphasis of this small project is the back-end application, so understandably the front-end is lacking.
