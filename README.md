# Pentagram Blog App

Pentagram Blog App; It is a small-scale social media application.

**In this project the user can:**

	-User can register, login, logout,
	
	-User can share, update, delete posts,
	
	-User can comment, update, delete,
	
	-User can like or dislike the posts,


#  Getting started

 1. Clone the repo:

 -`git clone https://github.com/hilaldedek/pentagram_blog-app.git`
 
 2. Frontend:

  -`cd client\blog`

  -`yarn install` 
  
  -`npm run serve`
  
 3. Backend:
 
   -`cd api`
   
   -`python -m venv env`
    
   -Windows: `.\env\Scripts\activate`
 
   -MacOS: `source env/bin/activate`
   
   -`pip install -r requirements.txt`

   -Create a config.py file in the api directory and paste the following codes into it. Don't forget to create your own key in YOUR_SECRET_KEY! :
   
    ```
    
    from datetime import timedelta
     class BaseConfig(object):
	    DEBUG = False
	    JWT_SECRET_KEY = 'YOUR_SECRET_KEY'
	    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
   
     class DevelopmentConfig(BaseConfig):
	    DEBUG = True
     class ProductionConfig(BaseConfig):
	    DEBUG = False
     config = DevelopmentConfig
     
    ```
    
   -`flask --app app run --debug`

 4.Database:

 -Install MongoDB step by step according to the platform you use from the link below:
    
   [Install MongoDB](https://www.mongodb.com/docs/manual/installation/)


 
# Demo

![loginregister](https://github.com/hilaldedek/pentagram_blog-app/assets/95539281/25273f07-4406-4749-b362-1c8a5ad0fcfc)

![createPost](https://github.com/hilaldedek/pentagram_blog-app/assets/95539281/c4e09113-4654-421c-ab70-da3d6834e717)

![post](https://github.com/hilaldedek/pentagram_blog-app/assets/95539281/8807c6ec-dfb0-4ebb-8459-8b0ea8a49ed6)

![comment](https://github.com/hilaldedek/pentagram_blog-app/assets/95539281/910b1242-822c-47b4-9a82-a0c5a6a20781)


