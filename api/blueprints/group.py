import json

from flask import Blueprint
from flask import Response, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from api import log
from api.auth import required_token, get_uid_from_request
from api.controllers.GroupController import GroupController
from api.controllers.UserController import UserController
from api.decorators import wrap_error, get_params, log_params
from api.utils import serialize_datetime

group_page = Blueprint('group_page', __name__)

# limiter = Limiter(get_remote_address)




@group_page.route('/group/', methods=['POST'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
@required_token
def add_group(params: dict, **kwargs):
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


@group_page.route('/group/', methods=['GET', 'DELETE'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
@required_token
def group_handle(params: dict, **kwargs):
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


@group_page.route('/group/<int:group_id>', methods=['PUT', 'PATCH'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
@required_token
def group_edit(params: dict, group_id: int, **kwargs):
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

@group_page.route('/group/list/<string:table>/', methods=['GET'])
@get_params
@wrap_error
# @required_token
def get_table_list_by_user(params: dict, table: str, **kwargs):
    """
    Given a user id and a related element (group, experiment, project or sample), return the list of elements related
     to the user. If no valid token, and the query is for samples, the list of public samples is returned.
    :param params:
    :param id: the user id.
    :param table: the table to get the related data.
    :return: the list of elements of the table related to the user. Or the list of public samples
    """
    uid = get_uid_from_request(False)
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
@group_page.route('/group/invitation/<int:group>', methods=['PUT', 'PATCH', 'DELETE'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
@required_token
def accept(params: dict, group: int, **kwargs):
    """
    Accept or reject an invitation to join a group
    :param params:
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


@group_page.route('/group/invite/<int:invited>/<int:group>', methods=['POST'])
@wrap_error
def invite(params: dict, invited: int, group: int, **kwargs):
    """
    Invite a user to join a group
    :param params:
    :param invited: the user to invite
    :param group: the group to join
    :return:
    """
    try:
        uid = kwargs['uid']
        owner = UserController.get_user_by_uid(uid).id

        log.info(f"Invitation request from user {owner} to user {invited} to join group {group}")
        GroupController.invite(owner, invited, group)
        result = {"message": "OK"}
    except Exception as e:
        result = {"message": f"ERROR: {e}"}

    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")

