import os
import re
import asyncio
from edge_tts import Communicate

# 提取句子的函数
def extract_sentences_from_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取sentences数组中的所有句子
    sentences_match = re.search(r'const sentences = \[(.*?)\];', content, re.DOTALL)
    if not sentences_match:
        print("未找到sentences数组")
        return []
    
    sentences_text = sentences_match.group(1)
    # 提取所有句子字符串
    sentences = re.findall(r'"([^"]+)"', sentences_text)
    return sentences

# 生成音频文件的函数
async def generate_audio_files(sentences, output_dir):
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成音频文件
    for i, sentence in enumerate(sentences):
        output_file = os.path.join(output_dir, f"sentence_{i}.mp3")
        
        # 跳过已存在的文件
        if os.path.exists(output_file):
            print(f"文件已存在，跳过: {output_file}")
            continue
        
        print(f"生成音频: {sentence}")
        
        try:
            # 生成音频
            communicate = Communicate(text=sentence, voice="en-US-AriaNeural", rate="-20%")
            await communicate.save(output_file)
            print(f"生成成功: {output_file}")
        except Exception as e:
            print(f"生成失败: {sentence}, 错误: {e}")

# 生成映射文件
def generate_mapping_file(sentences, output_dir):
    mapping = {}
    for i, sentence in enumerate(sentences):
        mapping[sentence] = f"voice/game_sort/sentence_{i}.mp3"
    
    mapping_file = os.path.join(output_dir, "mapping.json")
    import json
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    
    print(f"生成映射文件: {mapping_file}")
    return mapping

if __name__ == "__main__":
    html_file = r'D:\code\test\game_sort.html'
    output_dir = r'D:\code\test\voice\game_sort'
    
    # 提取句子
    sentences = extract_sentences_from_html(html_file)
    print(f"提取到 {len(sentences)} 个句子")
    
    # 生成音频文件
    asyncio.run(generate_audio_files(sentences, output_dir))
    
    # 生成映射文件
    generate_mapping_file(sentences, output_dir)
    
    print("音频生成完成！")
