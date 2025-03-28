import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.type_api import to_instance

from api.db.db import DatabaseInstance
from api.db.models import Group, User, User_Has_Group
from api.utils import to_dict


class GroupController:
    """
    This class is responsible for the group operations.
        A group can have many users
        A group can have many samples
        A user can have different access permissions to different groups
    """

    @classmethod
    def list_groups(cls):
        """
        :return: the list of the whole set of groups defined in the database.
        """
        return to_dict(Group.query.all())

    @classmethod
    def get_groups_by_user(cls, user_id: str):
        """
        Get the list of groups that a user is part of
        :param user_id: the user identification.
        :return: the groups having the user as a member (can be None).
        """
        #
        groups = None
        with DatabaseInstance.get().session() as session:
            stmt = select(User_Has_Group.relation,
                          Group.id, Group.name, Group.description).join_from(Group, User_Has_Group).where(
                User_Has_Group.user_id == user_id)
            groups = session.execute(stmt).all()

            groups = [{'relation': grp[0], 'group_id': grp[1], 'name': grp[2], 'description': grp[3]} for grp in groups]

            # the_user = User.query.filter(User.id == user_id).first()
            # groups = to_dict(the_user.groups)

        return groups

    @classmethod
    def get_group_by_name(cls, name: str):
        """
        Get a group by its name.
        :param name: the name of the group.
        :return: the group if it exists, None otherwise.
        """
        return Group.query.filter(Group.name == name).first()

    @classmethod
    def get_group_by_id(cls, group_id: int) -> Group:
        """
        Get a group by its identifier.
        :param group_id: the group identifier.
        :return: the group if it exists, None otherwise.
        """
        return Group.query.filter(Group.id == group_id).first()

    @classmethod
    def accept_invite(cls, user_id: int, group_id: int, accept: bool):
        """
        An invited user cap accept or refuse the invitation
        :param user_id: the user identification
        :param group_id: the group identification
        :param accept: true if the invitation is accepted, false if not.
        :return:
        """
        with DatabaseInstance.get().session() as session:
            try:
                stmt = select(Group).filter_by(id=group_id)
                group = session.execute(stmt).first()
                if group is None:
                    raise Exception(f"Group with id {group_id} not found")

                stmt = select(User_Has_Group).filter_by(user_id=user_id).filter_by(group_id=group_id)
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

    @classmethod
    def invite(cls, owner_id: int, invited_id: int, group_id: int):
        """
        Invite a user to a group. The owner has to be the right privileges on the group.
        :param owner_id: the user that is inviting
        :param invited_id: the user that is being invited
        :param group_id: the group that the user is being invited to
        :return:
        """
        with DatabaseInstance.get().session() as session:
            try:
                # stmt = select(Group).filter_by(id=group_id)
                # group = session.execute(stmt).first()
                group = Group.query.filter_by(id=group_id).first()
                if group is None:
                    raise Exception(f"Group with id {group_id} not found")

                # stmt = select(User_Has_Group).filter_by(group_id=group_id, user_id=invited_id)
                # test = session.execute(stmt).first()
                test = User_Has_Group.query.filter_by(group_id=group_id, user_id=invited_id).first()
                if test is not None:
                    if test.relation != 'invited':
                        raise Exception(f"User with id {invited_id} is a member the group")
                    else:
                        raise Exception(f"User with id {invited_id} has already been invited to the group")

                # stmt = select(User_Has_Group).filter_by(group_id=group_id, user_id=owner_id)
                # test = session.execute(stmt).first()
                test = User_Has_Group.query.filter_by(group_id=group_id, user_id=owner_id).first()
                if test is None:
                    raise Exception(f"User with id {owner_id} doesn't belong to the group")

                if test.relation != 'owner':
                    raise Exception(f"User with id {owner_id} doesn't have the right privileges to invite")

                entry: User_Has_Group = User_Has_Group(group_id=group_id, user_id=invited_id, relation='invited')
                session.add(entry)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    @classmethod
    def create_group(cls, data: dict, user: User):
        """
        Create a group. The group name must be unique.
        :param user: the owner of the group.
        :param data: a dictionary with the keys and values to be used to create the group.
        :return: the group created, with the automated data added.
        """

        group_to_create = Group()
        group_to_create.from_dict(data)
        with DatabaseInstance.get().session() as session:
            try:
                # In order to have clarity, no two groups can have the same name
                test = Group.query.filter_by(name=group_to_create.name).first()
                if test is not None:
                    raise Exception(f'The group name "{group_to_create.name}" is already in use')

                session.add(group_to_create)
                session.flush()
                connection = User_Has_Group(group_id=group_to_create.id, user_id=user.id, relation='owner')
                session.add(connection)

                session.commit()

                group_created = group_to_create.as_dict()
            except Exception as e:
                session.rollback()
                raise e

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
        with DatabaseInstance.get().session() as session:
            try:
                group_to_edit = Group.query.filter_by(id=group_id).first()
                if group_to_edit is None:
                    raise Exception("Group not found")

                for key, value in new_data.items():
                    # setattr(group_to_edit, key, value)
                    if key == 'name':
                        test = Group.query.filter_by(name=value).first()
                        if test is not None:
                            raise Exception(f'The name "{value}" is already in use')
                        setattr(group_to_edit, key, value)
                    elif key != 'id':
                        setattr(group_to_edit, key, value)
                session.query(Group).filter_by(id=group_id).update(group_to_edit.as_dict())

                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            return group_to_edit

    @classmethod
    def delete_group(cls, group_id: int):
        """
        To delete a group, the relation between the group and the users and also the relation between the group and the
         samples must be deleted first.
        :param group_id: the group identifier
        :return:
        """
        with DatabaseInstance.get().session() as session:
            try:
                stmt = select(Group).filter_by(id=group_id)
                group = session.execute(stmt).first()
                if group is None:
                    raise Exception(f"Group with (group_id) does not exist")

                group_to_delete = group

                # Remove the group from all its users
                for relation_to_user in group_to_delete.user_has_group:
                    session.delete(relation_to_user)

                # Remove the group
                session.delete(group_to_delete)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    @classmethod
    def get_relation(cls, user_id, group_id):
        """
        Get the relation between a user and a group.
        :param user_id: the user identifier
        :param group_id: the group identifier
        :return: the relation between the user and the group.
        """
        with DatabaseInstance.get().session() as session:
            stmt = select(User_Has_Group.relation).where(User_Has_Group.user_id == user_id).where(
                User_Has_Group.group_id == group_id)
            relation = session.execute(stmt).first()
            return relation[0] if relation is not None else None
