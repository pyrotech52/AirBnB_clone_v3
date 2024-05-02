#!/usr/bin/python3
'''create users'''
from flask import jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False)
def get_users():
    """ list users """

    user = storage.all(User).values()
    return jsonify([user.to_dict() for user in user])


@app_views.route('/users/<user_id>', strict_slashes=False)
def gets_user(user_id):
    """ list user """

    user = storage.all(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        return abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ delete user """

    user = storage.all(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def create_user():
    """ add user """
    if request.content_type != 'application/json':
        return abort(400, 'Not JSON')
    if not request.get_json():
        return abort(400, 'Not JSON')
    data = request.get_json()
    if 'email' not in data:
        return abort(400, 'Enter email')
    if 'password' not in data:
        return abort(400, 'Enter Password')

    user = User(**data)
    user.save()

    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ add user """
    user = storage.get(User, user_id)
    if user:
        if not request.get_json():
            return abort(404, ' not JSON')
        if request.content_type != 'application/json':
            return abort(404, 'not JSON')
        data = request.get_json()

        ignore_keys = ['id,' 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        return abort(404)
