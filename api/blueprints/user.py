import json

from flask import Blueprint, abort
from flask import Response, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from api import log
from api.auth import required_token, get_uid_from_request
from api.controllers.GroupController import GroupController
from api.controllers.ProjectController import ProjectController
from api.controllers.SampleController import SampleController
from api.controllers.UserController import UserController
from api.decorators import wrap_error, get_params, log_params
from api.field_utils import get_step_table
from api.utils import serialize_datetime

user_page = Blueprint('user_page', __name__)

limiter = Limiter(get_remote_address)


@user_page.route('/user/', methods=['POST'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def add_user(params: dict, **kwargs):
    log.info('Request received for creating a new user')

    try:
        new_user = UserController.create_user(params)
        message = {'status': 'success',
                   'message': 'User created',
                   'user': new_user
                   }
        result_status = 200
        uid = new_user['uid']
        log.info(f'User with uid "{uid}" created')
    except Exception as e:
        message = {'status': 'error',
                   'message': str(e)
                   }
        result_status = 400

    return Response(response=json.dumps(message, default=serialize_datetime),
                    status=result_status,
                    mimetype="application/json")


@user_page.route('/user/', methods=['GET', 'DELETE'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def user_handle(params: dict, **kwargs):
    result_status = 200
    message = ''

    uid: str = kwargs['uid']

    if request.method == 'GET':
        log.info(f'GET request received for user { uid = } with { params = }')
        usr = UserController.get_user_by_uid(uid)
        message = usr
        result_status = 200

    if request.method == 'DELETE':
        log.info(f'DELETE request received for user { uid = }')
        try:
            UserController.delete_user(uid)
            message = {'status': 'success',
                       'message': 'User deleted'
                       }
            result_status = 200
            log.info(f'User with {uid = } deleted')
        except Exception as e:
            log.info(f'Error deleting user with {uid = }: {str(e)}')
            message = {'status': 'error',
                       'message': str(e)
                       }
            result_status = 400

    return Response(response=json.dumps(message, default=serialize_datetime),
                    status=result_status,
                    mimetype="application/json")


@user_page.route('/user/', methods=['PUT', 'PATCH'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
# @required_token
def user_edit(params: dict, **kwargs):
    uid: str = kwargs['uid']

    log.info(f'PUT/PATCH request received for user {uid = } with {params = }')

    request_form = json.loads(request.data)
    try:
        UserController.update_user(uid, request_form)
        updated = UserController.get_user_by_uid(uid)
        message = {'status': 'success',
                   'message': 'User updated',
                   'user': updated
                   }
        result_status = 200
        log.info(f'User with id = {updated.id} updated')
    except Exception as e:
        log.info(f'Error updating user with {uid = }: {str(e)}')
        message = {'status': 'error',
                   'message': str(e)
                   }
        result_status = 400

    return Response(response=json.dumps(message, default=serialize_datetime),
                    status=result_status,
                    mimetype="application/json")


# ##############################################################
#  Querying information related to a user
# ##############################################################

@user_page.route('/user/list/<string:table>/', methods=['GET'])
@get_params
@wrap_error
# @required_token
def get_table_list_by_user(params: dict, query_table: str, **kwargs):
    """
    Given a user id and a related element (group, experiment, project or sample), return the list of elements related
     to the user. If no valid token, and the query is for samples, the list of public samples is returned.
    :param params:
    :param id: the user id.
    :param query_table: the table to get the related data.
    :return: the list of elements of the table related to the user. Or the list of public samples
    """
    uid = get_uid_from_request(False)
    table = get_step_table(query_table)

    if uid is None:
        if table is not None:
            log.info('Request received for list of public {query_table}')
            result = SampleController.list_public(table)
        else:
            abort(403, "No token provided")
    else:
        # uid: str = kwargs['uid']
        user_id = UserController.get_user_by_uid(uid).id

        if table is None:
            abort(405, f"Table {query_table} not found")
        elif query_table == "groups":
            result = GroupController.get_groups_by_user(user_id)
        # elif table == "users":
        #     result = UserController.get_users_by_user(user_id)
        elif query_table == "projects":
            result = ProjectController.get_projects_by_user(user_id)
        # elif query_table == "samples":
        #     result = SampleController.get_samples_shared_with_user(user_id)
        else:
            result = SampleController.get_shared_with_user(query_table, user_id)

    return Response(response=json.dumps(result, default=serialize_datetime),
                    status=200,
                    mimetype="application/json")

