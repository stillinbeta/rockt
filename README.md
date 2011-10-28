Think Monopoly meets Foursquare with Streetcars. 

Uses Django and MongoDB. MongoDB's geospatial indices are used, so it's not 
substitutable without some work. 

Install [django mongodb engine](http://django-mongodb.org/topics/setup.html),
which depends on 
[django-norel](http://www.allbuttonspressed.com/projects/django-nonrel) and 
[djangotoolbox](http://www.allbuttonspressed.com/projects/djangotoolbox). 
I am currently a little ahead of the upstream `django_mongodb_engine`, so it's safest to use mine.

Also requires geopy:
    pip install geopy


