from sqlalchemy import select
from api.db.db import DatabaseInstance
from api.db.models import Experiment, UserExperiment, Project, UserProject


class ExperimentController:
    """
    This class is used to manage the experiments in the database. It is used to create, update, delete and list the
    experiments in the database.
    An experiment can have multiple users associated with it. The users are stored in the UserExperiment table.
    An experiment belongs to a single project. The project is stored in the Project table.
    An experiment can have multiple samples associated with it. The samples are stored in the Sample table.
    """

    @classmethod
    def _get_experiment_by_name_and_project(cls, the_name: str, the_project_id, session):
        """
        internal method to get an experiment by name using a already opened session.
        :param the_name: the name of the experiment to be retrieved.
        :param the_project_id: the project id to which the experiment belongs.
        :param session: the database session to use to retrieve the experiment.
        :return: the experiment if it exists, None otherwise.
        """
        stmt = select(Experiment).filter_by(name=the_name,
                                            project_id=the_project_id)
        experiment = session.execute(stmt).first()
        return experiment

    @classmethod
    def list_experiments(cls, user_id: int):
        """
        :return: the list of the whole set of experiments defined in the database
        """
        return Experiment.query.all()

    @classmethod
    def get_experiments_by_user(cls, user_id: int):
        """
        Get the list of groups that a user is part of
        :param user_id: the user identification.
        :return: the groups having the user as a member (can be None).
        """
        with DatabaseInstance().session() as session:
            # subquery = select(UserExperiment).where(UserExperiment.user_id == user_id).subquery()
            # stmt = select(Experiment).join(subquery, Experiment.id == subquery.c.experiment_id)

            stmt = select(Experiment.id, Experiment.name, Experiment.description, Experiment.project_id).join(UserExperiment).where(UserExperiment.user_id == user_id)
            experiments = session.execute(stmt).all()

        return experiments

        # return Experiment.query.filter_by(user_id=user_id).all()
        # with DatabaseInstance().session() as session:
        #     stmt = select(Experiment).filter(Experiment.users.any(id=user_id))
        #     experiments = session.execute(stmt).all()
        #
        # return experiments

    @classmethod
    def get_by_project(cls, user_id: int, project_id: int):
        """
        Get the list of experiments that belong to a project.
        :param user_id: the supposed member of the project.
        :param project_id: the project identification.
        :return: the experiments that belong to the project (can be None).
        """

        # Test if the user can access to the project
        link = UserProject.query.filter_by(user_id=user_id, project_id=project_id).first()
        if link is None:
            return None

        return Experiment.query.filter_by(project_id=project_id).all()

    @classmethod
    def get_experiment_by_id(cls, experiment_id: int):
        """
        Get an experiment by its id.
        :param experiment_id: the id of the experiment.
        :return: the experiment data if it exists, None otherwise.
        """
        return Experiment.query.get(experiment_id)
        # with DatabaseInstance().session() as session:
        #     stmt = select(Experiment).filter_by(id=experiment_id)
        #     experiment = session.execute(stmt).first()
        #
        # return experiment

    @classmethod
    def get_experiment_by_id_user_id(cls, experiment_id: int, user_id: int):
        """
        Get an experiment by its id.
        :param experiment_id: the id of the experiment.
        :return: the experiment data if it exists, None otherwise.
        """
        with DatabaseInstance().session() as session:
            subquery = select(UserExperiment).where(UserExperiment.experiment_id == experiment_id,
                                                    UserExperiment.user_id == user_id).subquery()
            stmt = select(Experiment).join(subquery, Experiment.id == subquery.c.experiment_id)
            experiment = session.execute(stmt).first()

            return experiment

    @classmethod
    def create_experiment(cls, user_id: int, data: dict):
        """
        To create an experiment, some data is needed. The experiment name must be unique in the project.
        :param user_id: the user that is creating the experiment.
        :param data: a dictionary with the keys and values to be used to create the experiment.
        :return: the experiment data updated with the auto-calculated fields.
        """

        experiment_to_create = Experiment('')
        experiment_to_create.from_dict(data)
        with DatabaseInstance().session() as session:
            try:
                test = Project.get_project_by_id(experiment_to_create.project_id)
                if test is None:
                    raise Exception(f'There are no projects with id {experiment_to_create.project_id}')

                # To avoid mistakes, no two experiments, belonging to the same project, can have the same name.
                test = cls._get_experiment_by_name_and_project(experiment_to_create.name,
                                                               experiment_to_create.project_id, session)
                if test is not None:
                    raise Exception(f'The experiment name "{experiment_to_create.name}" is already in use in the '
                                    f'project "{experiment_to_create.project_id}"')

                session.add(experiment_to_create)
                user_exp = UserExperiment(user_id, experiment_to_create.id)
                session.add(user_exp)
                stmt = select(Experiment).filter_by(id=experiment_to_create.id)
                session.commit()
                experiment_created = session.execute(stmt).first()[0]
            except Exception as e:
                session.rollback()
                raise e

            return experiment_created

    @classmethod
    def update_experiment(cls, experiment_id: int, new_data: dict):
        """
        Modify the data of an experiment
        :param experiment_id: the experiment unique identifier
        :param new_data: the data to be used to update the experiment information
        :return:
        """
        with DatabaseInstance().session() as session:
            try:
                stmt = select(Experiment).filter_by(id=experiment_id)
                experiment = session.execute(stmt).first()
                if experiment is None:
                    raise Exception("Experiment not found")
                experiment_to_edit = experiment[0]
                for key, value in new_data.items():
                    if key == 'project_id':
                        project = Project.get_project_by_id(value)
                        if project is None:
                            raise Exception(f"Project with id {value} not found")
                        # Does the new project have an experiment with the same name?
                        # Maybe the experiment name also changes, or not. Get the name of the experiment
                        # to check if it is already in use in the new project.
                        if "name" in new_data.keys:
                            the_name = new_data["name"]
                        else:
                            the_name = experiment.name

                        test = cls._get_experiment_by_name_and_project(the_name, project.id)
                        if test is not None:
                            raise Exception(f'The new project has already an experiment with the name'
                                            f' "{the_name}".')
                    elif key == 'name':
                        test = cls._get_experiment_by_name_and_project(value, experiment_to_edit.project_id, session)
                        if test is not None:
                            raise Exception(f'The name "{value}" is already in use in another experiment in the same '
                                            f'project')
                    # if no errors are found, update the key with the value.
                    setattr(experiment_to_edit, key, value)

                # session.add(experiment_to_edit)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    @classmethod
    def delete_experiment(cls, experiment_id: int):
        """
        Remove an experiment from the database. The possible samples related to the experiment are not removed. Only the
        experiment is removed, so the relation with the samples are also removed (but the samples remain).
        Also, the relation with the users are removed.
        :param experiment_id: the experiment identifier
        :return:
        """
        with DatabaseInstance().session() as session:
            try:
                stmt = select(Experiment).filter_by(id=experiment_id)
                experiment = session.execute(stmt).first()
                if experiment is None:
                    raise Exception("Experiment not found")
                experiment_to_delete = experiment[0]

                # Remove the experiment from all its users
                for user in experiment_to_delete.users:
                    user.experiment.remove(experiment_to_delete)

                # Remove the experiment from all its samples
                for sample in experiment_to_delete.samples:
                    sample.experiment.remove(experiment_to_delete)

                session.delete(experiment_to_delete)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
