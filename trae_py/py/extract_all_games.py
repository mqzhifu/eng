import os
import re
import json

# 提取游戏数据的函数
def extract_game_data(html_content, game_name):
    if game_name == 'game_animal':
        # 提取animalQuestions数组
        pattern = r'const animalQuestions = \[(.*?)\];'
        match = re.search(pattern, html_content, re.DOTALL)
        if match:
            questions_str = match.group(1)
            # 处理字符串，使其成为有效的JSON
            questions_str = questions_str.strip() 
            questions_str = re.sub(r'\s+', ' ', questions_str)
            questions_str = re.sub(r'(\w+):', r'"\1":', questions_str)
            questions_str = re.sub(r':\s*\'([^\']+)\'', r': "\1"', questions_str)
            questions_str = re.sub(r',\s*([\]})])', r' \1', questions_str)
            questions_json = f'[{questions_str}]'
            try:
                questions = json.loads(questions_json)
                return questions
            except json.JSONDecodeError as e:
                print(f"Error parsing {game_name}: {e}")
                return None
    elif game_name == 'game_antonyms':
        # 提取antonyms数组
        pattern = r'const antonyms = \[(.*?)\];'
        match = re.search(pattern, html_content, re.DOTALL)
        if match:
            antonyms_str = match.group(1)
            # 处理字符串，使其成为有效的JSON
            antonyms_str = antonyms_str.strip()
            antonyms_str = re.sub(r'\s+', ' ', antonyms_str)
            antonyms_str = re.sub(r'(\w+):', r'"\1":', antonyms_str)
            antonyms_str = re.sub(r':\s*\'([^\']+)\'', r': "\1"', antonyms_str)
            antonyms_str = re.sub(r',\s*([\]})])', r' \1', antonyms_str)
            antonyms_json = f'[{antonyms_str}]'
            try:
                antonyms = json.loads(antonyms_json)
                return antonyms
            except json.JSONDecodeError as e:
                print(f"Error parsing {game_name}: {e}")
                return None
    elif game_name == 'game_memory':
        # 提取phrases数组
        pattern = r'const phrases = \[(.*?)\];'
        match = re.search(pattern, html_content, re.DOTALL)
        if match:
            phrases_str = match.group(1)
            # 处理字符串，使其成为有效的JSON
            phrases_str = phrases_str.strip()
            phrases_str = re.sub(r'\s+', ' ', phrases_str)
            phrases_str = re.sub(r'(\w+):', r'"\1":', phrases_str)
            phrases_str = re.sub(r':\s*\'([^\']+)\'', r': "\1"', phrases_str)
            phrases_str = re.sub(r',\s*([\]})])', r' \1', phrases_str)
            phrases_json = f'[{phrases_str}]'
            try:
                phrases = json.loads(phrases_json)
                return phrases
            except json.JSONDecodeError as e:
                print(f"Error parsing {game_name}: {e}")
                return None
    elif game_name == 'game_qa':
        # 提取questions数组
        pattern = r'const questions = \[(.*?)\];'
        match = re.search(pattern, html_content, re.DOTALL)
        if match:
            questions_str = match.group(1)
            # 处理字符串，使其成为有效的JSON
            questions_str = questions_str.strip()
            questions_str = re.sub(r'\s+', ' ', questions_str)
            questions_str = re.sub(r'(\w+):', r'"\1":', questions_str)
            questions_str = re.sub(r':\s*\'([^\']+)\'', r': "\1"', questions_str)
            questions_str = re.sub(r',\s*([\]})])', r' \1', questions_str)
            questions_json = f'[{questions_str}]'
            try:
                questions = json.loads(questions_json)
                return questions
            except json.JSONDecodeError as e:
                print(f"Error parsing {game_name}: {e}")
                return None
    elif game_name == 'game_rencheng':
        # 提取sentences数组
        pattern = r'const sentences = \[(.*?)\];'
        match = re.search(pattern, html_content, re.DOTALL)
        if match:
            sentences_str = match.group(1)
            # 处理字符串，使其成为有效的JSON
            sentences_str = sentences_str.strip()
            sentences_str = re.sub(r'\s+', ' ', sentences_str)
            sentences_str = re.sub(r'(\w+):', r'"\1":', sentences_str)
            sentences_str = re.sub(r':\s*\'([^\']+)\'', r': "\1"', sentences_str)
            sentences_str = re.sub(r',\s*([\]})])', r' \1', sentences_str)
            sentences_json = f'[{sentences_str}]'
            try:
                sentences = json.loads(sentences_json)
                return sentences
            except json.JSONDecodeError as e:
                print(f"Error parsing {game_name}: {e}")
                return None
    elif game_name == 'game_sort':
        # 提取sentences数组
        pattern = r'const sentences = \[(.*?)\];'
        match = re.search(pattern, html_content, re.DOTALL)
        if match:
            sentences_str = match.group(1)
            # 处理字符串，使其成为有效的JSON
            sentences_str = sentences_str.strip()
            sentences_str = re.sub(r'\s+', ' ', sentences_str)
            sentences_str = re.sub(r'(\w+):', r'"\1":', sentences_str)
            sentences_str = re.sub(r':\s*\'([^\']+)\'', r': "\1"', sentences_str)
            sentences_str = re.sub(r',\s*([\]})])', r' \1', sentences_str)
            sentences_json = f'[{sentences_str}]'
            try:
                sentences = json.loads(sentences_json)
                return sentences
            except json.JSONDecodeError as e:
                print(f"Error parsing {game_name}: {e}")
                return None
    elif game_name == 'game_synonyms':
        # 提取synonyms数组
        pattern = r'const synonyms = \[(.*?)\];'
        match = re.search(pattern, html_content, re.DOTALL)
        if match:
            synonyms_str = match.group(1)
            # 处理字符串，使其成为有效的JSON
            synonyms_str = synonyms_str.strip()
            synonyms_str = re.sub(r'\s+', ' ', synonyms_str)
            synonyms_str = re.sub(r'(\w+):', r'"\1":', synonyms_str)
            synonyms_str = re.sub(r':\s*\'([^\']+)\'', r': "\1"', synonyms_str)
            synonyms_str = re.sub(r',\s*([\]})])', r' \1', synonyms_str)
            synonyms_json = f'[{synonyms_str}]'
            try:
                synonyms = json.loads(synonyms_json)
                return synonyms
            except json.JSONDecodeError as e:
                print(f"Error parsing {game_name}: {e}")
                return None
    elif game_name == 'game_translate':
        # 提取questions数组
        pattern = r'const questions = \[(.*?)\];'
        match = re.search(pattern, html_content, re.DOTALL)
        if match:
            questions_str = match.group(1)
            # 处理字符串，使其成为有效的JSON
            questions_str = questions_str.strip()
            questions_str = re.sub(r'\s+', ' ', questions_str)
            questions_str = re.sub(r'(\w+):', r'"\1":', questions_str)
            questions_str = re.sub(r':\s*\'([^\']+)\'', r': "\1"', questions_str)
            questions_str = re.sub(r',\s*([\]})])', r' \1', questions_str)
            questions_json = f'[{questions_str}]'
            try:
                questions = json.loads(questions_json)
                return questions
            except json.JSONDecodeError as e:
                print(f"Error parsing {game_name}: {e}")
                return None
    elif game_name == 'game_verb':
        # 提取verbQuestions数组
        pattern = r'const verbQuestions = \[(.*?)\];'
        match = re.search(pattern, html_content, re.DOTALL)
        if match:
            questions_str = match.group(1)
            # 处理字符串，使其成为有效的JSON
            questions_str = questions_str.strip()
            questions_str = re.sub(r'\s+', ' ', questions_str)
            questions_str = re.sub(r'(\w+):', r'"\1":', questions_str)
            questions_str = re.sub(r':\s*\'([^\']+)\'', r': "\1"', questions_str)
            questions_str = re.sub(r',\s*([\]})])', r' \1', questions_str)
            questions_json = f'[{questions_str}]'
            try:
                questions = json.loads(questions_json)
                return questions
            except json.JSONDecodeError as e:
                print(f"Error parsing {game_name}: {e}")
                return None
    return None

# 处理所有游戏页面
def process_all_games():
    # 确保data目录存在
    os.makedirs('data', exist_ok=True)
    
    # 游戏页面列表
    game_pages = [
        'game_animal.html',
        'game_antonyms.html',
        'game_memory.html',
        'game_qa.html',
        'game_rencheng.html',
        'game_sort.html',
        'game_synonyms.html',
        'game_translate.html',
        'game_verb.html'
    ]
    
    for page in game_pages:
        game_name = page.replace('.html', '')
        print(f"处理游戏: {game_name}")
        
        # 读取HTML文件
        try:
            with open(os.path.join('..', page), 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"文件不存在: {page}")
            continue
        
        # 提取数据
        data = extract_game_data(content, game_name)
        if data:
            # 保存为JSON文件
            json_file = os.path.join('..', 'data', f'{game_name}.json')
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"保存数据到: {json_file}")
        else:
            print(f"未找到数据: {game_name}")

if __name__ == "__main__":
    # 切换到py目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    process_all_games()
