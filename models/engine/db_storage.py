#!/usr/bin/python3
"""This module defines the engine for the DBStorage"""
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """ Connects to the MySQL database """
    __engine = None
    __session = None

    def __init__(self):
        """ Create the engine to link MySQL database """
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                getenv('HBNB_MYSQL_USER'), getenv('HBNB_MYSQL_PWD'),
                getenv('HBNB_MYSQL_HOST'), getenv('HBNB_MYSQL_DB')),
            pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """ Query to get all objects depending of the class """
        classes = ['State', 'City', 'User', 'Amenity', 'Place', 'Review']
        all_objs = {}

        if cls:
            query = self.__session.query(cls).all()
            for obj in query:
                all_objs[f'{obj.__class__}.{obj.id}'] = obj
        else:
            for class_name in classes:
                query = self.__session.query(class_name).all()
                for obj in query:
                    all_objs[f'{obj.__class__}.{obj.id}'] = obj

        return all_objs

    def new(self, obj):
        """ Add the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Create the current session and all tables in the database """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
        """ Close the session """
        self.__session.close()
