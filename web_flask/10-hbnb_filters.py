#!/usr/bin/python3
"""
Write a script that starts a Flask web application:
    Your web application must be listening on 0.0.0.0, port 5000
    You must use storage for fetching data from the storage engine
    To load all cities of a State:
        If your storage engine is DBStorage, you must use cities relationship
        Otherwise, use the public getter method cities
    After each request you must remove the current SQLAlchemy Session:
        Declare a method to handle @app.teardown_appcontext
        Call in this method storage.close()
    Routes:
        /hbnb_filters: display a HTML page like 6-index.html, which was done
        during the project 0x01. AirBnB clone - Web static
            - Update .popover class in 6-filters.css to allow scrolling in the
              popover and a max height of 300 pixels.
            - Use 6-index.html content as source code for the template
              10-hbnb_filters.html:
                - Replace the content of the H4 tag under each filter title
                  (H3 States and H3 Amenities) by &nbsp;
            - State, City and Amenity objects must be loaded from DBStorage
              and sorted by name (A->Z)
"""

from flask import Flask, render_template
from models import storage
from models.amenity import Amenity
from models.state import State

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """ Get all states and amenities to display on html """
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    return render_template(
        '10-hbnb_filters.html', states=states, amenities=amenities)


@app.teardown_appcontext
def teardown(exception):
    """ Remove the current SQLAlchemy Session """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
