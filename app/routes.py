from flask import Blueprint, render_template, jsonify, request, current_app
from services.message_queue import setup_queue, send_message
from app.models import get_db_connection  # Add this import
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/post', methods=['POST'])
def create_post():
    data = request.json
    content = data.get('content')
    if content:
        try:
            channel = setup_queue()
            send_message(channel, content)
            current_app.logger.info(f"Message sent to queue: {content}")
            return jsonify({"status": "success"}), 200
        except Exception as e:
            current_app.logger.error(f"Error sending message to queue: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify({"status": "error", "message": "No content provided"}), 400

@main.route('/api/posts_with_analytics')
def get_posts_with_analytics():
    try:
        conn = get_db_connection()
        posts = conn.execute('SELECT * FROM posts ORDER BY timestamp DESC LIMIT 10').fetchall()
        result = []
        for post in posts:
            analytics = conn.execute('SELECT type, value FROM analytics WHERE post_id = ?', (post['id'],)).fetchall()
            post_data = {
                'id': post['id'],
                'content': post['content'],
                'timestamp': post['timestamp'],
                'analytics': [dict(a) for a in analytics]
            }
            result.append(post_data)
            current_app.logger.info(f"Post ID: {post['id']}, Content: {post['content']}")
            current_app.logger.info(f"Analytics: {post_data['analytics']}")
        conn.close()
        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error fetching posts with analytics: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500