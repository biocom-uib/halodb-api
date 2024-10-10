from sqlalchemy import select
from sqlalchemy.orm import Session

from api.db.db import DatabaseInstance
from api.db.models import Project, Experiment, User  # , User_Project
from api.utils import to_dict


class ProjectController:
    """
    A project represents a set of experiments that are related to each other.
    The project can have multiple experiments associated with it. The experiments are stored in the Experiment table.
    The project can have multiple users. The users are stored in the UserProject table.
    Indirectly, the project can have multiple samples associated with it. The samples are stored in the Sample table.
    """

    @staticmethod
    def _get_project_by_name(the_name: str, session: Session):
        """
        internal method to get a project by name using an already opened session
        :param the_name: the name of the project to be retrieved
        :param session: the database session to use to retrieve the group
        :return: the project if it exists, None otherwise
        """
        stmt = select(Project).filter_by(name=the_name)
        group = session.execute(stmt).first()
        return group

    @classmethod
    def list_projects(cls):
        """
        Return a list of the projects in the database
        :return:
        """
        return to_dict(Project.query.all())

    @classmethod
    def get_projects_by_user(cls, user_id: int):
        """
        Get the list of projects that a user is part of
        :param user_id: the user identification.
        :return: the groups having the user as a member (can be None).
        """

        with DatabaseInstance.get().session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if user is None:
                projects = []
            else:
                # stmt = select(Project.id, Project.name, Project.description).join(UserProject).where(UserProject.user_id == user_id)
                # projects = session.execute(stmt).all()
                projects = user.projects

        return to_dict(projects)

    @classmethod
    def get_project_by_id(cls, project_id: int):
        """
        Get a project by its id
        :param project_id:
        :return: The project if it exists, None otherwise
        """
        return Project.query.get(project_id).as_dict()
        # with DatabaseInstance.get().session() as session:
        #     stmt = select(Project).filter_by(id=project_id)
        #     project = session.execute(stmt).first()
        #
        # return project

    @classmethod
    def create_project(cls, data: dict):
        """
        Create a project. The project name must be unique.
        :param data: a dictionary with the keys and values to be used to create the project
        :return:
        """

        project_to_create = Experiment('')
        project_to_create.from_dict(data)
        with DatabaseInstance.get().session() as session:
            try:
                # In order to have clarity, no two groups can have the same name
                test = cls._get_project_by_name(project_to_create.name, session)
                if test is not None:
                    raise Exception(f'The project name "{project_to_create.name}" is already in use')

                session.add(project_to_create)
                session.commit()
                stmt = select(Project).filter_by(id=project_to_create.id)
                project_created = session.execute(stmt).first()[0]
            except Exception as e:
                session.rollback()
                raise e
            return project_created.as_dict()

    @classmethod
    def update_project(cls, project_id: int, new_data: dict):
        with DatabaseInstance.get().session() as session:
            try:
                stmt = select(Project).filter_by(id=project_id)
                project = session.execute(stmt).first()
                if project is None:
                    raise Exception("Project not found")
                project_to_edit = project[0]
                for key, value in new_data.items():
                    if key == 'name':
                        stmt = select(Project).filter_by(name=value)
                        test = session.execute(stmt).first()
                        if test is not None:
                            raise Exception(f'The name "{value}" is the name of another project')
                    # if no errors found, update the key with the value
                    setattr(project_to_edit, key, value)

                # session.add(project_to_edit)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            return project_to_edit.as_dict()

    @classmethod
    def delete_project(cls, project_id: int):
        with DatabaseInstance.get().session() as session:
            try:
                stmt = select(Project).filter_by(id=project_id)
                project = session.execute(stmt).first()
                if project is None:
                    raise Exception("Project not found")

                # Remove all the experiments associated with the project
                # This is done to avoid orphan experiments
                # The samples and users associated with the experiments are not removed
                stmt = select(Experiment).filter_by(project_id=project_id)
                experiments = session.execute(stmt).all()
                for exp in experiments:
                    # Remove the experiment from all its samples
                    for sample in exp.samples:
                        sample.experiment.remove(exp)
                    # Remove the experiment from all its users
                    for user in exp.users:
                        user.experiment.remove(exp)
                    # Remove the experiment
                    session.delete(exp[0])

                project_to_delete = project[0]
                session.delete(project_to_delete)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
