import os
import asyncio
from edge_tts import Communicate

# 提取game_qa.html中的问题和答案
def extract_qa_from_html():
    html_path = '../game_qa.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取问题和答案
    import re
    qa_pattern = r'question:\s*"([^"]+)",\s*correctAnswer:\s*"([^"]+)"'
    qas = re.findall(qa_pattern, content)
    
    return qas

# 生成音频文件
async def generate_audio_files(qas):
    output_dir = '../voice/game_qa'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    mapping = {}
    
    for i, (question, answer) in enumerate(qas):
        # 生成问题音频
        question_filename = f'question_{i}.mp3'
        question_filepath = os.path.join(output_dir, question_filename)
        
        communicate = Communicate(question, "en-US-AriaNeural", rate="-20%")
        await communicate.save(question_filepath)
        mapping[question] = f'voice/game_qa/{question_filename}'
        
        # 生成答案音频
        answer_filename = f'answer_{i}.mp3'
        answer_filepath = os.path.join(output_dir, answer_filename)
        
        communicate = Communicate(answer, "en-US-AriaNeural", rate="-20%")
        await communicate.save(answer_filepath)
        mapping[answer] = f'voice/game_qa/{answer_filename}'
        
        print(f"生成音频: 问题 {i+1} -> {question_filename}, 答案 -> {answer_filename}")
    
    # 保存映射为JSON
    import json
    with open(os.path.join(output_dir, 'mapping.json'), 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    
    print(f"\n生成完成，共生成 {len(qas) * 2} 个音频文件")
    print(f"映射文件已保存到: {os.path.join(output_dir, 'mapping.json')}")

if __name__ == "__main__":
    qas = extract_qa_from_html()
    print(f"提取到 {len(qas)} 个问题和答案对")
    asyncio.run(generate_audio_files(qas))