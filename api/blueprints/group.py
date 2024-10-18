import json

from flask import Blueprint
from flask import Response, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from api import log
from api.auth import required_token, not_required_token
from api.controllers.GroupController import GroupController
from api.controllers.UserController import UserController
from api.decorators import wrap_error, get_params, log_params
from api.utils import serialize_datetime

group_page = Blueprint('group_page', __name__)

# limiter = Limiter(get_remote_address)

@wrap_error
# @limiter.limit("100/minute")
# @get_params
# @log_params
@required_token
@group_page.route('/group/', methods=['POST'])
def add_group(**kwargs):
    log.info('Request received for creating a new group')

    try:
        uid: str = kwargs['uid']
        if uid is None:
            message = {'status': 'error',
                       'message': 'No user provided'
                       }
            result_status = 400
        else:
            log.info(f'GET group request received for user { uid = } with { params = }')
            user = UserController.get_user_by_uid(uid)

            new_group = GroupController.create_group(params, user)
            message = {'status': 'success',
                       'message': 'Group created',
                       'group': new_group
                       }
            result_status = 200
            log.info(f'Group created')
    except Exception as e:
        message = {'status': 'error',
                   'message': str(e)
                   }
        result_status = 400

    return Response(response=json.dumps(message, default=serialize_datetime),
                    status=result_status,
                    mimetype="application/json")


@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
@required_token
@group_page.route('/group/', methods=['GET', 'DELETE'])
def group_handle(params: dict, **kwargs):
    """
    With the method GET: Get the data of a given group (if the param 'id' is provided) or the list of groups of a user.
    With the method DELETE: Delete a group. In this case, the param 'id' is mandatory.
    :param params:
    :param kwargs:
    :return:
    """
    result_status = 200
    message = ''

    uid: str = kwargs['uid']
    if uid is None:
        message = {'status': 'error',
                   'message': 'No user provided'
                   }
        result_status = 400
    else:
        log.info(f'GET group request received for user { uid = } with { params = }')
        user = UserController.get_user_by_uid(uid)
        if user is None:
            message = {'status': 'error',
                       'message': 'User with {uid =} not found'
                       }
            result_status = 400

    if 'id' in params:
        result = GroupController.get_group_by_id(params['id'])
        relation = GroupController.get_relation(user.id, result.id)
        if relation is None:
            message = {'status': 'error',
                       'message': 'The user with uid {uid} doesn\'t belong to the group {params["id"]}'
                       }
            result_status = 400
        else:
            result.relation = relation
    else:
        result = GroupController.get_groups_by_user(user['id'])

    if request.method == 'GET':
        log.info(f'GET group request received for user { uid = } with { params = }')

        message = {'status': 'success',
                   'message': 'Group found',
                   'group': result.as_dict()
                   }
        result_status = 200

    if request.method == 'DELETE':
        if 'id' not in params:
            message = {'status': 'error',
                       'message': 'No group id provided'
                       }
            result_status = 400
        else:
            if relation != 'owner':
                message = {'status': 'error',
                           'message': 'User with {uid =} is not the owner of the group {params["id"]}'
                           }
                result_status = 400
            else:
                log.info(f'DELETE request received for group {id =} from user { uid = }')
                try:
                    GroupController.delete_group(params['id'])
                    message = {'status': 'success',
                               'message': 'Group deleted'
                               }
                    result_status = 200
                    log.info(f'Group with {id = } deleted')
                except Exception as e:
                    log.info(f'Error deleting group with {id = }: {str(e)}')
                    message = {'status': 'error',
                               'message': str(e)
                               }
                    result_status = 400

    return Response(response=json.dumps(message, default=serialize_datetime),
                    status=result_status,
                    mimetype="application/json")


