from flask import Blueprint, jsonify, request, current_app
import hashlib
import base64
import random
import string
from .discover import Guess, WrongAttempt

game_bp = Blueprint('game_bp', __name__)


def hash_password(password, salt):
    """Hash a password with the given salt."""
    hasher = hashlib.sha256()
    hasher.update(f"{salt}{password}".encode('utf-8'))
    return hasher.hexdigest()


@game_bp.route('/create', methods=['POST'])
def create_game():
    password = request.json['password']
    encoded_password = base64.b64encode(password.encode('utf-8')).decode()
    game_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    data = {'password': f"{encoded_password}", 'attempts': []}
    current_app.db.store(game_id, data)
    return jsonify({'game_id': game_id})


@game_bp.route('/guess/<game_id>', methods=['POST'])
def guess(game_id):
    try:
        data = current_app.db.retrieve(game_id)
        myguess = request.json['guess']
        decoded_password = base64.b64decode(data['password']).decode()
        guess = Guess(decoded_password)
        try:
            guess.attempt(myguess)
        except WrongAttempt as e:
            return jsonify({'result': str(e)})
        return jsonify({'result': 'Correct'})
    except KeyError:
        current_app.logger.error(f"Game {game_id} not found")
        return jsonify({'error': 'Game not found'}), 404
