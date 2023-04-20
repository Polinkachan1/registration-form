from flask import Blueprint, jsonify, Response, request
from sqlalchemy import select

from data import db_session
from data.users import Users

blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=['GET'])
def get_users() -> Response:
    db_sess = db_session.create_session()
    result = db_sess.execute(
        select(Users)
    )
    users = result.all()
    fields = ('id', 'surname', 'name', 'age',
                  'position', 'speciality',
                  'address', 'email',
                  'hashed_password', 'modified_date')
    users_dict = [user.to_dict(only=fields) for user, in users]
    return jsonify({
        'users': users_dict,
    })


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db_sess = db_session.create_session()
    result = db_sess.execute(
        select(Users)
        .where(Users.id == user_id)
    )
    user = result.scalar()
    if user is None:
        return jsonify({'error': 'Not found'}), 404
    fields = ('id', 'surname', 'name', 'age',
                  'position', 'speciality',
                  'address', 'email',
                  'hashed_password', 'modified_date')
    return jsonify({
        'user': user.to_dict(only=fields),
    })


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'}), 400
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age',
                  'position', 'speciality',
                  'address', 'email',
                  'hashed_password', 'modified_date']):
        fields_str = ', '.join(['id', 'surname', 'name', 'age',
                                'position', 'speciality', 'address', 'email',
                                'hashed_password', 'modified_date'])
        return jsonify({'error': f'required fields: {fields_str}'}), 400

    db_sess = db_session.create_session()
    user = Users(
        # id=request.json['id'],
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        hasched_password=request.json['hashed_password'],
        modified_date=request.json['modified_date'],
    )
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'}), 201


@blueprint.route('/api/jobs/<int:users_id>', methods=['DELETE'])
def delete_users(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(Users).get(users_id)

    if not users:
        return jsonify({'error': 'Not found'})
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:users_id>', methods=['PUT'])
def edit_jobs(users_id):
    if not request.json:
        return jsonify({"error": "Empty request"})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age',
                  'position', 'speciality',
                  'address', 'email',
                  'hashed_password', 'modified_date']):
        return jsonify({"error": "Bad request"})

    db_sess = db_session.create_session()
    users = db_sess.query(Users).get(users_id)

    if not users:
        return jsonify({'error': 'Not found'})

    users.update(request.json)
    db_sess.commit()
    return jsonify({'success': 'OK'})