# Composite 
### This site emphasizes CRUD functionality, AJAX requests, and using API's
I initially hosted this site on heroku and I still maintain a heroku-production branch.  After learning how to configure a linux web server from scratch I went back and installed this site on an AWS linux box.  
___
[![Build Status](https://travis-ci.org/jreiher2003/Composite.svg?branch=master)](https://travis-ci.org/jreiher2003/Composite)
_______  
### Tech Stack 
* linux ubuntu/trusty64  
* vagrant  
* python2.7 
* flask 
* memecached  
* sqlalchemy
* postgresql 
* bootstrap 
* aws  

#### Run code  
`vagrant up`  
`vagrant ssh`  

#### put environ envs like this
```
mkvirtualenv venv

# sudo nano $VIRTUAL_ENV/bin/postactivate
# ex. ->-> export APP_SETTINGS="config.DevelopmentConfig"
  ex. ->-> export SECRET_KEY="add a secret key"
  ex. ->-> export DATABASE_URL="postgres://vagrant:vagrant@localhost:5432/ascii"
```
`workon venv`  
`cd /vagrant`  
`python db_create.py`  
`python manage.py runserver`  

#### Page 1 Home or /ascii
**Front page** has a submission form to collect title and ascii art. The app also collects IP addresses and converts them to geoPts of lat, lon which is represented on the map with a marker when you make a post.
**Crud functionality** - this app can create read update and delete

#### Page 2 /ajax
This page uses **ajax requests and api's**.
The api's used are **NY Times, Wikipedia, and Google street maps**
A user puts in an address and a street view picture shows up along with NYT articles about the city and any Wikipedia links about the city or state.

#### Page 3 /api 
This page uses my own **api** that I created from this [site](http://adopt-puppy.herokuapp.com/api ) and this [repo](https://github.com/jreiher2003/Puppy-Adoption).  It is a simple example of how to create and use an api in this type of tech stack.  