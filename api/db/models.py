import datetime
import os

import uuid

from api.config import UPLOADS_DIR
from api.db import db
from api.db.db import DatabaseInstance

if DatabaseInstance.get() is None:
    raise RuntimeError('The database has not been initialized yet, this module should be imported later')


class HaloDatabaseInstanceModel(db.Base):
    __abstract__ = True

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def from_dict(self, data):
        for field in data:
            if field in self.__table__.columns:
                setattr(self, field, data[field])


class Author(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get().get_table('author')

    def __init__(self, name, **kw: any):
        super().__init__(**kw)
        self.name = name

    def __repr__(self):
        return f'<Author {self.name}>'

    def __str__(self):
        return f'<Author {self.name}>'

    @staticmethod
    def find_by_user(user_id):
        return Author.query.filter(Author.user_id == user_id).first()

    @staticmethod
    def save(author):
        session = DatabaseInstance.get().session()
        session.add(author)
        session.commit()

    @staticmethod
    def get(id):
        return Author.query.get(id)

    @staticmethod
    def set(id, name):
        author = Author.query.get(id)
        author.name = name
        DatabaseInstance.get().session().commit()

    @staticmethod
    def delete(id):
        author = Author.query.get(id)
        session = DatabaseInstance.get().session()
        session.delete(author)
        session.commit()


class Experiment(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get().get_table('experiment')

    def __init__(self, name, **kw: any):
        super().__init__(**kw)
        self.name = name

    def __repr__(self):
        return f'<Experiment {self.name}>'

    def __str__(self):
        return f'{self.name}'

    @staticmethod
    def get(id):
        return Experiment.query.get(id)

    @staticmethod
    def set(id, name):
        experiment = Experiment.query.get(id)
        experiment.name = name
        DatabaseInstance.get().session().commit()

    @staticmethod
    def delete(id):
        experiment = Experiment.query.get(id)
        DatabaseInstance.get().session().delete(experiment)
        DatabaseInstance.get().session().commit()


class Fraction(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get().get_table('fraction')

    def __init__(self, name, **kw: any):
        super().__init__(**kw)
        self.name = name

    def __repr__(self):
        return f'<Fraction {self.name}>'

    def __str__(self):
        return f'<Fraction {self.name}>'

    @staticmethod
    def get(id):
        return Fraction.query.get(id)

    @staticmethod
    def set(id, name):
        fraction = Fraction.query.get(id)
        fraction.name = name
        DatabaseInstance.get().session().commit()

    @staticmethod
    def delete(id):
        fraction = Fraction.query.get(id)
        DatabaseInstance.get().session().delete(fraction)
        DatabaseInstance.get().session().commit()


class Group(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get().get_table('group')

    def __init__(self, name, **kw: any):
        super().__init__()
        self.name = name

    def __repr__(self):
        return f'<Group {self.name}>'

    def __str__(self):
        return f'<Group {self.name}>'

    @staticmethod
    def get(id):
        return Group.query.get(id)

    @staticmethod
    def set(id, name):
        group = Group.query.get(id)
        group.name = name
        DatabaseInstance.get().session().commit()

    @staticmethod
    def delete(id):
        group = Group.query.get(id)
        DatabaseInstance.get().session().delete(group)
        DatabaseInstance.get().session().commit()


class GroupSharingSample(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get().get_table('group_sharing_sample')

    def __init__(self, **kw: any):
        super().__init__(**kw)

    def __repr__(self):
        return f'<GroupSharingSample {self.group_id} {self.sample_id}>'

    def __str__(self):
        return f'<GroupSharingSample {self.group_id} {self.sample_id}>'

    @staticmethod
    def get(group_id, sample_id):
        return GroupSharingSample.query.get((group_id, sample_id))

    @staticmethod
    def set(group_id, sample_id):
        group_sharing_sample = GroupSharingSample.query.get((group_id, sample_id))
        group_sharing_sample.group_id = group_id
        group_sharing_sample.sample_id = sample_id
        DatabaseInstance.get().session().commit()

    @staticmethod
    def delete(group_id, sample_id):
        group_sharing_sample = GroupSharingSample.query.get((group_id, sample_id))
        DatabaseInstance.get().session().delete(group_sharing_sample)
        DatabaseInstance.get().session().commit()


class Keywords(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get().get_table('keywords')

    def __init__(self, name, **kw: any):
        super().__init__(**kw)
        self.name = name

    def __repr__(self):
        return f'<Keywords {self.name}>'

    def __str__(self):
        return f'<Keywords {self.name}>'

    @staticmethod
    def get(id):
        return Keywords.query.get(id)

    @staticmethod
    def set(id, name):
        keywords = Keywords.query.get(id)
        keywords.name = name
        DatabaseInstance.get().session().commit()

    @staticmethod
    def delete(id):
        keywords = Keywords.query.get(id)
        DatabaseInstance.get().session().delete(keywords)
        DatabaseInstance.get().session().commit()


class Method(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get().get_table('method')

    def __init__(self, name, **kw: any):
        super().__init__(**kw)
        self.name = name

    def __repr__(self):
        return f'<Method {self.name}>'

    def __str__(self):
        return f'<Method {self.name}>'

    def get(id):
        return Method.query.get(id)

    def set(id, name):
        method = Method.query.get(id)
        method.name = name
        DatabaseInstance.get().session().commit()

    def delete(id):
        method = Method.query.get(id)
        DatabaseInstance.get().session().delete(method)
        DatabaseInstance.get().session().commit()


class Oxygen(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get().get_table('oxygen')

    # __tablename__ = 'oxygen'

    # id = Column(Integer, primary_key=True)
    # relationship = Column(String(40), nullable=False)

    def __init__(self, relationship, **kw: any):
        super().__init__(**kw)
        self.relationship = relationship

    def __repr__(self):
        return f'<Oxygen {self.relationship}>'

    def __str__(self):
        return f'{self.relationship}'

    @staticmethod
    def get(id):
        return Oxygen.query.get(id)

    @staticmethod
    def set(id, relationship):
        oxygen = Oxygen.query.get(id)
        oxygen.relationship = relationship
        DatabaseInstance.get().session().commit()

    @staticmethod
    def delete(id):
        oxygen = Oxygen.query.get(id)
        DatabaseInstance.get().session().delete(oxygen)
        DatabaseInstance.get().session().commit()


class Ph(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get().get_table('ph')

    def __init__(self, relationship, **kw: any):
        super().__init__(**kw)
        self.relationship = relationship

    def __repr__(self):
        return f'<Ph {self.relationship}>'

    def __str__(self):
        return f'<Ph {self.relationship}>'

    @staticmethod
    def get(id):
        return Ph.query.get(id)

    @staticmethod
    def set(id, relationship):
        ph = Ph.query.get(id)
        ph.relationship = relationship
        DatabaseInstance.get().session().commit()

    @staticmethod
    def delete(id):
        ph = Ph.query.get(id)
        DatabaseInstance.get().session().delete(ph)
        DatabaseInstance.get().session().commit()


class Project(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get().get_table('project')

    def __init__(self, name, **kw: any):
        super().__init__(**kw)
        self.name = name

    def __repr__(self):
        return f'<Project {self.name}>'

    def __str__(self):
        return f'<Project {self.name}>'

    @staticmethod
    def get(id):
        return Project.query.get(id)

    @staticmethod
    def set(id, name):
        project = Project.query.get(id)
        project.name = name
        DatabaseInstance.get().session().commit()

    @staticmethod
    def delete(id):
        project = Project.query.get(id)
        DatabaseInstance.get().session().delete(project)
        DatabaseInstance.get().session().commit()


class Salinity(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get().get_table('salinity')

    def __init__(self, relationship, **kw: any):
        super().__init__(**kw)
        self.relationship = relationship

    def __repr__(self):
        return f'<Salinity {self.relationship}>'

    def __str__(self):
        return f'<Salinity {self.relationship}>'

    @staticmethod
    def get(id):
        return Salinity.query.get(id)

    @staticmethod
    def set(id, relationship):
        salinity = Salinity.query.get(id)
        salinity.relationship = relationship
        DatabaseInstance.get().session().commit()


class Sample(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get().get_table('sample')

    def __init__(self, **kw: any):
        super().__init__(**kw)

    def __repr__(self):
        return f'<Sample {self.id}>'

    def __str__(self):
        return f'<Sample {self.id}>'

    __file_fields__ = {
        "rreads": "rrname",
        "treads": "trname",
        "assembled": "assname",
        "pgenes": "pgenesname"
                   }

    __forbidden_files__ = [
        "created", "updated", "id", "is_public", "experiment_id"
    ]

    @classmethod
    def is_file_field(cls, field):
        return field in cls.__file_fields__.keys()

    @classmethod
    def get_file_name_field(cls, field):
        if cls.is_file_field(field):
            return cls.__file_fields__[field]
        return None

    @classmethod
    def exclude_param_files(cls, params: dict):
        return {k: v for k, v in params.items()
                if k not in cls.__file_fields__.keys() and k not in cls.__file_fields__.values()}

    @classmethod
    def exclude_forbidden_fields(cls, params: dict):
        return {k: v for k, v in params.items() if k not in cls.__forbidden_files__}

    @classmethod
    def valid_field(cls, field):
        return (field not in cls.__file_fields__.keys() and
                field not in cls.__file_fields__.values() and
                field not in cls.__forbidden_files__)

    @staticmethod
    def get(id):
        return Sample.query.get(id)

    def get_file_data(self, field):
        if not Sample.is_file_field(field):
            raise Exception("The field is not a file")

        filedata = getattr(self, field)
        filename = getattr(self, Sample.get_file_name_field(field))

        return filename, open(os.path.join(UPLOADS_DIR, filedata), 'rb')

    def add_file(self, field, file_data, filename_field, filename):
        if not self.is_file_field(field):
            raise Exception("The field is not a file")

        uuid_file = getattr(self, field)
        if uuid_file is None:
            uuid_file = str(uuid.uuid4())
            setattr(self, field, uuid_file)

        setattr(self, Sample.get_file_name_field(field), filename)
        setattr(self, "updated", datetime.datetime.now())
        file_data.save(os.path.join(UPLOADS_DIR, uuid_file))


    @staticmethod
    def set(id, name):
        sample = Sample.query.get(id)
        sample.name = name
        DatabaseInstance.get().session().commit()

    @staticmethod
    def find_by_user(user_id):
        return Sample.query.filter(Sample.user_id == user_id).all()

    @staticmethod
    def delete(id):
        sample = Sample.query.get(id)
        session = DatabaseInstance.get().session()
        session.delete(sample)
        session.commit()


class SampleHasKeywords(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get().get_table('sample_has_keywords')

    def __init__(self, sample_id, keywords_id, **kw: any):
        super().__init__(**kw)
        self.sample_id = sample_id
        self.keywords_id = keywords_id

    def __repr__(self):
        return f'<SampleHasKeywords {self.sample_id} {self.keywords_id}>'

    def __str__(self):
        return f'<SampleHasKeywords {self.sample_id} {self.keywords_id}>'

    @staticmethod
    def get(sample_id, keywords_id):
        return SampleHasKeywords.query.get((sample_id, keywords_id))

    @staticmethod
    def set(sample_id, keywords_id):
        sample_has_keywords = SampleHasKeywords.query.get((sample_id, keywords_id))
        sample_has_keywords.sample_id = sample_id
        sample_has_keywords.keywords_id = keywords_id
        DatabaseInstance.get().session().commit()

    @staticmethod
    def delete(sample_id, keywords_id):
        sample_has_keywords = SampleHasKeywords.query.get((sample_id, keywords_id))
        DatabaseInstance.get().session().delete(sample_has_keywords)
        DatabaseInstance.get().session().commit()


class Target(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get().get_table('target')

    def __init__(self, name, **kw: any):
        super().__init__(**kw)
        self.name = name

    def __repr__(self):
        return f'<Target {self.name}>'

    def __str__(self):
        return f'<Target {self.name}>'

    @staticmethod
    def get(id):
        return Target.query.get(id)

    @staticmethod
    def set(id, name):
        target = Target.query.get(id)
        target.name = name
        DatabaseInstance.get().session().commit()

    @staticmethod
    def delete(id):
        target = Target.query.get(id)
        DatabaseInstance.get().session().delete(target)
        DatabaseInstance.get().session().commit()


class Temperature(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get().get_table('temperature')

    def __init__(self, relationship, **kw: any):
        super().__init__(**kw)
        self.relationship = relationship

    def __repr__(self):
        return f'<Temperature {self.relationship}>'

    def __str__(self):
        return f'<Temperature {self.relationship}>'

    @staticmethod
    def get(id):
        return Temperature.query.get(id)

    @staticmethod
    def set(id, relationship):
        temperature = Temperature.query.get(id)
        temperature.relationship = relationship
        DatabaseInstance.get().session().commit()

    @staticmethod
    def delete(id):
        temperature = Temperature.query.get(id)
        DatabaseInstance.get().session().delete(temperature)
        DatabaseInstance.get().session().commit()


class User(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get().get_table('user')

    def __init__(self, name, **kw: any):
        super().__init__(**kw)
        self.name = name

    def __repr__(self):
        return f'<User {self.name}>'

    def __str__(self):
        return f'<User {self.name}>'

    @staticmethod
    def get(id):
        return User.query.get(id)

    @staticmethod
    def get_by_uid(uid: str):
        return User.query.filter(User.uid == uid).first()
        # return DatabaseInstance.get().session().query(User).filter(User.uid == uid).first()

    @staticmethod
    def get_by_email(email: str):
        return User.query.filter(User.email == email).first()

    @staticmethod
    def set(id, name):
        user = User.query.get(id)
        user.name = name

    @staticmethod
    def delete(user_id):
        user = User.query.get(user_id)
        session = DatabaseInstance.get().session()
        session.delete(user)
        session.commit()

    @staticmethod
    def save(user):
        session = DatabaseInstance.get().session()
        session.add(user)
        session.commit()


class UserExperiment(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get().get_table('user_experiment')

    def __init__(self, user_id, experiment_id, **kw: any):
        super().__init__(**kw)
        self.user_id = user_id
        self.experiment_id = experiment_id

    def __repr__(self):
        return f'<UserExperiment {self.user_id} {self.experiment_id}>'

    def __str__(self):
        return f'<UserExperiment {self.user_id} {self.experiment_id}>'

    @staticmethod
    def get(user_id, experiment_id):
        return UserExperiment.query.get((user_id, experiment_id))

    @staticmethod
    def set(user_id, experiment_id):
        user_experiment = UserExperiment.query.get((user_id, experiment_id))
        user_experiment.user_id = user_id
        user_experiment.experiment_id = experiment_id
        DatabaseInstance.get().session().commit()

    @staticmethod
    def delete(user_id, experiment_id):
        user_experiment = UserExperiment.query.get((user_id, experiment_id))
        DatabaseInstance.get().session().delete(user_experiment)
        DatabaseInstance.get().session().commit()


class UserHasGroup(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get().get_table('user_has_group')

    def __init__(self, user_id, group_id, relation, **kw: any):
        super().__init__(**kw)
        self.user_id = user_id
        self.group_id = group_id
        self.relation = relation

    def __repr__(self):
        return f'<UserHasGroup {self.user_id} {self.group_id}>'

    def __str__(self):
        return f'<UserHasGroup {self.user_id} {self.group_id}>'

    @staticmethod
    def get(user_id, group_id):
        return UserHasGroup.query.get(user_id=user_id, group_id=group_id)

    @staticmethod
    def set(user_id, group_id):
        user_has_group = UserHasGroup.query.get((user_id, group_id))
        user_has_group.user_id = user_id
        user_has_group.group_id = group_id
        DatabaseInstance.get().session().commit()

    @staticmethod
    def delete(user_id, group_id):
        user_has_group = UserHasGroup.query.get((user_id, group_id))
        DatabaseInstance.get().session().delete(user_has_group)
        DatabaseInstance.get().session().commit()


class UserProject(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get().get_table('user_project')

    def __init__(self, user_id, project_id, **kw:any):
        super().__init__(**kw)
        self.user_id = user_id
        self.project_id = project_id

    def __repr__(self):
        return f'<UserProject {self.user_id} {self.project_id}>'

    def __str__(self):
        return f'<UserProject {self.user_id} {self.project_id}>'

    @staticmethod
    def get(user_id, project_id):
        return UserProject.query.get((user_id, project_id))

    @staticmethod
    def set(user_id, project_id):
        user_project = UserProject.query.get((user_id, project_id))
        user_project.user_id = user_id
        user_project.project_id = project_id
        DatabaseInstance.get().session().commit()

    @staticmethod
    def delete(user_id, project_id):
        user_project = UserProject.query.get((user_id, project_id))
        DatabaseInstance.get().session().delete(user_project)
        DatabaseInstance.get().session().commit()


class UserSharedSample(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get().get_table('user_shared_sample')

    def __init__(self, **kw: any):
        super().__init__(**kw)

    def __repr__(self):
        return f'<UserSharedSample {self.user_id} {self.sample_id}>'

    def __str__(self):
        return f'<UserSharedSample {self.user_id} {self.sample_id}>'


