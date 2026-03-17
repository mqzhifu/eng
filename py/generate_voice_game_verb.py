import os
import json
import asyncio
import edge_tts

# 从 game_verb.html 提取英语句子
def extract_sentences():
    with open('game_verb.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 allQuestions 数组中的句子
    sentence_pairs = []
    # 找到 allQuestions 开始和结束的位置
    start_idx = content.find('const allQuestions = [')
    if start_idx == -1:
        print('未找到 allQuestions 数组')
        return sentence_pairs
    
    end_idx = content.find('];', start_idx)
    if end_idx == -1:
        print('未找到 allQuestions 数组结束')
        return sentence_pairs
    
    # 提取数组内容
    array_content = content[start_idx:end_idx+2]
    
    # 解析每个问题对象
    import re
    # 匹配问题对象
    question_pattern = re.compile(r'\{[^}]*sentence: "([^"]*)"[^}]*correctAnswer: "([^"]*)"[^}]*\}', re.DOTALL)
    matches = question_pattern.findall(array_content)
    
    for match in matches:
        sentence = match[0]
        correct_answer = match[1]
        # 生成完整的句子
        full_sentence = sentence.replace('______', correct_answer)
        sentence_pairs.append((full_sentence, sentence))
    
    # 去重（基于完整句子）
    seen = set()
    unique_pairs = []
    for full_sentence, original_sentence in sentence_pairs:
        if full_sentence not in seen:
            seen.add(full_sentence)
            unique_pairs.append((full_sentence, original_sentence))
    
    return unique_pairs

# 生成音频文件
async def generate_audio(sentence, output_path, index):
    try:
        print(f"正在生成第 {index} 个音频: {sentence}")
        # 使用 edge-tts 生成音频，语速设置为0.8（-20%）
        communicate = edge_tts.Communicate(
            sentence, 
            "en-US-AriaNeural",  # 美国英语女声
            rate="-20%"  # 语速为0.8倍
        )
        await communicate.save(output_path)
        # 检查文件大小
        import os
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"成功生成音频: {output_path}, 大小: {file_size} bytes")
            return True
        else:
            print(f"生成音频失败: 文件未创建 {output_path}")
            return False
    except Exception as e:
        print(f"生成音频失败 {sentence}: {e}")
        return False

async def main():
    # 提取句子
    sentence_pairs = extract_sentences()
    print(f"提取到 {len(sentence_pairs)} 个句子")
    
    # 创建目录
    output_dir = 'voice/game_verb'
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成音频文件和映射
    audio_mapping = {}
    tasks = []
    
    for i, (full_sentence, original_sentence) in enumerate(sentence_pairs):
        output_path = os.path.join(output_dir, f'sentence_{i}.mp3')
        # 映射使用完整句子（包含正确答案）
        audio_mapping[full_sentence] = f'voice/game_verb/sentence_{i}.mp3'
        tasks.append(generate_audio(full_sentence, output_path, i))
    
    # 并行生成音频
    results = await asyncio.gather(*tasks)
    
    # 统计成功和失败的数量
    success_count = sum(results)
    print(f"成功生成 {success_count} 个音频文件，失败 {len(results) - success_count} 个")
    
    # 保存映射到 JSON 文件
    mapping_path = os.path.join(output_dir, 'mapping.json')
    try:
        with open(mapping_path, 'w', encoding='utf-8') as f:
            json.dump(audio_mapping, f, ensure_ascii=False, indent=2)
        print(f"音频映射已保存到 {mapping_path}")
        print(f"映射内容示例: {list(audio_mapping.items())[:3]}")
    except Exception as e:
        print(f"保存映射文件失败: {e}")

if __name__ == "__main__":
    asyncio.run(main())