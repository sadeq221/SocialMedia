# SOCIAL MEDIA

## Introduction
A Django back-end project containing two apps:
####**Main**: Provides DRF APIs for managing features like: Authentication, Posts, Comments, Likes, Follows and etc.
####**Chat**: Provides the ability to chat with other users using Django channels and websockets.

## Structure of the Project
### Root directory

**Note** When explaining the structure, We are not gonna mention the django built-in files like manage.py and ... because these are familiar to everyone who knows djanog and there is no need to talk about them here.

#### .env
A file that include the environment variables of the sensitive data to be used in the settings

#### db.sqlite3
The database file that is used for this project

#### /media and /static
"Media" directoriy is meant to store the media files uploaded by user. While "static" is all about storing the files that are parts of the website like html, css, javascript and the some media files.
These two operations are handled differently through development and production.
In development, they are done by django itself. While in production, static files are served by the server using "whitenoise" and the user-media files are served using a separeate domain; "media.domain.com".

#### /Requirements
This directory includes three ".in" files, requirements_base.in, requirements_dev.in and requirements_prod.in. The first one includes all pip-installable packages that are required for development and production. The second inherits all that packages from the first one and in addition has some development-specific packages that are needed for staff like debuging, testing and ...
The third one also inherits from the base but as you can guess from its name, It has some additional production-specific packages that are necessary for deployment.
When you want to install the requirements, You just need to run pip-compile on one of those to files to get the ".txt" file which you can install its packages running pip-sync command.

#### /social
This is my project folder that includes:

##### wsgi.py
The configuration file needed in deployment

##### urls.py
The main urls of the project.

##### /settings
Like requirements folder, The settings also has three files: base.py, development.py and production.py. The first has all the necessary configuration for the project. The second inherits from the first and adds some development-specific configuration. While the production.py in addition to inheriting from the base, it has the production-specific confgs.

#### /app
This is the main and only app of the project. It includes:

##### /tests
This is a folder containig all the necessary tests like testing views, models and urls

##### helpers.py
In this file, I've defined some handy and reusable functions to take adventage of in the views.py file.

##### urls.py
The urls of the app. This urls take us to the main functionallity of the API's. Most of them are for the CRUD operations.

##### models.py
The models of the app. The available models are User, Profile, Follow, Post, Comment, PostLike and CommentLike. Each one of them handles the dealing with database to create, read, edit and delete the related objects.

##### serializers.py
Contains serializers for the above models.

##### views.py
Contains the fuction-based api-views that are used in this application

## How does it work
Like any other django-rest-framework API. This program is supposed to behave the same. By visiting a url, you're gonna be taken to the related view and after proccessing the request, you will get a json response.

Lets take a look at some of important aspects of the app

### Authentication
For authentication, we're using jwt tokens. They are generated through register and login views. You will need them whenever you touch a view with "IsAuthenticated" permission. This permission is set for all the requests except the ones with "GET" method.

### Database Considerations
* User needs to have a unique email
* I've overriden the default save method of the user model so whenever a user object is created, there will be a profile created for it.
* A user can only like a post or a comment once.(Duplicate PostLikes or CommentLikes are not allowed).
* A user can only follow another user once (Duplicate Follow objects are not allowed).

### Tests
The project is coverd by lots of tests using django test framework. This tests are written for views, models and urls and are designed to verify that valid and invalid scenarios are handled correctly.
They are written into separate files; test_views.py, test_urls.py and test_models.py.
In each file the tests are coded into classes, each class is meant to handle the related operations. For expamle, in test_views.py, all the comment-related tests are written into a class called "TestCommentViews". By using this approach, the test are gonna be more clean, readable and well-designed.
