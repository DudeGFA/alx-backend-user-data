#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
            creates and saves
            a user to the database
            Args:
                email_: string
                hashed_password_: string
            return:
                a User object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
            Args: arbitrary
            returns: first row found in the users table
                as filtered by the method's input arguments
        """
        all_users = self._session.query(User)
        for key, value in kwargs.items():
            if key not in User.__dict__:
                raise InvalidRequestError
            for user in all_users:
                if getattr(user, key) == value:
                    return user
        raise NoResultFound

    def update_user(self, user_id, **kwargs) -> User:
        """
            update a user's attributes
            Args: arbitrary
            returns: None
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if key not in User.__dict__:
                raise ValueError()
            setattr(user, key, value)
        return None
