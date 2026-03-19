from flask import Flask, jsonify, send_from_directory, request
import os
import json
import asyncio
from edge_tts import Communicate
import io
import base64

app = Flask(__name__, static_folder='..', static_url_path='/')

# 启用CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# 提供游戏数据的API
@app.route('/api/game/<game_name>')
def get_game_data(game_name):
    try:
        # 读取JSON文件
        json_path = os.path.join('..', 'data', f'{game_name}.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'Game data not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 根路径重定向到index.html
@app.route('/')
def index():
    return send_from_directory('..', 'index.html')

# 提供静态文件
@app.route('/<path:path>')
def static_file(path):
    return send_from_directory('..', path)

# 语音生成API
@app.route('/api/tts', methods=['GET'])
def generate_tts():
    try:
        # 获取请求数据
        text = request.args.get('text', '')
        page = request.args.get('game', 'default')  # 默认页面为default
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # 生成文件名（使用文本的哈希值作为文件名）
        import hashlib
        text_hash = hashlib.md5(text.encode()).hexdigest()
        audio_file_path = os.path.join('..', 'voice', page, f'{text_hash}.mp3')
        
        # 确保页面对应的目录存在
        os.makedirs(os.path.join('..', 'voice', page), exist_ok=True)
        
        # 检查文件是否存在
        if os.path.exists(audio_file_path):
            print(f"Using existing audio file: {audio_file_path}")
            # 读取现有文件
            with open(audio_file_path, 'rb') as f:
                audio_data = f.read()
        else:
            print(f"Generating new audio for: {text} (page: {page})")
            # 生成语音
            async def generate_audio():
                communicate = Communicate(text, "en-US-AriaNeural", rate="-20%")
                audio_data = io.BytesIO()
                async for chunk in communicate.stream():
                    if chunk['type'] == 'audio':
                        audio_data.write(chunk['data'])
                audio_data.seek(0)
                return audio_data
            
            # 运行异步函数
            audio_stream = asyncio.run(generate_audio())
            audio_data = audio_stream.read()
            
            # 保存到文件
            with open(audio_file_path, 'wb') as f:
                f.write(audio_data)
        
        # 直接返回音频文件
        from flask import send_file
        import tempfile
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
        
        # 发送文件
        return send_file(temp_file_path, mimetype='audio/mpeg', as_attachment=False)
    except Exception as e:
        print(f"Error generating TTS: {e}")
        return jsonify({'error': str(e)}), 500

# 打卡记录API
@app.route('/api/checkin', methods=['POST'])
def checkin():
    try:
        # 打卡记录文件路径
        checkin_file = os.path.join('..', 'data', 'checkin_records.json')
        
        # 确保文件存在
        if not os.path.exists(checkin_file):
            with open(checkin_file, 'w', encoding='utf-8') as f:
                json.dump({'records': []}, f, ensure_ascii=False, indent=2)
        
        # 读取现有记录
        with open(checkin_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 获取今天的日期（格式：YYYY-MM-DD）
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 检查今天是否已经打卡
        for record in data['records']:
            if record['date'] == today:
                return jsonify({'success': False, 'message': '今天已经打卡过了'})
        
        # 添加新的打卡记录
        data['records'].append({
            'date': today,
            'timestamp': datetime.now().isoformat()
        })
        
        # 保存更新后的记录
        with open(checkin_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return jsonify({'success': True, 'message': '打卡成功'})
    except Exception as e:
        print(f"Error during checkin: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

# 检查打卡状态API
@app.route('/api/checkin/status')
def checkin_status():
    try:
        # 打卡记录文件路径
        checkin_file = os.path.join('..', 'data', 'checkin_records.json')
        
        # 确保文件存在
        if not os.path.exists(checkin_file):
            return jsonify({'checked': False})
        
        # 读取现有记录
        with open(checkin_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 获取今天的日期（格式：YYYY-MM-DD）
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 检查今天是否已经打卡
        checked = any(record['date'] == today for record in data['records'])
        
        return jsonify({'checked': checked})
    except Exception as e:
        print(f"Error checking checkin status: {e}")
        return jsonify({'checked': False})

# 获取打卡记录API
@app.route('/api/checkin/records')
def get_checkin_records():
    try:
        # 打卡记录文件路径
        checkin_file = os.path.join('..', 'data', 'checkin_records.json')
        
        # 确保文件存在
        if not os.path.exists(checkin_file):
            return jsonify({'records': []})
        
        # 读取现有记录
        with open(checkin_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return jsonify(data)
    except Exception as e:
        print(f"Error getting checkin records: {e}")
        return jsonify({'records': []})

# 统计数据API
@app.route('/api/stats')
def get_stats():
    try:
        # 打卡记录文件路径
        checkin_file = os.path.join('..', 'data', 'checkin_records.json')
        # 游戏记录文件路径
        game_file = os.path.join('..', 'data', 'game_records.json')
        
        # 确保文件存在
        if not os.path.exists(checkin_file):
            with open(checkin_file, 'w', encoding='utf-8') as f:
                json.dump({'records': []}, f, ensure_ascii=False, indent=2)
        
        if not os.path.exists(game_file):
            with open(game_file, 'w', encoding='utf-8') as f:
                json.dump({'plays': 0}, f, ensure_ascii=False, indent=2)
        
        # 读取打卡记录
        with open(checkin_file, 'r', encoding='utf-8') as f:
            checkin_data = json.load(f)
        
        # 读取游戏记录
        with open(game_file, 'r', encoding='utf-8') as f:
            game_data = json.load(f)
        
        # 计算总打卡天数
        total_checkins = len(checkin_data['records'])
        
        # 计算连续打卡天数
        continuous_checkins = 0
        if total_checkins > 0:
            # 按日期排序（降序）
            sorted_records = sorted(checkin_data['records'], key=lambda x: x['date'], reverse=True)
            
            # 获取今天的日期
            from datetime import datetime, timedelta
            today = datetime.now().strftime('%Y-%m-%d')
            
            # 检查今天是否打卡
            if sorted_records[0]['date'] == today:
                continuous_checkins = 1
                # 从昨天开始往前检查
                current_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                for record in sorted_records[1:]:
                    if record['date'] == current_date:
                        continuous_checkins += 1
                        current_date = (datetime.strptime(current_date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
                    else:
                        break
        
        # 获取游戏次数
        game_plays = game_data.get('plays', 0)
        
        return jsonify({
            'continuousCheckins': continuous_checkins,
            'totalCheckins': total_checkins,
            'gamePlays': game_plays
        })
    except Exception as e:
        print(f"Error getting stats: {e}")
        return jsonify({
            'continuousCheckins': 0,
            'totalCheckins': 0,
            'gamePlays': 0
        })

if __name__ == '__main__':
    # 确保data目录存在
    os.makedirs(os.path.join('..', 'data'), exist_ok=True)
    # 在8090端口运行
    app.run(host='0.0.0.0', port=8090, debug=True)