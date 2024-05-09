from sqlalchemy import select
from sqlalchemy.orm import Session

from api.db.db import DatabaseInstance
from api.db.models import User, Sample, Author


class UserController:

    @classmethod
    def list_users(cls):
        """
        This method returns a list of all users in the database.
        :return: the list of users, None if there's no user in the database.
        """
        return User.query.all()

    @classmethod
    def get_user(cls, user_id: int):
        """
        This method returns a user by its id.
        :param user_id: the user id.
        :return: the user if it exists, None otherwise.
        """
        return User.query.get(user_id)

    @classmethod
    def get_user_by_uid(cls, uid: str):
        """
        This method returns a user by its uid.
        :param uid: the (unique) uid of the user.
        :return: the user if it exists, None otherwise.
        """
        return User.get_by_uid(uid)

    @classmethod
    def get_user_by_email(cls, email: str):
        """
        This method returns a user by its email.
        :param email: the email of the user.
        :return: the user if it exists, None otherwise.
        """
        return User.get_by_email(email)

    @classmethod
    def create_user(cls, data: dict):
        """
        Method to create a user in the database. A new user has to have an uid and an email that are unique.
        :param data: the data to be used to create the user.
        :return: the user data, with the automatic fields updated.
        """
        user_to_create = User('')
        user_to_create.from_dict(data)
        with DatabaseInstance().session() as session:
            try:
                # Check if the uid is already in use. The uid has to be unique,
                # so no two users can have the same uid
                stmt = select(User).filter_by(uid=user_to_create.uid)
                test = session.execute(stmt).first()
                if test is not None:
                    raise Exception(f'The uid "{user_to_create.uid}" is already in use')

                # Check if the email is already in use. The email has to be unique,
                # so no two users can have the same email
                stmt = select(User).filter_by(email=user_to_create.email)
                test = session.execute(stmt).first()
                if test is not None:
                    raise Exception(f'The email "{user_to_create.email}" is already in use')

                session.add(user_to_create)
                session.commit()

                stmt = select(User).filter_by(uid=user_to_create.uid)
                user_created = session.execute(stmt).first()[0]
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
        return user_created

    @classmethod
    def update_user(cls, uid: str, new_data: dict):
        """
        Method to update the data of a user.
        :param uid: the uid to identify the user to update.
        :param new_data: the data to update.
        :return:
        """
        user_to_edit = None
        with DatabaseInstance().session() as session:
            try:
                stmt = select(User).filter_by(uid=uid)
                usr = session.execute(stmt).first()
                if usr is None:
                    raise Exception("User not found")
                user_to_edit = usr[0]
                if 'email' in new_data:
                    user_to_edit.email = new_data['email']
                if 'name' in new_data:
                    user_to_edit.name = new_data['name']
                if 'surname' in new_data:
                    user_to_edit.surname = new_data['surname']
                if 'password' in new_data:
                    user_to_edit.password = new_data['password']
                # uid is an internal identifier, it should not be changed
                # so this last condition is not really necessary
                if 'uid' in new_data:
                    user_to_edit.uid = new_data['uid']

                # Check if the uid is already in use. The uid has to be unique,
                # so no two users can have the same uid
                stmt = select(User).filter_by(uid=user_to_edit.uid)
                test = session.execute(stmt).first()
                if test is not None and test[0].id != user_to_edit.id:
                    raise Exception(f'The uid "{user_to_edit.uid}" is already in use')

                # Check if the email is already in use. The email has to be unique,
                # so no two users can have the same email
                stmt = select(User).filter_by(email=user_to_edit.email)
                test = session.execute(stmt).first()
                if test is not None and test[0].id != user_to_edit.id:
                    raise Exception(f'The email "{user_to_edit.email}" is already in use')

                session.add(user_to_edit)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
        # It may be necessary avoid the lazy loading of the user's samples
        # return user_to_edit

    @classmethod
    def delete_user(cls, uid: str):
        """
        This method removes the data associated to a user, given its uid.
        A user can't be deleted if it has samples associated.
        If a user is also an author, the user_id is removed from the author's table and the author becomes an
        'external' author.

        :param uid: the unique identifier of the user.
        :return:
        """
        with DatabaseInstance().session() as session:
            try:
                stmt = select(User).filter_by(uid=uid)
                usr = session.execute(stmt).first()
                if usr is None:
                    raise Exception("User not found")

                user_to_delete = usr[0]
                stmt = select(Sample).filter_by(user_id=user_to_delete.id)
                samples = session.execute(stmt).all()
                if len(samples) > 0:
                    raise Exception('User has samples attached')

                # If the user is also an author, remove the user_id from the author's table
                # and update the 'author' fields with the user's name and surname
                # and the email with the user's email. Thus, the author becomes an 'external' author.
                stmt = select(Author).filter_by(user_id=user_to_delete.id)
                author = session.execute(stmt).first()
                if author is not None:
                    author = author[0]
                    author.user_id = None
                    author.author = f'{user_to_delete.surname}, {user_to_delete.name}'
                    author.email = user_to_delete.email
                    session.add(author)

                session.delete(user_to_delete)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
