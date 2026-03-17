import os
import re
import asyncio
from edge_tts import Communicate

# 提取game_synonyms.html中的单词
def extract_words_from_html():
    html_path = 'game_synonyms.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取wordTranslations对象中的单词
    word_pattern = r'"([a-zA-Z\s]+)":\s*"[^"]+"'
    words = re.findall(word_pattern, content)
    
    # 去重并排序
    unique_words = sorted(list(set(words)))
    return unique_words

# 生成音频文件
async def generate_audio_files(words):
    # 目标目录
    output_dir = r'D:\code\test\voice\game_synonyms'
    if not os.path.exists(output_dir):
        print(f"创建目录: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)
    
    mapping = {}
    success_count = 0
    
    # 直接生成所有音频文件
    for i, word in enumerate(words):
        try:
            # 替换空格为下划线，用于文件名
            filename = f'word_{i}.mp3'
            filepath = os.path.join(output_dir, filename)
            
            # 生成音频
            print(f"开始生成: {word}")
            communicate = Communicate(word, "en-US-AriaNeural", rate="-20%")
            await communicate.save(filepath)
            
            # 检查文件是否生成成功
            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                # 构建映射
                mapping[word] = f'voice/game_synonyms/{filename}'
                
                print(f"生成音频成功: {word} -> {filename} (大小: {os.path.getsize(filepath)} 字节)")
                success_count += 1
            else:
                print(f"生成音频失败: {word} -> 文件为空或不存在")
                # 删除空文件
                if os.path.exists(filepath):
                    os.remove(filepath)
        except Exception as e:
            print(f"生成音频失败: {word} -> {e}")
    
    # 保存映射为JSON
    import json
    mapping_file = os.path.join(output_dir, 'mapping.json')
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    
    print(f"\n生成完成，共生成 {success_count} 个音频文件")
    print(f"映射文件已保存到: {mapping_file}")

if __name__ == "__main__":
    words = extract_words_from_html()
    print(f"提取到 {len(words)} 个单词")
    # 生成所有单词的音频文件
    print(f"生成所有 {len(words)} 个单词的音频文件")
    asyncio.run(generate_audio_files(words))
