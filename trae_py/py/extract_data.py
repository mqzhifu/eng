import re
import json
import os

# 提取HTML中的questions数组
def extract_questions(html_content):
    # 使用正则表达式匹配questions数组
    pattern = r'const questions = \[(.*?)\];' 
    match = re.search(pattern, html_content, re.DOTALL)
    if match:
        # 提取数组内容
        questions_str = match.group(1)
        # 处理字符串，使其成为有效的JSON
        questions_str = questions_str.strip()
        
        # 修复JavaScript对象到JSON的转换
        # 1. 移除多余的空格
        questions_str = re.sub(r'\s+', ' ', questions_str)
        # 2. 确保属性名用双引号包围
        questions_str = re.sub(r'(\w+):', r'"\1":', questions_str)
        # 3. 处理字符串值，确保用双引号包围
        # 处理单引号包围的字符串
        questions_str = re.sub(r':\s*\'([^\']+)\'', r': "\1"', questions_str)
        # 处理时间格式如"9:00"
        questions_str = re.sub(r':\s*("[0-9]+:[0-9]+")', r': \1', questions_str)
        # 4. 修复布尔值和数字
        questions_str = re.sub(r':\s*(true|false|null)', r': \1', questions_str)
        # 5. 移除末尾的逗号
        questions_str = re.sub(r',\s*([\]})])', r' \1', questions_str)
        
        # 转换为JSON格式
        questions_json = f'[{questions_str}]'
        
        # 解析JSON
        try:
            questions = json.loads(questions_json)
            return questions
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            # 打印出错的部分
            error_pos = e.pos
            start = max(0, error_pos - 50)
            end = min(len(questions_json), error_pos + 50)
            print(f"出错位置附近: {questions_json[start:end]}")
            return None
    return None

# 处理所有HTML文件
def process_html_files():
    # 确保data目录存在
    os.makedirs('data', exist_ok=True)
    
    # 获取所有HTML文件
    html_files = [f for f in os.listdir('.') if f.endswith('.html') and f.startswith('game_')]
    
    for html_file in html_files:
        print(f"处理文件: {html_file}")
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取questions
        questions = extract_questions(content)
        if questions:
            # 生成JSON文件名
            json_file = os.path.join('data', f"{html_file.replace('.html', '')}.json")
            # 保存为JSON文件
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(questions, f, ensure_ascii=False, indent=2)
            print(f"保存数据到: {json_file}")
        else:
            print(f"未找到questions数组: {html_file}")

if __name__ == "__main__":
    # 切换到项目根目录
    os.chdir('..')
    process_html_files()
