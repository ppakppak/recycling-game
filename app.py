from flask import Flask, render_template, jsonify, current_app
import random
import sys
import os

app = Flask(__name__)

# 원본 아이템 데이터
ORIGINAL_ITEMS = [
    {'name': '신문지', 'type': '종이'},
    {'name': '페트병', 'type': '플라스틱'},
    {'name': '비닐봉지', 'type': '비닐'},
    {'name': '캔', 'type': '캔'},
    {'name': '종이컵', 'type': '종이'},
    {'name': '플라스틱 용기', 'type': '플라스틱'},
    {'name': '알루미늄 캔', 'type': '캔'},
    {'name': '과자 봉지', 'type': '비닐'},
    {'name': '종이 상자', 'type': '종이'},
    {'name': '우유 팩', 'type': '종이'},
    {'name': '식용유 페트병', 'type': '플라스틱'},
    {'name': '스티로폼 용기', 'type': '비닐'},
    {'name': '세제 용기', 'type': '플라스틱'},
    {'name': '포장지', 'type': '종이'},
    {'name': '유리병', 'type': '캔'},
    {'name': '비닐 포장재', 'type': '비닐'},
    {'name': '페인트 통', 'type': '캔'}
]

# 현재 게임에서 사용할 아이템 리스트
current_items = []

def log_to_vercel(message, level="INFO"):
    """Vercel 환경에 맞는 로깅 함수"""
    print(f"[{level}] {message}", file=sys.stderr)

@app.route('/')
def index():
    try:
        log_to_vercel("Accessing index route")
        global current_items
        current_items = ORIGINAL_ITEMS.copy()
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
            "env_info": env_info,
            "route": "index"
        }), 500

@app.route('/get-item')
def get_item():
    try:
        log_to_vercel("Accessing get-item route")
        global current_items
        if not current_items:
            log_to_vercel("Resetting current_items")
            current_items = ORIGINAL_ITEMS.copy()
        
        if current_items:
            item = random.choice(current_items)
            current_items.remove(item)
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

if __name__ == '__main__':
    app.run(debug=True)
else:
    # Vercel 환경을 위한 설정
    app.debug = False

# Vercel을 위한 export
app = app