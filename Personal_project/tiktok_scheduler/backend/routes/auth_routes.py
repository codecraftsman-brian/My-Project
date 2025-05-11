from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth_service import AuthService
from jsonschema import validate
import logging

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()
logger = logging.getLogger(__name__)

# JSON schemas for validation
register_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "minLength": 3, "maxLength": 50},
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string", "minLength": 8}
    },
    "required": ["username", "email", "password"]
}

login_schema = {
    "type": "object",
    "properties": {
        "username_or_email": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["username_or_email", "password"]
}

change_password_schema = {
    "type": "object",
    "properties": {
        "current_password": {"type": "string"},
        "new_password": {"type": "string", "minLength": 8}
    },
    "required": ["current_password", "new_password"]
}

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        validate(instance=data, schema=register_schema)
        
        user_id = auth_service.register_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user_id
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'An error occurred during registration'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        validate(instance=data, schema=login_schema)
        
        auth_result = auth_service.authenticate_user(
            username_or_email=data['username_or_email'],
            password=data['password']
        )
        
        return jsonify(auth_result), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'An error occurred during login'}), 500

@auth_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    try:
        user_id = get_jwt_identity()
        user = auth_service.get_user_by_id(user_id)
        
        return jsonify(user.to_dict()), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f"Get user error: {str(e)}")
        return jsonify({'error': 'An error occurred while retrieving user information'}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    try:
        user_id = get_jwt_identity()
        data = request.json
        validate(instance=data, schema=change_password_schema)
        
        auth_service.change_password(
            user_id=user_id,
            current_password=data['current_password'],
            new_password=data['new_password']
        )
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Change password error: {str(e)}")
        return jsonify({'error': 'An error occurred while changing the password'}), 500

@auth_bp.route('/delete-account', methods=['POST'])
@jwt_required()
def delete_account():
    try:
        user_id = get_jwt_identity()
        data = request.json
        
        if 'password' not in data:
            return jsonify({'error': 'Password is required'}), 400
        
        auth_service.delete_user(
            user_id=user_id,
            password=data['password']
        )
        
        return jsonify({'message': 'Account deleted successfully'}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Delete account error: {str(e)}")
        return jsonify({'error': 'An error occurred while deleting the account'}), 500