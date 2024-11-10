from flask import Flask, jsonify
from flask_cors import CORS
from repository import dynamodb, hash, sqlite, postgres
from opentelemetry.instrumentation.flask import FlaskInstrumentor
import pathlib


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_prefixed_env()
    print(app.config)
    CORS(app)

    app.config.update(config or {})

    FlaskInstrumentor().instrument_app(app)

    if app.config.get('TESTING'):
        app.db = hash.HashRepository()
    else:
        db_type = app.config.get('DB_TYPE', 'dynamodb')
        if db_type == 'sqlite':
            path = "{}/db/database.db".format(pathlib.Path(__file__).parent.parent.absolute())
            app.db = sqlite.SQLiteRepository(app.config.get('DB_PATH', path))
        elif db_type == 'dynamodb':
            db_table_name = app.config.get('DB_TABLE_NAME', 'GameTable')
            app.db = dynamodb.DynamoDBRepository(db_table_name)
        elif db_type == 'postgres':
            db_string = (f"dbname={app.config.get('DB_NAME')} user={app.config.get('DB_USER')}"
                         f" password={app.config.get('DB_PASSWORD')} host={app.config.get('DB_HOST')}")
            try:
                app.db = postgres.PostgresRepository(db_string)
            except Exception as e:
                app.logger.error(f"Error connecting to database: {e}")
                raise e

    from .game_routes import game_bp  # Assuming your blueprint is named `game_bp`
    app.register_blueprint(game_bp)

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok'})

    return app