@wrap_error
# @limiter.limit("100/minute")
# @get_params
# @log_params
@required_token
@group_page.route('/group/<int:group_id>/', methods=['PUT', 'PATCH'])
def group_edit(group_id: int, **kwargs):
    uid: str = kwargs['uid']

    log.info(f'PUT/PATCH request received for group {group_id = } from user with uid {uid} with {params = }')

    user = UserController.get_user_by_uid(uid)

    request_form = json.loads(request.data)

    relation = GroupController.get_relation(user.id, group_id)
    if relation is None:
        message = {'status': 'error',
                   'message': 'The user with uid {uid} doesn\'t belong to the group {group_id}'
                   }
        result_status = 400
    else:
        if relation != 'owner':
            message = {'status': 'error',
                       'message': 'User with {uid =} is not the owner of the group {group_id} and can\'t edit it'
                       }
            result_status = 400
        else:

            try:
                updated = GroupController.update_group(group_id, request_form)
                # updated = GroupController.get_group_by_id(id)
                message = {'status': 'success',
                           'message': 'Group updated',
                           'group': updated.as_dict()
                           }
                result_status = 200
                log.info(f'User with id = {updated.id} updated')
            except Exception as e:
                log.info(f'Error updating group with id {group_id}: {str(e)}')
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

@get_params
@wrap_error
@not_required_token
@group_page.route('/group/<string:table>/list/', methods=['GET'])
def get_table_list_by_user(table: str, **kwargs):
    """
    Given a user id and a related element (group, experiment, project or sample), return the list of elements related
     to the user. If no valid token, and the query is for samples, the list of public samples is returned.
    :param params:
    :param id: the user id.
    :param table: the table to get the related data.
    :return: the list of elements of the table related to the user. Or the list of public samples
    """
    uid: str = kwargs['uid']
    # uid: str = not_required_token(False)
    # TODO: implement the query for the different tables

    ## if uid is None:
    ##     if table == 'samples':
    ##         log.info('Request received for list of public samples')
    ##         result = SampleController.list_public_samples()
    ##     else:
    ##         abort(403, "No token provided")
    ## else:
    ##     # uid: str = kwargs['uid']
    ##     user_id = UserController.get_user_by_uid(uid).id
    ##
    ##     if table == "groups":
    ##         result = GroupController.get_groups_by_user(user_id)
    ##     # elif table == "users":
    ##     #     result = UserController.get_users_by_user(user_id)
    ##     elif table == "experiments":
    ##         result = ExperimentController.get_experiments_by_user(user_id)
    ##     elif table == "projects":
    ##         result = ProjectController.get_projects_by_user(user_id)
    ##     elif table == "samples":
    ##         result = SampleController.get_samples_shared_with_user(user_id)
    ##     else:
    ##         abort(405, f"Table {table} not found")
    result = []
    return Response(response=json.dumps(result, default=serialize_datetime),
                    status=200,
                    mimetype="application/json")



# ##############################################################
# Group invitation handling
# ##############################################################
@wrap_error
# @limiter.limit("100/minute")
# @get_params
# @log_params
@required_token
@group_page.route('/group/<int:group>/invitation/', methods=['PUT', 'PATCH', 'DELETE'])
def accept(group: int, **kwargs):
    """
    Accept or reject an invitation to join a group, if the request is a DELETE, the invitation is rejected

    :param group: the group identifier
    :return:
    """
    try:
        uid = kwargs['uid']
        user_id = UserController.get_user_by_uid(uid).id

        answer = request.method != 'DELETE'

        log.info(f"The invitation request to user {user_id} to join {group} is {'accept' if answer else 'reject'}ed")
        GroupController.accept_invite(user_id, group, answer)
        result = {"message": "OK"}
    except Exception as e:
        result = {"message": f"ERROR: {e}"}

    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")


@wrap_error
@required_token
@group_page.route('/group/<int:group>/invite/<string:invited_uid>/', methods=['POST'])
def invite(group: int, invited_uid: int,  **kwargs):
    """
    Invite a user to join a group
    :param invited_uid: the user to invite
    :param group: the group to join
    :return:
    """
    try:
        owner_uid = kwargs['uid']
        owner_id = UserController.get_user_by_uid(owner_uid).id
        user_invited_id = UserController.get_user_by_uid(invited_uid).id

        log.info(f"Invitation request from user {owner_uid} to user {invited_uid} to join group {group}")
        GroupController.invite(owner_id, user_invited_id, group)
        result = {"message": "OK"}
    except Exception as e:
        result = {"message": f"ERROR: {e}"}

    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")

