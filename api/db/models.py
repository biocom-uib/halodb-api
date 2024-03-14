
from api.db.db import get_session, db


class HaloDBModel(db.Model):
    __abstract__ = True

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Author(HaloDBModel):
    __table__ = db.metadata.tables['author']

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Author {self.name}>'

    def __str__(self):
        return f'<Author {self.name}>'

    @staticmethod
    def get(self, id):
        return Author.query.get(id)

    @staticmethod
    def set(self, id, name):
        author = Author.query.get(id)
        author.name = name
        get_session().commit()

    @staticmethod
    def delete(self, id):
        author = Author.query.get(id)
        get_session().delete(author)
        get_session().commit()


class Experiment(HaloDBModel):
    __table__ = db.metadata.tables['experiment']

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Experiment {self.name}>'

    def __str__(self):
        return f'{self.name}'

    @staticmethod
    def get(self, id):
        return Experiment.query.get(id)

    @staticmethod
    def set(self, id, name):
        experiment = Experiment.query.get(id)
        experiment.name = name
        get_session().commit()

    @staticmethod
    def delete(self, id):
        experiment = Experiment.query.get(id)
        get_session().delete(experiment)
        get_session().commit()


class Fraction(HaloDBModel):
    __table__ = db.metadata.tables['fraction']

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Fraction {self.name}>'

    def __str__(self):
        return f'<Fraction {self.name}>'

    @staticmethod
    def get(self, id):
        return Fraction.query.get(id)

    @staticmethod
    def set(self, id, name):
        fraction = Fraction.query.get(id)
        fraction.name = name
        get_session().commit()

    @staticmethod
    def delete(self, id):
        fraction = Fraction.query.get(id)
        get_session().delete(fraction)
        get_session().commit()


class Group(HaloDBModel):
    __table__ = db.metadata.tables['group']

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Group {self.name}>'

    def __str__(self):
        return f'<Group {self.name}>'

    @staticmethod
    def get(self, id):
        return Group.query.get(id)

    @staticmethod
    def set(self, id, name):
        group = Group.query.get(id)
        group.name = name
        get_session().commit()

    @staticmethod
    def delete(self, id):
        group = Group.query.get(id)
        get_session().delete(group)
        get_session().commit()


class GroupSharingSample(HaloDBModel):
    __table__ = db.metadata.tables['group_sharing_sample']

    def __init__(self, group_id, sample_id):
        self.group_id = group_id
        self.sample_id = sample_id

    def __repr__(self):
        return f'<GroupSharingSample {self.group_id} {self.sample_id}>'

    def __str__(self):
        return f'<GroupSharingSample {self.group_id} {self.sample_id}>'

    @staticmethod
    def get(self, group_id, sample_id):
        return GroupSharingSample.query.get((group_id, sample_id))

    @staticmethod
    def set(self, group_id, sample_id):
        group_sharing_sample = GroupSharingSample.query.get((group_id, sample_id))
        group_sharing_sample.group_id = group_id
        group_sharing_sample.sample_id = sample_id
        get_session().commit()

    @staticmethod
    def delete(self, group_id, sample_id):
        group_sharing_sample = GroupSharingSample.query.get((group_id, sample_id))
        get_session().delete(group_sharing_sample)
        get_session().commit()


class Keywords(HaloDBModel):
    __table__ = db.metadata.tables['keywords']

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Keywords {self.name}>'

    def __str__(self):
        return f'<Keywords {self.name}>'

    @staticmethod
    def get(self, id):
        return Keywords.query.get(id)

    @staticmethod
    def set(self, id, name):
        keywords = Keywords.query.get(id)
        keywords.name = name
        get_session().commit()

    @staticmethod
    def delete(self, id):
        keywords = Keywords.query.get(id)
        get_session().delete(keywords)
        get_session().commit()


class Method(HaloDBModel):
    __table__ = db.metadata.tables['method']

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Method {self.name}>'

    def __str__(self):
        return f'<Method {self.name}>'

    def get(self, id):
        return Method.query.get(id)

    def set(self, id, name):
        method = Method.query.get(id)
        method.name = name
        get_session().commit()

    def delete(self, id):
        method = Method.query.get(id)
        get_session().delete(method)
        get_session().commit()


