#!/usr/bin/python3
"""
Write a script that starts a Flask web application:
    Your web application must be listening on 0.0.0.0, port 5000
    Routes:
        - /: display “Hello HBNB!”
        - /hbnb: display “HBNB”
        - /c/<text>: display “C ”, followed by the value of the text variable
          (replace underscore _ symbols with a space )
        - /python/(<text>): display “Python ”, followed by the value of the
          text variable (replace underscore _ symbols with a space )
            - The default value of text is “is cool”
        - /number/<n>: display “n is a number” only if n is an integer
        - /number_template/<n>: display a HTML page only if n is an integer:
            - h1 tag: “Number: n” inside the tag body
    You must use the option strict_slashes=False in your route definition
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """ List all states on html """
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def remove_session(exception):
    """ Remove the current SQLAlchemy Session """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
