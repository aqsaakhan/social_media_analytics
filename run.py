from app import create_app, socketio
from app.models import init_db

app = create_app()

if __name__ == '__main__':
    init_db()  # Initialize the database
    socketio.run(app, debug=True)