class Oxygen(HaloDBModel):

    __table__ = db.metadata.tables['oxygen']

    # __tablename__ = 'oxygen'

    # id = Column(Integer, primary_key=True)
    # relationship = Column(String(40), nullable=False)

    def __init__(self, relationship):
        self.relationship = relationship

    def __repr__(self):
        return f'<Oxygen {self.relationship}>'

    def __str__(self):
        return f'{self.relationship}'


    def save(self):
        get_session().add(self)
        get_session().commit()

    @staticmethod
    def get(self, id):
        return Oxygen.query.get(id)

    @staticmethod
    def set(self, id, relationship):
        oxygen = Oxygen.query.get(id)
        oxygen.relationship = relationship
        get_session().commit()

    @staticmethod
    def delete(self, id):
        oxygen = Oxygen.query.get(id)
        get_session().delete(oxygen)
        get_session().commit()


class Ph(HaloDBModel):
    __table__ = db.metadata.tables['ph']

    def __init__(self, relationship):
        self.relationship = relationship

    def __repr__(self):
        return f'<Ph {self.relationship}>'

    def __str__(self):
        return f'<Ph {self.relationship}>'

    @staticmethod
    def get(self, id):
        return Ph.query.get(id)

    @staticmethod
    def set(self, id, relationship):
        ph = Ph.query.get(id)
        ph.relationship = relationship
        get_session().commit()

    @staticmethod
    def delete(self, id):
        ph = Ph.query.get(id)
        get_session().delete(ph)
        get_session().commit()


class Project(HaloDBModel):
    __table__ = db.metadata.tables['project']

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Project {self.name}>'

    def __str__(self):
        return f'<Project {self.name}>'

    @staticmethod
    def get(self, id):
        return Project.query.get(id)

    @staticmethod
    def set(self, id, name):
        project = Project.query.get(id)
        project.name = name
        get_session().commit()

    @staticmethod
    def delete(self, id):
        project = Project.query.get(id)
        get_session().delete(project)
        get_session().commit()


class Salinity(HaloDBModel):
    __table__ = db.metadata.tables['salinity']

    def __init__(self, relationship):
        self.relationship = relationship

    def __repr__(self):
        return f'<Salinity {self.relationship}>'

    def __str__(self):
        return f'<Salinity {self.relationship}>'

    @staticmethod
    def get(self, id):
        return Salinity.query.get(id)

    @staticmethod
    def set(self, id, relationship):
        salinity = Salinity.query.get(id)
        salinity.relationship = relationship
        get_session().commit()


class Sample(HaloDBModel):
    __table__ = db.metadata.tables['sample']

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Sample {self.name}>'

    def __str__(self):
        return f'<Sample {self.name}>'

    @staticmethod
    def get(self, id):
        return Sample.query.get(id)

    @staticmethod
    def set(self, id, name):
        sample = Sample.query.get(id)
        sample.name = name
        get_session().commit()

    @staticmethod
    def delete(self, id):
        sample = Sample.query.get(id)
        get_session().delete(sample)
        get_session().commit()


class SampleHasKeywords(HaloDBModel):
    __table__ = db.metadata.tables['sample_has_keywords']

    def __init__(self, sample_id, keywords_id):
        self.sample_id = sample_id
        self.keywords_id = keywords_id

    def __repr__(self):
        return f'<SampleHasKeywords {self.sample_id} {self.keywords_id}>'

    def __str__(self):
        return f'<SampleHasKeywords {self.sample_id} {self.keywords_id}>'

    @staticmethod
    def get(self, sample_id, keywords_id):
        return SampleHasKeywords.query.get((sample_id, keywords_id))

    @staticmethod
    def set(self, sample_id, keywords_id):
        sample_has_keywords = SampleHasKeywords.query.get((sample_id, keywords_id))
        sample_has_keywords.sample_id = sample_id
        sample_has_keywords.keywords_id = keywords_id
        get_session().commit()

    @staticmethod
    def delete(self, sample_id, keywords_id):
        sample_has_keywords = SampleHasKeywords.query.get((sample_id, keywords_id))
        get_session().delete(sample_has_keywords)
        get_session().commit()


class Target(HaloDBModel):
    __table__ = db.metadata.tables['target']

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Target {self.name}>'

    def __str__(self):
        return f'<Target {self.name}>'

    @staticmethod
    def get(self, id):
        return Target.query.get(id)

    @staticmethod
    def set(self, id, name):
        target = Target.query.get(id)
        target.name = name
        get_session().commit()

    @staticmethod
    def delete(self, id):
        target = Target.query.get(id)
        get_session().delete(target)
        get_session().commit()


