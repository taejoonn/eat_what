Eat What

A web app which chooses a random local restaurant to eat and displays their information and menu.


--------------------------------
            SET UP
--------------------------------

Requires:
    Python 3.7.1 or greater

pip install django

pip install python-google-places

pip install requests


In /eat_what/settings.py :
    - Enter your email address on line 132
    - Enter your password on line 133

In /eats/views/result.py :
    - Enter your Google API key on line 7


--------------------------------
            EXECUTE
--------------------------------

In the project directory "/eat-what":

    python manage.py runserver

In your browser, enter:
    localhost:8000/eats


--------------------------------
            FUTURE
--------------------------------
- Integrate food courier services
- Integrate more Yelp restaurant information - e.g. review, hours, rating

Demo:

![Image of demo gif](https://github.com/taejoonn/eat_what/blob/master/static/img/eat-what-demo.gif)