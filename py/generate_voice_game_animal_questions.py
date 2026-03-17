import os
import re
import asyncio
from edge_tts import Communicate

# 从HTML文件中提取问题描述
def extract_questions_from_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取animalQuestions数组
    pattern = r'const animalQuestions = \[(.*?)\];' 
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print("未找到animalQuestions数组")
        return []
    
    questions_text = match.group(1)
    
    # 提取每个问题的description
    descriptions = []
    pattern = r'description: "(.*?)"'
    matches = re.findall(pattern, questions_text)
    
    for i, description in enumerate(matches):
        # 去除转义字符
        description = description.replace('\\"', '"')
        descriptions.append((i+1, description))
    
    return descriptions

# 生成音频文件
async def generate_audio_files(questions, output_dir):
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    total = len(questions)
    success_count = 0
    failed_items = []
    
    print(f"开始生成 {total} 个音频文件...")
    
    for i, (index, description) in enumerate(questions):
        try:
            # 生成文件名（使用问题索引）
            filename = f"question_{index}.mp3"
            output_path = os.path.join(output_dir, filename)
            
            # 生成音频
            print(f"生成第 {index} 个音频: {description[:50]}...")
            communicate = Communicate(description, "en-US-AriaNeural", rate="-20%")
            await communicate.save(output_path)
            
            success_count += 1
            print(f"✓ 成功生成: {filename}")
            
        except Exception as e:
            print(f"✗ 生成失败 ({index}): {str(e)}")
            failed_items.append((index, description))
        
        # 每生成5个文件后休息一下，避免API限制
        if (i + 1) % 5 == 0:
            print("休息2秒...")
            await asyncio.sleep(2)
    
    print(f"\n生成完成！")
    print(f"成功: {success_count}/{total}")
    if failed_items:
        print(f"失败: {len(failed_items)} 个")
        print("失败的项目:")
        for index, description in failed_items:
            print(f"  {index}: {description[:100]}...")
    
    return failed_items

# 生成音频映射文件
def generate_audio_mapping(questions, output_dir):
    mapping = {}
    for index, description in questions:
        mapping[description] = f"voice/game_animal/question_{index}.mp3"
    
    # 保存映射到JSON文件
    import json
    mapping_file = os.path.join(output_dir, "mapping.json")
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    
    print(f"映射文件已保存到: {mapping_file}")
    return mapping

if __name__ == "__main__":
    html_file = r"D:\code\test\game_animal.html"
    output_dir = r"D:\code\test\voice\game_animal"
    
    # 提取问题
    questions = extract_questions_from_html(html_file)
    print(f"提取到 {len(questions)} 个问题")
    
    if questions:
        # 生成音频文件
        failed = asyncio.run(generate_audio_files(questions, output_dir))
        
        # 生成映射文件
        generate_audio_mapping(questions, output_dir)
        
        if failed:
            print("\n注意：有失败的音频文件需要重新生成")
        else:
            print("\n所有音频文件生成成功！")