class Temperature(HaloDBModel):
    __table__ = db.metadata.tables['temperature']

    def __init__(self, relationship):
        self.relationship = relationship

    def __repr__(self):
        return f'<Temperature {self.relationship}>'

    def __str__(self):
        return f'<Temperature {self.relationship}>'

    @staticmethod
    def get(self, id):
        return Temperature.query.get(id)


    @staticmethod
    def set(self, id, relationship):
        temperature = Temperature.query.get(id)
        temperature.relationship = relationship
        get_session().commit()

    @staticmethod
    def delete(self, id):
        temperature = Temperature.query.get(id)
        get_session().delete(temperature)
        get_session().commit()

class User(HaloDBModel):
    __table__ = db.metadata.tables['user']

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<User {self.name}>'

    def __str__(self):
        return f'<User {self.name}>'

    @staticmethod
    def get(self, id):
        return User.query.get(id)

    @staticmethod
    def set(self, id, name):
        user = User.query.get(id)
        user.name = name
        get_session().commit()

    @staticmethod
    def delete(self, id):
        user = User.query.get(id)
        get_session().delete(user)
        get_session().commit()


class UserExperiment(HaloDBModel):
    __table__ = db.metadata.tables['user_experiment']

    def __init__(self, user_id, experiment_id):
        self.user_id = user_id
        self.experiment_id = experiment_id

    def __repr__(self):
        return f'<UserExperiment {self.user_id} {self.experiment_id}>'

    def __str__(self):
        return f'<UserExperiment {self.user_id} {self.experiment_id}>'

    @staticmethod
    def get(self, user_id, experiment_id):
        return UserExperiment.query.get((user_id, experiment_id))

    @staticmethod
    def set(self, user_id, experiment_id):
        user_experiment = UserExperiment.query.get((user_id, experiment_id))
        user_experiment.user_id = user_id
        user_experiment.experiment_id = experiment_id
        get_session().commit()

    @staticmethod
    def delete(self, user_id, experiment_id):
        user_experiment = UserExperiment.query.get((user_id, experiment_id))
        get_session().delete(user_experiment)
        get_session().commit()


class UserHasGroup(HaloDBModel):
    __table__ = db.metadata.tables['user_has_group']

    def __init__(self, user_id, group_id):
        self.user_id = user_id
        self.group_id = group_id

    def __repr__(self):
        return f'<UserHasGroup {self.user_id} {self.group_id}>'

    def __str__(self):
        return f'<UserHasGroup {self.user_id} {self.group_id}>'

    @staticmethod
    def get(self, user_id, group_id):
        return UserHasGroup.query.get((user_id, group_id))

    @staticmethod
    def set(self, user_id, group_id):
        user_has_group = UserHasGroup.query.get((user_id, group_id))
        user_has_group.user_id = user_id
        user_has_group.group_id = group_id
        get_session().commit()

    @staticmethod
    def delete(self, user_id, group_id):
        user_has_group = UserHasGroup.query.get((user_id, group_id))
        get_session().delete(user_has_group)
        get_session().commit()


class UserProject(HaloDBModel):
    __table__ = db.metadata.tables['user_project']

    def __init__(self, user_id, project_id):
        self.user_id = user_id
        self.project_id = project_id

    def __repr__(self):
        return f'<UserProject {self.user_id} {self.project_id}>'

    def __str__(self):
        return f'<UserProject {self.user_id} {self.project_id}>'

    @staticmethod
    def get(self, user_id, project_id):
        return UserProject.query.get((user_id, project_id))

    @staticmethod
    def set(self, user_id, project_id):
        user_project = UserProject.query.get((user_id, project_id))
        user_project.user_id = user_id
        user_project.project_id = project_id
        get_session().commit()

    @staticmethod
    def delete(self, user_id, project_id):
        user_project = UserProject.query.get((user_id, project_id))
        get_session().delete(user_project)
        get_session().commit()


class UserSharedSample(HaloDBModel):
    __table__ = db.metadata.tables['user_shared_sample']

    def __init__(self, user_id, sample_id):
        self.user_id = user_id
        self.sample_id = sample_id

    def __repr__(self):
        return f'<UserSharedSample {self.user_id} {self.sample_id}>'

    def __str__(self):
        return f'<UserSharedSample {self.user_id} {self.sample_id}>'

    @staticmethod
    def get(self, user_id, sample_id):
        return UserSharedSample.query.get((user_id, sample_id))

    @staticmethod
    def set(self, user_id, sample_id):
        user_shared_sample = UserSharedSample.query.get((user_id, sample_id))
        user_shared_sample.user_id = user_id
        user_shared_sample.sample_id = sample_id
        get_session().commit()

    @staticmethod
    def delete(self, user_id, sample_id):
        user_shared_sample = UserSharedSample.query.get((user_id, sample_id))
        get_session().delete(user_shared_sample)
        get_session().commit()
