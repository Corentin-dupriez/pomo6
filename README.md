# POMO6 Website 

## What is it? 
Pomo6 is a website created for my final project in the SoftUni course
on Django. The idea is to create a small site
similar to fiverr, where people can propose 
their help. 
The technology used is Python, and mostly
Django. 

## App structure 
The app is composed of several components: 
- **pomo6**: containing the home page, settings and URLs
- **accounts**: contains no models, only register view and URLs
for login, logout and register. 
There's no specific model for users, we use the standard 
user model.
- **adverts**: containing forms, views and methods 
for advert search, visualisation, modification. It also contains 
models for views, ratings and orders. The script categories_model
also allows for the generation of an ML model to propose categories
on the FE to the user based on the title of the advert they are creating
- **profiles**: contains views and models for user profiles
- chat: app that allows real-time chat using websockets. It contains
the models for threads and messages, as well as channels consumers 
and routing.
- **notifications**: contains the models, utilities and signals to create notifications
- **ml_model**: contains the exported model and vectorizer from categories_model
- **populate_db**: a script that allows filling the DB with random values

## User journey
Upon arriving on the home page, the user has several choices:
- register
- login
- search as a guest

If the user decides to navigate as a guest, their functionality will
be reduced. They can visualize listings, but have to log in to do anything 
else (contact sellers, post a listing ...).

If the user doesn't have an account yet, they can use the register button
to create one. Otherwise, they can log in.

## Requirements 
- The application must have at least 10 web pages 
- At least 5 pages must use CBV
- The application must have at least 5 independent models
- The application must have at least 5 forms 
- The application must have at least 5 templates 
- Have a public part 
- Login/register/logout functionality
- Private part 
- Customized admin site with at least 5 custom options
- Unauthenticated users have only get permissions and post on login/register
- Authenticated users have CRUD access to their content
- 2 groups of admins: One with full CRUD (superuser) and one with limited CRUD (staff)
- User roles managed from admin site 
- Role management secure and error safe 
- Error handling and data validation to avoid crash 

## Bonuses
- Testing (Unit and integration)
- Async views 
- REST capabilities 
- Extend Django user
- Deploy project 
- Other functionalities 

## Learning journey 
The goal of the project is just to get 
better at Django, and try to improve the 
app incrementally, following the SoftUni lesson.

If you have any comments on the structure
of the app, or beginner mistakes, feel free to comment.

Thank you!
