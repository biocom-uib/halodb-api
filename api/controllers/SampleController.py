import datetime

from sqlalchemy import select

from api.db.db import DatabaseInstance
from api.db.models import Sample, UserSharedSample, Group, GroupSharingSample, UserHasGroup, Temperature, Ph, Salinity, \
    Method, Oxygen, Fraction, Target, Extraction, Assembly, Sequencing, Binning
from api.utils import convert_to_dict, to_dict


class SampleController:
    """
    This class is the way to interact with the samples in the database.
    The samples are the most important data stored in the database.
    The samples are associated with an experiment, thus they are related to a project.
    The samples are owned by a user, and can be shared with other users o with groups.
    It's possible that a samples doesn't have an owner, nor group nor experiment associated with it.
    """

    @classmethod
    def get_sample_by_id(cls, sample_id: int):
        with DatabaseInstance.get().session() as session:
            stmt = select(Sample).filter_by(id=sample_id)
            sample = session.execute(stmt).first()
            if sample is not None:
                sample = sample[0]

        return sample

    @classmethod
    def get_samples_owned_by_user(cls, user_id: int):
        with DatabaseInstance.get().session() as session:
            stmt = select(Sample).filter_by(user_id=user_id)
            samples = session.execute(stmt).all()

        return samples

    @classmethod
    def filter_description_fields(cls, sample):
        complementaries = {
            # "publication": "publication",
            # "hkgn": "",
            "method": "method",
            "dnae": "extraction",
            "asem": "assembly",
            "seqt": "sequencing",
            "bins": "binning",
            "orel": "oxygen",
            "sfrac": "fraction",
            "target": "target"
        }
        supplementaries = {
            "temc": {"field": "temo", "table": "temperature"},
            "phca": {"field": "phop", "table": "ph"},
            "salc": {"field": "salo", "table": "salinity"}
        }
        # with DatabaseInstance.get() as session:
        for key, value in complementaries.items():
            if sample[key] is not None:
                # stmt = select(value).filter_by(id=sample[key])
                # result = session.execute(stmt).first()
                # if result is not None:
                #     sample[key] = result[0]
                if value == 'method':
                    element = Method.query.filter_by(id=sample[key]).first()
                elif value == 'extraction':
                    element = Extraction.query.filter_by(id=sample[key]).first()
                elif value == 'assembly':
                    element = Assembly.query.filter_by(id=sample[key]).first()
                elif value == 'sequencing':
                    element = Sequencing.query.filter_by(id=sample[key]).first()
                elif value == 'binning':
                    element = Binning.query.filter_by(id=sample[key]).first()
                elif value == 'oxygen':
                    element = Oxygen.query.filter_by(id=sample[key]).first()
                elif value == 'fraction':
                    element = Fraction.query.filter_by(id=sample[key]).first()
                elif value == 'target':
                    element = Target.query.filter_by(id=sample[key]).first()
                elif value == 'target':
                    element = Target.query.filter_by(id=sample[key]).first()
                else:
                    element = None

                if element is not None:
                    sample[key] = element.description
                else:
                    sample[key] = None
        for key, value in supplementaries.items():
            v = sample[value['field']]
            if sample[value['field']] is not None:
                # stmt = select(value['table']).filter_by(vmin<=v and v=vmax)
                #  result = session.execute(stmt).first()
                # if result is not None:
                #    sample[key] = result[0]
                if value['table'] == 'temperature':
                    element = Temperature.query.filter(Temperature.vmin < v, v <= Temperature.vmax).first()
                elif value['table'] == 'ph':
                    element = Ph.query.filter(Ph.vmin < v, v <= Ph.vmax).first()
                elif value['table'] == 'salinity':
                    element = Salinity.query.filter(Salinity.vmin < v, v <= Salinity.vmax).first()
                else:
                    element = None

                if element is not None:
                    sample[key] = element.description
                else:
                    sample[key] = None
        return sample

    @classmethod
    def get_samples_shared_with_user(cls, user_id):
        with DatabaseInstance.get().cursor() as cursor:
            cursor.callproc("get_samples_available", [user_id])
            column_names = [desc[0] for desc in cursor.description]
            result = list(cursor.fetchall())

        data = [cls.filter_description_fields(convert_to_dict(row, column_names)) for row in result]

        return data

    @classmethod
    def get_samples_by_experiment(cls, experiment_id: int):
        with DatabaseInstance.get().session() as session:
            stmt = select(Sample).filter_by(experiment_id=experiment_id)
            samples = session.execute(stmt).all()

        return samples

    __date_fields__ = ["dats",
                       "dati"]
    __time_fields__ = ["hocs"]

    @classmethod
    def fix_times(cls, data: dict):
        for key in cls.__date_fields__:
            if key in data.keys():
                data[key] = datetime.datetime.strptime(data[key], '%d/%m/%Y')
        for key in cls.__time_fields__:
            if key in data.keys():
                data[key] = datetime.datetime.strptime(data[key], '%H:%M:%S')

    @classmethod
    def create_sample(cls, data: dict):
        with DatabaseInstance.get().session() as session:
            try:
                sample_to_create = Sample()
                cls.fix_times(data)

                sample_to_create.from_dict(data)

                session.add(sample_to_create)

                session.commit()
                return sample_to_create.as_dict()
            except Exception as e:
                session.rollback()
                raise e

    @classmethod
    def update_file(cls, sample_id: int, file_id: str, file_name: str, file_data: bytes):
        with DatabaseInstance.get().session() as session:
            try:
                if not Sample.is_file_field(file_id):
                    raise Exception("The field is not a file")

                filename_field = Sample.get_file_name_field(file_id)

                stmt = select(Sample).filter_by(id=sample_id)
                sample = session.execute(stmt).first()
                if sample is None:
                    raise Exception("Sample not found")
                sample_to_edit = sample[0]

                sample_to_edit.add_file(file_id, file_data, filename_field, file_name)

                session.add(sample_to_edit)

                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    @classmethod
    def update_sample(cls, sample_id: int, new_data: dict):
        with DatabaseInstance.get().session() as session:
            try:
                stmt = select(Sample).filter_by(id=sample_id)
                sample = session.execute(stmt).first()
                if sample is None:
                    raise Exception("Sample not found")
                sample_to_edit = sample[0]

                cls.fix_times(new_data)

                for key, value in new_data.items():
                    if Sample.valid_field(key):
                        setattr(sample_to_edit, key, value)

                setattr(sample_to_edit, 'updated', datetime.datetime.now())

                session.add(sample_to_edit)
                result = sample_to_edit.as_dict()
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
        return result

    @classmethod
    def delete_sample(cls, sample_id: int):
        with DatabaseInstance.get().session() as session:
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

    @classmethod
    def list_samples(cls):
        return to_dict(Sample.query.all())

    __extra_headers__ = ['public', 'owned', 'shared_by_group', 'shared_by_others', 'access_mode',
                         'group_relation', 'group_id', 'group_name']
    __extra_values__ = [1, 0, 0, 0, 'read', None, None, None]

    @staticmethod
    def merge_extra_fields(sample):
        keys = list(sample.keys())
        values = list(sample.values())
        merged_keys = SampleController.__extra_headers__ + keys
        merged_values = SampleController.__extra_values__ + values
        return convert_to_dict(merged_values, merged_keys)

    @classmethod
    def list_public_samples(cls):
        samples = Sample.query.filter_by(is_public=True).all()
        samples = [cls.filter_description_fields(cls.merge_extra_fields(sample.as_dict())) for sample in samples]
        return samples

    @classmethod
    def get_access_mode(cls, user_id, sample_id: int):
        accessible_list = cls.get_samples_shared_with_user(user_id)
        for sample in accessible_list:
            if sample['id'] == sample_id:
                return sample['access_mode']
        return None

    @classmethod
    def make_public(cls, sample_id, owner):
        with DatabaseInstance.get().session() as session:
            try:
                sample = session.query(Sample).filter_by(id=sample_id).first()

                if sample is None:
                    raise Exception("Sample not found")

                if sample.user_id != owner:
                    raise Exception("User is not the owner of the sample")

                setattr(sample, 'is_public', 1)

                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    @classmethod
    def share_sample_user(cls, owner: int, sample_id: int, user_id: int, readwrite: bool):
        with DatabaseInstance.get().session() as session:
            try:
                sample = Sample.query.filter_by(id=sample_id).first()
                # stmt = select(Sample).filter_by(id=sample_id)
                # sample = session.execute(stmt).first()
                if sample is None:
                    raise Exception("Sample not found")

                if sample.user_id != owner:
                    raise Exception("User is not the owner of the sample")

                shared_sample = session.query(UserSharedSample).filter_by(sample_id=sample_id, user_id=user_id).first()
                if shared_sample is None:
                    shared_sample = UserSharedSample()
                    shared_sample.sample_id = sample_id
                    shared_sample.user_id = user_id
                    shared_sample.access_mode = "readwrite" if readwrite else "read"
                    session.add(shared_sample)
                else:
                    setattr(shared_sample, 'access_mode', 'readwrite' if readwrite else 'read')

                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    @classmethod
    def unshare_sample_user(cls, sample_id, user_id):
        with DatabaseInstance.get().session() as session:
            try:
                shared_sample = session.query(UserSharedSample).filter_by(sample_id=sample_id, user_id=user_id).first()
                if shared_sample is None:
                    raise Exception(f"User {user_id} doesn't have access to sample {sample_id}")

                session.delete(shared_sample)

                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    @classmethod
    def verify_relation(cls, owner, sample_id, group_id):
        sample = Sample.query.filter_by(id=sample_id).first()
        if sample is None:
            raise Exception(f"Sample {sample_id} not found")

        if sample.user_id != owner:
            raise Exception(f"User {owner} is not the owner of the sample")

        group = Group.query.filter_by(id=group_id).first()
        if group is None:
            raise Exception(f"The group {group_id} doesn't exist")

        owner_group = UserHasGroup.query.filter_by(user_id=owner, group_id=group_id).first()
        if owner_group is None or owner_group.relation != 'owner':
            raise Exception(f"User {owner} doesn't have the right privileges to share "
                            f"or remove the sample {sample_id}  to the group {group}")

    @classmethod
    def share_sample_group(cls, owner, sample_id, group_id, readwrite):
        with DatabaseInstance.get().session() as session:
            try:
                cls.verify_relation(owner, sample_id, group_id)

                shared_sample = session.query(GroupSharingSample).filter_by(
                    sample_id=sample_id, group_id=group_id).first()
                if shared_sample is None:
                    shared_sample = GroupSharingSample()
                    shared_sample.sample_id = sample_id
                    shared_sample.group_id = group_id
                    shared_sample.access_mode = "readwrite" if readwrite else "read"
                    session.add(shared_sample)
                else:
                    setattr(shared_sample, 'access_mode', 'readwrite' if readwrite else 'read')

                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    @classmethod
    def unshare_sample_group(cls, owner, sample_id, group_id):
        with DatabaseInstance.get().session() as session:
            try:
                cls.verify_relation(owner, sample_id, group_id)

                shared_sample = session.query(GroupSharingSample).filter_by(
                    sample_id=sample_id, group_id=group_id).first()

                if shared_sample is not None:
                    session.delete(shared_sample)
                    session.commit()
                else:
                    session.rollback()
                    raise Exception(f"Sample {sample_id} isn't shared with group {group_id}")

            except Exception as e:
                session.rollback()
                raise e

