from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True,
                           description='Email of the user'),
    'password': fields.String(required=True,
                              description='Password of the user')
})


@api.route('/')
class UserList(Resource):
    @jwt_required
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(409, 'Email already registered')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        current_user = get_jwt_identity()
        if not current_user["is_admin"]:
            return {'error': 'Only admins can create users.'}, 403

        user_data = api.payload

        # Simulate email uniqueness check
        # (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered.'}, 409

        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'message': 'User successfully created'
                }, 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of users
        (no need to edit as the dict doesn't include password)"""
        users = facade.get_users()
        return [user.to_dict() for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID
        (no need to edit as the dict doesn't include password)"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found.'}, 404
        return user.to_dict(), 200

    @jwt_required()
    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        user_data = api.payload

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found.'}, 404

        current_user = get_jwt_identity()
        if not current_user["id"] == user_id:
            return {'error': 'Unauthorized action.'}, 403

        if not current_user["is_admin"] and \
           ("email" in user_data or "password" in user_data):
            return {'error': '"You cannot modify email or password.'}, 400

        email = user_data["email"]
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        try:
            facade.update_user(user_id, user_data)
            return user.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400
