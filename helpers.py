from functools import wraps
import secrets
from flask import request, jsonify, json
import decimal

from models import Dog

def token_required(flask_func):
    @wraps(flask_func)
    def decorated(*args, **kwargs):
        token = None

        if 'x-api-key' in request.headers:
            token = request.headers['x-api-key']
        if not token:
            return jsonify({'message': 'Token is missing.'}), 401
        
        try:
            current_token = Dog.query.filter_by(token = token)
        except:
            owner = Dog.query.token.filter_by(token = token)

            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Token is invalid'})
        return flask_func(current_token, *args, **kwargs)
    return decorated
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)