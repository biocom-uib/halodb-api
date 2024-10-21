import json

from flask import Blueprint
from flask import Response, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from typing import Optional

from api import log
from api.auth import required_token, not_required_token
from api.controllers.GroupController import GroupController
from api.controllers.ProjectController import ProjectController
from api.controllers.UserController import UserController
from api.decorators import wrap_error, get_params, log_params
from api.utils import serialize_datetime

project_page = Blueprint('project_page', __name__)

# limiter = Limiter(get_remote_address)


# ##############################################################
# Project handling
# ##############################################################
@project_page.route('/project/', methods=['GET', 'POST'])
@wrap_error
# # @limiter.limit("100/minute")
# @get_params
# @log_params
@required_token
def create_project(params: dict, **kwargs):
    # TODO: link to user
    message = ''
    result_status = 200

    if request.method == 'GET':
        log.info('Request received for list of projects')
        resp = ProjectController.list_projects()
        message = json.dumps(resp, default=serialize_datetime)
        result_status = 200
    elif request.method == 'POST':
        log.info('Request received for creating a new project')
        try:
            new_project = ProjectController.create_project(params)

            message = {'status': 'success',
                       'message': 'Project created',
                       'project': new_project
                       }
            result_status = 200
            log.info(f'Project with id "{new_project.id}" created')
        except Exception as e:
            message = {'status': 'error',
                       'message': str(e)
                       }
            result_status = 400

    # return Response(response=json.dumps(message, default=serialize_datetime),
    return Response(response=json.dumps(message, default=str),
                    status=result_status,
                    mimetype="application/json")


@project_page.route('/project/<int:id>/', methods=['GET', 'DELETE'])
@wrap_error
# @limiter.limit("100/minute")
# @get_params
# @log_params
@required_token
def project_handle(project_id: Optional[int] = None, **kwargs):
    """
    Handle the project with the given id. (Retrieves or deletes it)
    If no project_id is provided, return a list of all projects for the user.
    TODO: link to user. Only the user that created the project should be able to delete it.
    :param project_id:
    :param kwargs:
    :return:
    """
    result_status = 200
    message = ''

    if request.method == 'GET':
        log.info(f'GET request received for project {project_id = }')
        prj = ProjectController.get_project_by_id(project_id)
        message = prj
        result_status = 200

    if request.method == 'DELETE':
        log.info(f'DELETE request received for project {project_id = }')
        try:
            ProjectController.delete_project(project_id)
            message = {'status': 'success',
                       'message': 'Project deleted'
                       }
            result_status = 200
            log.info(f'Project with {project_id = } deleted')
        except Exception as e:
            log.info(f'Error deleting project with {project_id = }: {str(e)}')
            message = {'status': 'error',
                       'message': str(e)
                       }
            result_status = 400

    return Response(response=json.dumps(message, default=serialize_datetime),
                    status=result_status,
                    mimetype="application/json")


@project_page.route('/project/<int:id>', methods=['PUT', 'PATCH'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
@required_token
def project_edit(params: dict, id: Optional[int] = None, **kwargs):
    # TODO: link to user
    log.info(f'PUT/PATCH request received for project {id = } with {params = }')

    result_status = 200
    message = ''
    try:
        ProjectController.update_project(id, params)
        updated = ProjectController.get_project_by_id(id)
        message = {'status': 'success',
                   'message': 'Project updated',
                   'project': updated
                   }
        result_status = 200
        log.info(f'Project with id = {updated.id} updated')
    except Exception as e:
        log.info(f'Error updating project with {id = }: {str(e)}')
        message = {'status': 'error',
                   'message': str(e)
                   }
        result_status = 400

    # return Response(response=json.dumps(message, default=serialize_datetime),
    return Response(response=json.dumps(message, default=str),
                    status=result_status,
                    mimetype="application/json")


@wrap_error
@project_page.route('/project/<int:id>/list/', methods=['GET'])
# @limiter.limit("100/minute")
@get_params
@log_params
@required_token
def project_get_samples(params: dict, id: Optional[int] = None, **kwargs):
    """
    Retrieves a list of samples related to the project.
    TODO: link to user
    :param params:
    :param id:
    :param kwargs:
    :return:
    """
    result_status = 200
    message = ''

    # if request.method == 'GET':
    #     log.info(f'GET request received for samples in project {id = } with {params = }')
    #     experiments = ExperimentController.get_by_project(id, params['project_id'])
    #     message = experiments
    #     result_status = 200

    return Response(response=json.dumps(message, default=serialize_datetime),
                    status=result_status,
                    mimetype="application/json")

