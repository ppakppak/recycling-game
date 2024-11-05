from flask import Flask, render_template, jsonify
import random
import sys
import os

ORIGINAL_ITEMS = [
    {"name": "사과", "type": "과일"},
    {"name": "바나나", "type": "과일"},
    {"name": "당근", "type": "채소"},
    {"name": "감자", "type": "채소"}
]

# 전역 변수를 앱 컨텍스트 내부로 이동
class GameState:
    def __init__(self):
        self.current_items = []

game_state = GameState()

def create_app():
    app = Flask(__name__)
    
    def log_to_vercel(message, level="INFO"):
        """Vercel 환경에 맞는 로깅 함수"""
        print(f"[{level}] {message}", file=sys.stderr, flush=True)

    @app.route('/')
    def index():
        try:
            log_to_vercel("Accessing index route")
            game_state.current_items = ORIGINAL_ITEMS.copy()
            log_to_vercel("Successfully initialized current_items")
            
            # 환경 정보 로깅
            env_info = {
                "VERCEL_ENV": os.environ.get("VERCEL_ENV", "unknown"),
                "PYTHON_VERSION": sys.version,
                "FLASK_ENV": os.environ.get("FLASK_ENV", "unknown"),
                "PWD": os.environ.get("PWD", "unknown"),
            }
            log_to_vercel(f"Environment info: {env_info}")
            
            return render_template('index.html')
        except Exception as e:
            error_msg = f"Error in index route: {str(e)}"
            log_to_vercel(error_msg, "ERROR")
            return jsonify({
                "error": str(e),
                "route": "index"
            }), 500

    @app.route('/get-item')
    def get_item():
        try:
            log_to_vercel("Accessing get-item route")
            if not game_state.current_items:
                log_to_vercel("Resetting current_items")
                game_state.current_items = ORIGINAL_ITEMS.copy()
            
            if game_state.current_items:
                item = random.choice(game_state.current_items)
                game_state.current_items.remove(item)
                log_to_vercel(f"Successfully returned item: {item}")
                return jsonify(item)
            
            log_to_vercel("No items available")
            return jsonify({'name': None, 'type': None})
        except Exception as e:
            error_msg = f"Error in get-item route: {str(e)}"
            log_to_vercel(error_msg, "ERROR")
            return jsonify({
                "error": str(e),
                "route": "get-item"
            }), 500

    return app

# 앱 인스턴스 생성
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# Vercel을 위한 export
app = app