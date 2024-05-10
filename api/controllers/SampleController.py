from sqlalchemy import select
from api.db.db import DatabaseInstance
from api.db.models import Sample, User, Experiment


class SampleController:
    """
    This class is the way to interact with the samples in the database.
    The samples are the most important data stored in the database.
    The samples are associated with an experiment, thus they are related to a project.
    The samples are owned by an user, and can be shared with other users o with groups.
    It's possible that a samples doesn't have an owner, nor group nor experiment associated with it.
    """
    @classmethod
    def get_sample_by_id(cls, sample_id: int):
        with DatabaseInstance().session() as session:
            stmt = select(Sample).filter_by(id=sample_id)
            sample = session.execute(stmt).first()
            # session.close()
            return sample

    @classmethod
    def get_samples_by_user(cls, user_id: int):
        with DatabaseInstance().session() as session:
            stmt = select(Sample).filter_by(owner_id=user_id)
            samples = session.execute(stmt).all()
            # session.close()
            return samples

    @classmethod
    def get_samples_by_group(cls, group_id: int):
        with DatabaseInstance().session() as session:
            stmt = select(Sample).filter_by(group_id=group_id)
            samples = session.execute(stmt).all()
            # session.close()
            return samples

    @classmethod
    def get_samples_by_experiment(cls, experiment_id: int):
        with DatabaseInstance().session() as session:
            stmt = select(Sample).filter_by(experiment_id=experiment_id)
            samples = session.execute(stmt).all()
            # session.close()
            return samples

    @classmethod
    def create_sample(cls, sample_to_create: Sample):
        with DatabaseInstance().session() as session:
            try:
                # TODO: add the logic needed to add correctly the sample to the database
                session.add(sample_to_create)
                session.commit()
                stmt = select(Sample).filter_by(id=sample_to_create.id)
                sample_created = session.execute(stmt).first()[0]
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
            return sample_created

    @classmethod
    def update_sample(cls, sample_id: int, new_data: dict):
        with DatabaseInstance().session() as session:
            try:
                stmt = select(Sample).filter_by(id=sample_id)
                sample = session.execute(stmt).first()
                if sample is None:
                    raise Exception("Sample not found")
                sample_to_edit = sample[0]
                for key, value in new_data.items():
                    setattr(sample_to_edit, key, value)
                session.add(sample_to_edit)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()

    @classmethod
    def delete_sample(cls, sample_id: int):
        with DatabaseInstance().session() as session:
            try:
                stmt = select(Sample).filter_by(id=sample_id)
                sample = session.execute(stmt).first()
                if sample is None:
                    raise Exception("Sample not found")
                sample_to_delete = sample[0]
                session.delete(sample_to_delete)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()