import datetime
import logging
import os

import uuid

from sqlalchemy import select, delete

from api.config import UPLOADS_DIR
from api.db.db import DatabaseInstance
from api.db.models import Sample, User_Shared_Sample, Group, User_Has_Group, Temperature, Ph, Salinity, \
    Method, Oxygen, Fraction, Target, Extraction, Assembly, Sequencing, Binning, Group_Shared_Sample, Project, User, \
    Keywords, Hkgenes, Dois
from api.field_utils import valid_field, fix_times, complementaries, supplementaries, multi_complementaries, \
    get_reference_tables, get_step_table, get_sharing_tables, is_file_field, get_file_name_field, get_stored_procedure, \
    merge_extra_fields, sequence_step_sharings, filter_dict, get_file_name_field_raw
from api.utils import convert_to_dict, to_dict, normalize



class SampleController:
    """
    This class is the way to interact with the samples in the database.
    The samples are the most important data stored in the database.
    The samples are associated with an experiment, thus they are related to a project.
    The samples are owned by a user, and can be shared with other users o with groups.
    It's possible that samples don't have an owner, nor group nor experiment associated with it.
    """

    @classmethod
    def get_sample_by_id(cls, sample_id: int):
        sample = Sample.query.get(sample_id)
        return sample

    @classmethod
    def get_step_by_id(cls, table, step_id: int):
        value = table.query.get(step_id)
        return value

    @classmethod
    def get_samples_owned_by_user(cls, user_id: int):
        Sample.query.filter_by(user_id=user_id).all()


    #TODO: get_experiment_steps return the list of the ids of steps available given an experiment and a user id


    @classmethod
    def test_description_fields(cls, sample):
        # Test if the fields that are supposed to be ids to other tables are valid
        # This way we can avoid inserting wrong data in the database, and also avoid
        # querying the database with wrong data. If more than one value is wrong, all
        # the wrong values are returned at a time.
        wrong_list = []
        for key, value in complementaries.items():
            if key in sample and sample[key] is not None:
                element = value.query.filter_by(id=sample[key]).first()

                if element is None:
                    wrong_list.append(key)

        return wrong_list

    @classmethod
    def filter_description_fields(cls, step):
        # This method is used to replace the ids of the fields that are supposed to be ids to other tables
        # with the description of the element in the other table. This way the user can see the description
        # of the element instead of the id.

        # TODO: implement keyword, publication and hkgn handling.

        for key, value in complementaries.items():
            if key in step and step[key] is not None:
                element = value.query.filter_by(id=step[key]).first()

                if element is not None:
                    step[key] = element.description
                else:
                    step[key] = None

        for key, value in supplementaries.items():
            if key in step:
                if value['field'] in step:
                    v = step[value['field']]
                    if v is not None:
                        element = value['table'].query.filter(value['table'].vmin < v, v <= value['table'].vmax).first()

                        if element is not None:
                            step[key] = element.description
                        else:
                            step[key] = None

        # keywords, publication and hkgn are slightly more complex than the others
        for key, value in multi_complementaries.items():
            if key in step and step[key] is not None and isinstance(step[key], list) and len(step[key]) > 0:
                step[key] = step[key]
            else:
                step[key] = None

        # finally keep only the fields that are not None
        step = {k: v for k, v in step.items() if v is not None}

        return step

    @classmethod
    def get_shared_with_user(cls, step, user_id):
        with DatabaseInstance.get().cursor() as cursor:
            procedure = get_stored_procedure(step)
            cursor.callproc(procedure, [user_id])
            column_names = [desc[0] for desc in cursor.description]
            result = list(cursor.fetchall())

        data = [cls.filter_description_fields
                (merge_extra_fields
                 (convert_to_dict(row, column_names))) for row in result]

        return data

    @classmethod
    def get_file_data(cls, step, field):
        if not is_file_field(field):
            raise Exception("The field is not a file")

        filedata = getattr(step, field)
        filename = getattr(step, get_file_name_field_raw(field))
        if filedata is None or filename is None:
            raise Exception("The file is not set")
        if not os.path.exists(os.path.join(UPLOADS_DIR, filedata)):
            raise Exception("The file doesn't exist")

        #return filename, open(os.path.join(UPLOADS_DIR, filedata), 'rb')
        return filename, os.path.abspath(os.path.join(UPLOADS_DIR, filedata))


    @classmethod
    def add_file(cls, step, field, file_data, filename_field, filename):
        if not is_file_field(field):
            raise Exception("The field is not a file")

        uuid_file = getattr(step, field)
        if uuid_file is None:
            uuid_file = str(uuid.uuid4())
            setattr(step, field, uuid_file)

        setattr(step, get_file_name_field_raw(field), filename)
        setattr(step, 'updated', datetime.datetime.now())
        file_data.save(os.path.join(UPLOADS_DIR, uuid_file))

    @classmethod
    def update_file(cls, sequence: str, step: str, step_id: int, file_id: str, file_name: str, file_data: bytes):

        # Get the reference tables for the sequence and the step
        current_class, parent_class = get_reference_tables(sequence, step)

        with DatabaseInstance.get().session() as session:
            try:
                if not is_file_field(file_id):
                    raise Exception("The field {file_id} is not a file field")

                filename_field = get_file_name_field(step, file_id)

                step_to_edit = current_class.query.filter_by(id=step_id).first()

                if step_to_edit is None:
                    raise Exception(f"Sequence step {step} with id {step_id} not found")

                cls.add_file(step_to_edit, file_id, file_data, filename_field, file_name)

                session.query(current_class).filter_by(id=step_id).update(step_to_edit.as_dict())
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    # @classmethod
    # def update_sample(cls, sample_id: int, new_data: dict):
    #     with DatabaseInstance.get().session() as session:
    #         try:
    #             fix_times(new_data)
    #
    #             sample_to_edit = Sample.query.filter_by(id=sample_id).first()
    #             if sample_to_edit is None:
    #                 raise Exception("Sample with id {sample_id} not found")
    #
    #             for key, value in new_data.items():
    #                 if valid_field(key):
    #                     setattr(sample_to_edit, key, value)
    #
    #             setattr(sample_to_edit, 'updated', datetime.datetime.now())
    #
    #             session.query(Sample).filter_by(id=sample_id).update(sample_to_edit.as_dict())
    #             session.commit()
    #             result = sample_to_edit.as_dict()
    #         except Exception as e:
    #             session.rollback()
    #             raise e
    #     return result

    @classmethod
    def update_sequence_step(cls, sequence, step, step_id: int, new_data: dict):

        current_class, parent_class = get_reference_tables(sequence, step)

        fix_times(new_data)

        with DatabaseInstance.get().session() as session:
            try:
                # step_to_edit = current_class.query.filter_by(id=step_id).first()
                stmt = select(current_class).filter_by(id=step_id)
                step_to_edit = session.execute(stmt).scalar_one_or_none()

                if step_to_edit is None:
                    raise Exception("Sequence step {step} with id {sample_id} not found")

                for key, value in new_data.items():
                    if valid_field(key) and key not in multi_complementaries:
                       setattr(step_to_edit, key, value)

                cls.update_multi_complementaries(step_to_edit, new_data, session)

                setattr(step_to_edit, 'updated', datetime.datetime.now())

                # session.query(current_class).filter_by(id=step_id).update(step_to_edit.as_dict())
                # session.flush()
                result = step_to_edit.as_dict()

                session.commit()

                result = cls.fix_multiples(result)
                result = filter_dict(result)

            except Exception as e:
                session.rollback()
                raise e
        return result

    @classmethod
    def delete_sample(cls, sample_id: int):
        # TODO: To take into consideration when deleting a sample:
        # TODO: make sure that the user is the owner of the sample
        # TODO: if a sample is shared with a group, the group must be informed
        # TODO: if a sample is shared with a user, the user must be informed
        # TODO: if a sample has treatments, the sample can't be deleted
        with DatabaseInstance.get().session() as session:
            try:
                stmt = select(Sample).filter_by(id=sample_id)
                sample = session.execute(stmt).first()
                if sample is None:
                    raise Exception("Sample with id {sample_id} not found")
                sample_to_delete = sample[0]
                session.delete(sample_to_delete)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    @classmethod
    def get_access_mode(cls, table, user_id, step_id: int):
        # accessible_list = cls.get_samples_shared_with_user(user_id)
        # for sample in accessible_list:
        #     if sample['id'] == sample_id:
        #         return sample['access_mode']
        # return None
        the_step = table.query.get(step_id)

        if the_step.is_public:
            return 'read'

        if the_step.user_id == user_id:
            return 'readwrite'

        for shared_user in the_step.user_shared_sample:
            if shared_user.user_id == user_id:
                return shared_user.access_mode

        for shared_group in the_step.group_shared_sample:
            for user_group in shared_group.group.user_has_group:
                if user_id == user_group.user_id and user_group.relation != 'invited':
                    return shared_group.access_mode

        return None

    @classmethod
    def get_step_access_mode(cls, sequence_step: str, user_id, step_id: int):
        """
        Check the access mode of the user to the sequence step
        :param sequence_step: the kind of step
        :param user_id: the user
        :param step_id: the step id
        :return: the corresponding access mode o None if the user doesn't have access to the step
        """
        # TODO: implement this method correctly

        # accessible_list = cls.get_samples_shared_with_user(user_id)
        # for sample in accessible_list:
        #     if sample['id'] == sample_id:
        #         return sample['access_mode']
        # return None

        # user = User.query.get(user_id)
        table = get_step_table(sequence_step)
        step = table.query.get(step_id)

        if step.user_id == user_id:
            return 'readwrite'

        sharing = get_sharing_tables(sequence_step)
        sharing_groups_table = sharing['group']
        sharing_users_table = sharing['user']

        if sharing_users_table is not None:
            shared_user = sharing_users_table.query.filter(
                sharing_users_table.user_id == step.user_id and sharing_users_table.shared_id == step_id).first()
            if shared_user is not None:
                return shared_user.access_mode

        if sharing_groups_table is not None:
            for shared_group in sharing_groups_table.query.filter(sharing_groups_table.shared_id == step_id):
                for user_group in shared_group.group.user_has_group:
                    if user_id.id == user_group.user_id and user_group.relation != 'invited':
                        return shared_group.access_mode

        # for shared_user in step.user_shared_experiment:
        #    if shared_user.user_id == user_id:
        #        return shared_user.access_mode

        # for shared_group in step.group_shared_experiment:
        #    for user_group in shared_group.group.user_has_group:
        #        if user_id.id == user_group.user_id and user_group.relation != 'invited':
        #            return shared_group.access_mode

        return None

    @classmethod
    def list_samples(cls):
        return to_dict(Sample.query.all())

    @classmethod
    def list_public(cls, step):
        table = get_step_table(step)
        result = table.query.filter_by(is_public=True).all()

        result = [cls.filter_description_fields(merge_extra_fields(element.as_dict())) for element in result]
        return result

    @classmethod
    def make_public(cls, step, step_id, owner):

        table = get_step_table(step)
        with DatabaseInstance.get().session() as session:
            try:
                item = session.query(table).filter_by(id=step_id).first()

                if item is None:
                    raise Exception("{step} with id {step_id} not found")

                if item.user_id != owner:
                    raise Exception("User is not the owner of the {step} with id {step_id}}")

                setattr(item, 'is_public', 1)

                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    @classmethod
    def share_step(cls, type: str, step: str, owner: int, step_id: int, user_group_id: int, readwrite: bool):
        with DatabaseInstance.get().session() as session:
            try:
                shared_table = get_sharing_tables(step)[type]
                if type == 'user':
                    shared_step = shared_table.query.filter_by(shared_id=step_id, user_id=user_group_id).first()
                else:
                    shared_step = shared_table.query.filter_by(shared_id=step_id, group_id=user_group_id).first()

                if shared_step is None:
                    shared_step = shared_table()
                    shared_step.shared_id = step_id
                    if type == 'group':
                        shared_step.group_id = user_group_id
                    else:
                        shared_step.user_id = user_group_id
                    shared_step.access_mode = "readwrite" if readwrite else "read"
                    session.add(shared_step)
                else:
                    setattr(shared_step, 'access_mode', 'readwrite' if readwrite else 'read')

                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    @classmethod
    def verify_group_relation(cls, step, owner, step_id, group_id):
        """
        Test if the user is the owner of the sequence step and if the user has the right privileges to share it to the
        group.
        :param step:
        :param owner:
        :param step_id:
        :param group_id:
        :return:
        """
        table = get_step_table(step)

        the_step = table.query.filter_by(id=step_id).first()
        if the_step is None:
            raise Exception(f"Sequence step {step} with id {step_id} not found")

        if the_step.user_id != owner:
            raise Exception(f"User {owner} is not the owner of the sequence step {step} with id {step_id}")

        group = Group.query.filter_by(id=group_id).first()
        if group is None:
            raise Exception(f"The group {group_id} doesn't exist")

        owner_group = User_Has_Group.query.filter_by(user_id=owner, group_id=group_id).first()
        if owner_group is None or owner_group.relation != 'owner':
            raise Exception(f"User {owner} doesn't have the right privileges to share "
                            f"or remove the sequence step {step_id} to the group {group}")

    @classmethod
    def verify_user_relation(cls, step, owner, step_id, user_id):
        table = get_step_table(step)

        the_step = table.query.filter_by(id=step_id).first()
        if the_step is None:
            raise Exception(f"Sequence step {step} with id {step_id} not found")

        if the_step.user_id != owner:
            raise Exception(f"User {owner} is not the owner of a {step} with id {step_id}")

        if user_id == owner:
            raise Exception("User can't share a {step} with himself")

    @classmethod
    def share_step_group(cls, step, owner, step_id, group_id, readwrite):
        cls.verify_group_relation(step, owner, step_id, group_id)
        cls.share_step('group', step, owner, step_id, group_id, readwrite)

    @classmethod
    def share_step_user(cls, step: str, owner: int, step_id: int, user_id: int, readwrite: bool):
        cls.verify_user_relation(step, owner, step_id, user_id)
        cls.share_step('user', step, owner, step_id, user_id, readwrite)

    @classmethod
    def unshare_step_group(cls, step: str, owner, shared_id, group_id):
        with DatabaseInstance.get().session() as session:
            try:
                cls.verify_group_relation(step, owner, shared_id, group_id)

                shared_table = get_sharing_tables(step)['group']

                the_shared_step = shared_table.query.filter_by(shared_id=shared_id, group_id=group_id).first()

                if the_shared_step is not None:
                    session.delete(shared_table).where(shared_id == shared_id).where(group_id == group_id)
                    session.commit()
                else:
                    session.rollback()
                    raise Exception(f"Sample {shared_id} isn't shared with group {group_id}")

            except Exception as e:
                session.rollback()
                raise e

    @classmethod
    def unshare_step_user(cls, step, step_id, user_id):
        with DatabaseInstance.get().session() as session:
            try:
                shared_table = get_sharing_tables(step)['user']

                shared_step = shared_table.query.filter_by(shared_id=step_id, user_id=user_id).first()
                if shared_step is None:
                    raise Exception(f"User {user_id} doesn't have access to the sequence step {step} with id {step_id}")
                # TODO: this doesn't work. the database is not updated
                # session.delete(shared_step)
                delete(shared_table).where(shared_table.shared_id == step_id).where(shared_table.user_id == user_id)
                # session.delete(shared_table).where(shared_id=step_id).where(user_id=user_id)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    # ######################################

    @classmethod
    def create_sequence_step(cls, data, sequence, step, user_id):

        current_class, parent_class = get_reference_tables(sequence, step)

        fix_times(data)

        with (DatabaseInstance.get().session() as session):
            try:
                step_to_create = current_class()

                if 'project_id' in data:
                    # Make sure there is a valid project id, not an empty one
                    if len(data['project_id']) == 0:
                        data.pop('project_id')
                    else:
                        project = Project.query.get(data['project_id'])
                        if project is None:
                            raise Exception("Project not found")
                        found = False
                        for test in Project.users:
                            if test.id == user_id:
                                found = True
                                break
                        if not found:
                            raise Exception("User is not associated with the project")

                        step_to_create.project_id = project
                # else:
                #    step_to_create.project_id = None

                wrong_complementaries = cls.test_description_fields(data)
                if len(wrong_complementaries) > 0:
                    raise Exception(f"Fields {wrong_complementaries} are not valid for {step} in {sequence}")

                step_to_create.from_dict(data)

                cls.update_multi_complementaries(step_to_create, data, session)

                # Fix the owner of the sample to the current owner
                step_to_create.user_id = user_id

                session.add(step_to_create)
                # session.flush()
                result = step_to_create.as_dict()

                session.commit()

                result = cls.fix_multiples(result)
                result = filter_dict(result)

                return result
            except Exception as e:
                session.rollback()
                raise e



    @classmethod
    def update_multi_complementaries(cls, the_step, data, the_session):

        if 'keywords' in data:
            # If the keywords are provided, they must be a list of strings
            if isinstance(data['keywords'], str):
                keywords_list = [data['keywords']]
            elif isinstance(data['keywords'], list):
                keywords_list = data['keywords']
            else:
                keywords_list = None
            if keywords_list is not None:
                the_step.keywords = []
                for keyword in keywords_list:
                    if isinstance(keyword, int):
                        # If the keyword is an integer, it is an id of an existing keyword
                        # existing_kw = Keywords.query.get(keyword)
                        stmt = select(Keywords).filter_by(id=keyword)
                        existing_kw = the_session.execute(stmt).scalar_one_or_none()
                        the_step.keywords.append(existing_kw)
                    elif isinstance(keyword, str) and len(keyword.strip()) > 0:
                        # existing_kw = Keywords.query.filter_by(keyword=keyword.strip().lower()).first()
                        stmt = select(Keywords).filter_by(keyword=keyword.strip().lower())
                        existing_kw = the_session.execute(stmt).scalar_one_or_none()
                        if existing_kw is not None:
                            try:
                                the_step.keywords.append(existing_kw)
                            except Exception as e:
                                logging.exception(e)
                        else:
                            new_keyword = Keywords(keyword=keyword.strip())
                            # the_session.add(new_keyword)
                            the_step.keywords.append(new_keyword)


        if 'hkgenes' in data:
            # Housekeeping genes provided?, they are list of strings of indexes
            if isinstance(data['hkgenes'], str):
                hkgenes_list = [data['hkgenes']]
            elif isinstance(data['hkgenes'], list):
                hkgenes_list = data['hkgenes']
            else:
                hkgenes_list = None
            if hkgenes_list is not None:
                the_step.hkgenes = []
                for gene in hkgenes_list:
                    if isinstance(gene, int):
                        # If gene is an integer, it is an id of an existing housekeeping gene
                        # existing_gene = Hkgenes.query.get(gene)
                        stmt = select(Hkgenes).filter_by(id=gene)
                        existing_gene = the_session.execute(stmt).scalar_one_or_none()
                        if existing_gene is not None:
                            the_step.hkgenes.append(existing_gene)
                    elif isinstance(gene, str) and len(gene.strip()) > 0:
                        # existing_gene = Hkgenes.query.filter_by(gene=gene.strip()).first()
                        stmt = select(Hkgenes).filter_by(gene=gene.strip()) #.first()
                        existing_gene = the_session.execute(stmt).scalar_one_or_none()
                        if existing_gene is not None:
                            the_step.hkgenes.append(existing_gene)
                        else:
                            new_hkgene = Hkgenes(gene=gene.strip())
                            the_session.add(new_hkgene)
                            the_step.hkgenes.append(new_hkgene)

        if 'dois' in data:
            # DOI handling if provided, they are a list of URI
            if isinstance(data['dois'], str):
                doi_list = [data['dois']]
            elif isinstance(data['dois'], list):
                doi_list = data['dois']
            else:
                doi_list = None
            if doi_list is not None:
                the_step.dois = []
                for doi in doi_list:
                    if isinstance(doi, int):
                        # If the doi is an integer, it is an id of an existing doi
                        # existing_doi = Dois.query.get(doi)
                        stmt = select(Dois).filter_by(id=doi)
                        existing_doi = the_session.execute(stmt).scalar_one_or_none()
                        if existing_doi is not None:
                            the_step.dois.append(existing_doi)
                    elif isinstance(doi, str) and len(doi.strip()) > 0:
                        # existing_doi = Dois.query.filter_by(value=doi.strip()).first()
                        stmt = select(Dois).filter_by(value=doi.strip())# .first()
                        existing_doi = the_session.execute(stmt).scalar_one_or_none()
                        if existing_doi is not None:
                            the_step.dois.append(existing_doi)
                        elif isinstance(doi, str) and len(doi.strip()) > 0:
                            new_doi = Dois(value=doi.strip())
                            the_session.add(new_doi)
                            the_step.dois.append(new_doi)


    @classmethod
    def fix_multiples(cls, data):
        """
        This function is used to fix the fields that are supposed to be lists of ids, but are not.
        :param data: the data to fix
        :return: the fixed data
        """

        if 'keywords' in data:
            data['keywords'] = [k.keyword for k in data['keywords']]
        if 'hkgenes' in data:
            data['hkgenes'] = [k.gene for k in data['hkgenes']]
        if 'dois' in data:
            data['dois'] = [k.value for k in data['dois']]

        return data

    @classmethod
    def get_public_sequence_step(cls, step):

        current_class = get_step_table(step)
        current_class.query.filter_by(is_public=True).all()
        return to_dict(current_class.query.filter_by(is_public=True).all())