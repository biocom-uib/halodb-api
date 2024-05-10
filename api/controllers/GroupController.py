import datetime

import sqlalchemy.orm.session
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.db.db import DatabaseInstance
from api.db.models import Group, UserHasGroup


class GroupController:
    """
    This class is responsible for the group operations.
        A group can have many users
        A group can have many samples
        A user can have different access permissions to different groups
    """

    @staticmethod
    def _get_group_by_name(the_name: str, session: Session):
        """
        internal method to get a group by name using an already opened session.
        :param the_name: the name of the group to be retrieved.
        :param session: the database session to use to retrieve the group.
        :return: the group if it exists, None otherwise.
        """
        stmt = select(Group).filter_by(name=the_name)
        group = session.execute(stmt).first()
        return group

    @classmethod
    def list_groups(cls):
        """
        :return: the list of the whole set of groups defined in the database.
        """
        return Group.query.all()

    @classmethod
    def get_groups_by_user(cls, user_id: str):
        """
        Get the list of groups that a user is part of
        :param user_id: the user identification.
        :return: the groups having the user as a member (can be None).
        """
        with DatabaseInstance().session() as session:
            stmt = select(UserHasGroup.relation,
                          Group.id, Group.name, Group.description).join_from(Group, UserHasGroup).where(
                UserHasGroup.user_id == user_id)
            groups = session.execute(stmt).all()
            session.close()
            return groups

        # return Group.query.filter(Group.users.any(id=user_id)).all()
        # with DatabaseInstance().session() as session:
        #     stmt = select(Group).filter(Group.users.any(id=user_id))
        #     groups = session.execute(stmt).all()
        #     session.close()
        #     return groups

    @classmethod
    def get_group_by_name(cls, name: str):
        """
        Get a group by its name.
        :param name: the name of the group.
        :return: the group if it exists, None otherwise.
        """
        return Group.query.filter(Group.name == name).first()
        # with DatabaseInstance().session() as session:
        #     group = cls._get_group_by_name(name, session)
        #     session.close()
        #     return group

    @classmethod
    def get_group_by_id(cls, group_id: int) -> Group:
        """
        Get a group by its identifier.
        :param group_id: the group identifier.
        :return: the group if it exists, None otherwise.
        """
        return Group.query.filter(Group.id == group_id).first()
        # with DatabaseInstance().session() as session:
        #     stmt = select(Group).filter_by(id=group_id)
        #     group = session.execute(stmt).first()[0]
        #     session.close()
        #     return group

    @classmethod
    def accept_invite(cls, user_id: int, group_id: int, accept: bool):
        """
        An invited user cap accept or refuse the invitation
        :param user_id: the user identification
        :param group_id: the group identification
        :param accept: true if the invitation is accepted, false if not.
        :return:
        """
        with DatabaseInstance().session() as session:
            try:
                stmt = select(Group).filter_by(id=group_id)
                group = session.execute(stmt).first()
                if group is None:
                    raise Exception(f"Group with id {group_id} not found")

                stmt = select(UserHasGroup).filter_by(user_id=user_id).filter_by(group_id=group_id)
                user_has_group = session.execute(stmt).first()
                if user_has_group is None or user_has_group[0].relation != 'invited':
                    raise Exception(f"User with id {user_id} is not invited to the group")

                if accept:
                    setattr(user_has_group[0], 'relation', 'member')
                    setattr(user_has_group[0], 'addition_date', datetime.datetime.utcnow())
                else:
                    session.delete(user_has_group[0])
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()

    @classmethod
    def invite(cls, owner_id: int, invited_id: int, group_id: int):
        """
        Invite a user to a group. The owner has to be the right privileges on the group.
        :param owner_id: the user that is inviting
        :param invited_id: the user that is being invited
        :param group_id: the group that the user is being invited to
        :return:
        """
        with DatabaseInstance().session() as session:
            try:
                stmt = select(Group).filter_by(id=group_id)
                group = session.execute(stmt).first()
                if group is None:
                    raise Exception(f"Group with id {group_id} not found")

                # test = UserHasGroup.get(invited_id, group_id)
                stmt = select(UserHasGroup).filter_by(group_id=group_id, user_id=invited_id)
                test = session.execute(stmt).first()
                if test is not None:
                    if test[0].relation != 'invited':
                        raise Exception(f"User with id {invited_id} is a member the group")
                    else:
                        raise Exception(f"User with id {invited_id} has already been invited to the group")

                stmt = select(UserHasGroup).filter_by(group_id=group_id, user_id=owner_id)
                test = session.execute(stmt).first()
                # test = UserHasGroup.get(owner_id, group_id)
                if test is None:
                    raise Exception(f"User with id {owner_id} doesn't belong to the group")

                if test[0].relation != 'owner':
                    raise Exception(f"User with id {owner_id} doesn't have the right privileges to invite")

                entry: UserHasGroup = UserHasGroup(group_id=group_id, user_id=invited_id, relation='invited')
                session.add(entry)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()

    @classmethod
    def create_group(cls, data: dict):
        """
        Create a group. The group name must be unique.
        :param data: a dictionary with the keys and values to be used to create the group.
        :return: the group created, with the automated data added.
        """

        group_to_create = Group('')
        group_to_create.from_dict(data)
        with DatabaseInstance().session() as session:
            try:
                # In order to have clarity, no two groups can have the same name
                test = cls._get_group_by_name(group_to_create.name, session)
                if test is not None:
                    raise Exception(f'The group name "{group_to_create.name}" is already in use')

                session.add(group_to_create)
                session.commit()

                group_created = cls._get_group_by_name(group_to_create.name, session)[0]
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
            return group_created

    @classmethod
    def update_group(cls, group_id: int, new_data: dict):
        """
        Update a group. Although it's possible to change the group name, the group name must be unique, it's not
        possible to have two groups with the same name.
        :param group_id:
        :param new_data: The data of the group to be updated
        :return:
        """
        with DatabaseInstance().session() as session:
            try:
                stmt = select(Group).filter_by(id=group_id)
                group = session.execute(stmt).first()
                if group is None:
                    raise Exception("Group not found")
                group_to_edit = group[0]
                for key, value in new_data.items():
                    # setattr(group_to_edit, key, value)
                    if key == 'name':
                        stmt = select(Group).filter_by(name=value)
                        test = session.execute(stmt).first()
                        if test is not None:
                            raise Exception(f'The name "{value}" is already in use')
                        setattr(group_to_edit, key, value)
                    elif key == 'description':
                        setattr(group_to_edit, key, value)

                # session.add(group_to_edit)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()

    @classmethod
    def delete_group(cls, group_id: int):
        """
        To delete a group, the relation between the group and the users and also the relation between the group and the
         samples must be deleted first.
        :param group_id: the group identifier
        :return:
        """
        with DatabaseInstance().session() as session:
            try:
                stmt = select(Group).filter_by(id=group_id)
                group = session.execute(stmt).first()
                if group is None:
                    raise Exception(f"Group with (group_id) does not exist")

                group_to_delete = group[0]

                # Remove the group from all its users
                for user in group_to_delete.users:
                    user.groups.remove(group_to_delete)

                # Remove the group
                session.delete(group_to_delete)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
