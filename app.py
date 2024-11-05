from flask import Flask, render_template, jsonify
import random

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

@app.route('/')
def index():
    try:
        global current_items
        current_items = ORIGINAL_ITEMS.copy()
        return render_template('index.html')
    except Exception as e:
        print(f"Error in index route: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/get-item')
def get_item():
    try:
        global current_items
        if not current_items:
            current_items = ORIGINAL_ITEMS.copy()
        
        if current_items:
            item = random.choice(current_items)
            current_items.remove(item)
            return jsonify(item)
        return jsonify({'name': None, 'type': None})
    except Exception as e:
        print(f"Error in get-item route: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 개발 환경에서만 실행되도록 수정
if __name__ == '__main__':
    app.run(debug=True)
else:
    # Vercel에서 실행될 때는 app 변수를 직접 사용
    pass

# Vercel을 위한 export
app = app