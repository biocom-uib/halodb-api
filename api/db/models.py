from api.db import db
from api.db.db import DatabaseInstance


class HaloDatabaseInstanceModel(db.Base):
    __abstract__ = True

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Author(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get_table('author')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Author {self.name}>'

    def __str__(self):
        return f'<Author {self.name}>'

    @staticmethod
    def get(id):
        return Author.query.get(id)

    @staticmethod
    def set(id, name):
        author = Author.query.get(id)
        author.name = name
        DatabaseInstance.get_session().commit()

    @staticmethod
    def delete(id):
        author = Author.query.get(id)
        DatabaseInstance.get_session().delete(author)
        DatabaseInstance.get_session().commit()


class Experiment(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get_table('experiment')

    def __init__(self, name):
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
        DatabaseInstance.get_session().commit()

    @staticmethod
    def delete(id):
        experiment = Experiment.query.get(id)
        DatabaseInstance.get_session().delete(experiment)
        DatabaseInstance.get_session().commit()


class Fraction(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get_table('fraction')

    def __init__(self, name):
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
        DatabaseInstance.get_session().commit()

    @staticmethod
    def delete(id):
        fraction = Fraction.query.get(id)
        DatabaseInstance.get_session().delete(fraction)
        DatabaseInstance.get_session().commit()


class Group(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get_table('group')

    def __init__(self, name):
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
        DatabaseInstance.get_session().commit()

    @staticmethod
    def delete(id):
        group = Group.query.get(id)
        DatabaseInstance.get_session().delete(group)
        DatabaseInstance.get_session().commit()


class GroupSharingSample(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get_table('group_sharing_sample')

    def __init__(self, group_id, sample_id):
        self.group_id = group_id
        self.sample_id = sample_id

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
        DatabaseInstance.get_session().commit()

    @staticmethod
    def delete(group_id, sample_id):
        group_sharing_sample = GroupSharingSample.query.get((group_id, sample_id))
        DatabaseInstance.get_session().delete(group_sharing_sample)
        DatabaseInstance.get_session().commit()


class Keywords(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get_table('keywords')

    def __init__(self, name):
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
        DatabaseInstance.get_session().commit()

    @staticmethod
    def delete(id):
        keywords = Keywords.query.get(id)
        DatabaseInstance.get_session().delete(keywords)
        DatabaseInstance.get_session().commit()


class Method(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get_table('method')

    def __init__(self, name):
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
        DatabaseInstance.get_session().commit()

    def delete(id):
        method = Method.query.get(id)
        DatabaseInstance.get_session().delete(method)
        DatabaseInstance.get_session().commit()


class Oxygen(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get_table('oxygen')

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
        DatabaseInstance.get_session().add(self)
        DatabaseInstance.get_session().commit()

    @staticmethod
    def get(id):
        return Oxygen.query.get(id)

    @staticmethod
    def set(id, relationship):
        oxygen = Oxygen.query.get(id)
        oxygen.relationship = relationship
        DatabaseInstance.get_session().commit()

    @staticmethod
    def delete(id):
        oxygen = Oxygen.query.get(id)
        DatabaseInstance.get_session().delete(oxygen)
        DatabaseInstance.get_session().commit()


class Ph(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get_table('ph')

    def __init__(self, relationship):
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
        DatabaseInstance.get_session().commit()

    @staticmethod
    def delete(id):
        ph = Ph.query.get(id)
        DatabaseInstance.get_session().delete(ph)
        DatabaseInstance.get_session().commit()


class Project(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get_table('project')

    def __init__(self, name):
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
        DatabaseInstance.get_session().commit()

    @staticmethod
    def delete(id):
        project = Project.query.get(id)
        DatabaseInstance.get_session().delete(project)
        DatabaseInstance.get_session().commit()


class Salinity(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get_table('salinity')

    def __init__(self, relationship):
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
        DatabaseInstance.get_session().commit()


class Sample(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get_table('sample')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Sample {self.name}>'

    def __str__(self):
        return f'<Sample {self.name}>'

    @staticmethod
    def get(id):
        return Sample.query.get(id)

    @staticmethod
    def set(id, name):
        sample = Sample.query.get(id)
        sample.name = name
        DatabaseInstance.get_session().commit()

    @staticmethod
    def delete(id):
        sample = Sample.query.get(id)
        DatabaseInstance.get_session().delete(sample)
        DatabaseInstance.get_session().commit()


class SampleHasKeywords(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get_table('sample_has_keywords')

    def __init__(self, sample_id, keywords_id):
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
        DatabaseInstance.get_session().commit()

    @staticmethod
    def delete(sample_id, keywords_id):
        sample_has_keywords = SampleHasKeywords.query.get((sample_id, keywords_id))
        DatabaseInstance.get_session().delete(sample_has_keywords)
        DatabaseInstance.get_session().commit()


class Target(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get_table('target')

    def __init__(self, name):
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
        DatabaseInstance.get_session().commit()

    @staticmethod
    def delete(id):
        target = Target.query.get(id)
        DatabaseInstance.get_session().delete(target)
        DatabaseInstance.get_session().commit()


class Temperature(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get_table('temperature')

    def __init__(self, relationship):
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
        DatabaseInstance.get_session().commit()

    @staticmethod
    def delete(id):
        temperature = Temperature.query.get(id)
        DatabaseInstance.get_session().delete(temperature)
        DatabaseInstance.get_session().commit()

class User(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get_table('user')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<User {self.name}>'

    def __str__(self):
        return f'<User {self.name}>'

    @staticmethod
    def get(id):
        return User.query.get(id)

    @staticmethod
    def set(id, name):
        user = User.query.get(id)
        user.name = name
        DatabaseInstance.get_session().commit()

    @staticmethod
    def delete(id):
        user = User.query.get(id)
        DatabaseInstance.get_session().delete(user)
        DatabaseInstance.get_session().commit()


class UserExperiment(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get_table('user_experiment')

    def __init__(self, user_id, experiment_id):
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
        DatabaseInstance.get_session().commit()

    @staticmethod
    def delete(user_id, experiment_id):
        user_experiment = UserExperiment.query.get((user_id, experiment_id))
        DatabaseInstance.get_session().delete(user_experiment)
        DatabaseInstance.get_session().commit()


class UserHasGroup(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get_table('user_has_group')

    def __init__(self, user_id, group_id):
        self.user_id = user_id
        self.group_id = group_id

    def __repr__(self):
        return f'<UserHasGroup {self.user_id} {self.group_id}>'

    def __str__(self):
        return f'<UserHasGroup {self.user_id} {self.group_id}>'

    @staticmethod
    def get(user_id, group_id):
        return UserHasGroup.query.get((user_id, group_id))

    @staticmethod
    def set(user_id, group_id):
        user_has_group = UserHasGroup.query.get((user_id, group_id))
        user_has_group.user_id = user_id
        user_has_group.group_id = group_id
        DatabaseInstance.get_session().commit()

    @staticmethod
    def delete(user_id, group_id):
        user_has_group = UserHasGroup.query.get((user_id, group_id))
        DatabaseInstance.get_session().delete(user_has_group)
        DatabaseInstance.get_session().commit()


class UserProject(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get_table('user_project')

    def __init__(self, user_id, project_id):
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
        DatabaseInstance.get_session().commit()

    @staticmethod
    def delete(user_id, project_id):
        user_project = UserProject.query.get((user_id, project_id))
        DatabaseInstance.get_session().delete(user_project)
        DatabaseInstance.get_session().commit()


class UserSharedSample(HaloDatabaseInstanceModel):
    __table__ = DatabaseInstance.get_table('user_shared_sample')

    def __init__(self, user_id, sample_id):
        self.user_id = user_id
        self.sample_id = sample_id

    def __repr__(self):
        return f'<UserSharedSample {self.user_id} {self.sample_id}>'

    def __str__(self):
        return f'<UserSharedSample {self.user_id} {self.sample_id}>'

    @staticmethod
    def get(user_id, sample_id):
        return UserSharedSample.query.get((user_id, sample_id))

    @staticmethod
    def set(user_id, sample_id):
        user_shared_sample = UserSharedSample.query.get((user_id, sample_id))
        user_shared_sample.user_id = user_id
        user_shared_sample.sample_id = sample_id
        DatabaseInstance.get_session().commit()

    @staticmethod
    def delete(user_id, sample_id):
        user_shared_sample = UserSharedSample.query.get((user_id, sample_id))
        DatabaseInstance.get_session().delete(user_shared_sample)
        DatabaseInstance.get_session().commit()
