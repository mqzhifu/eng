import os
import json
import asyncio
import edge_tts

# 从 H5/game_rencheng.html 提取句子和正确答案
def extract_sentences():
    with open('H5/game_rencheng.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 allQuestions 数组中的句子和正确答案
    sentence_answer_pairs = []
    # 找到 allQuestions 开始和结束的位置
    start_idx = content.find('const allQuestions = [')
    if start_idx == -1:
        print('未找到 allQuestions 数组')
        return sentence_answer_pairs
    
    end_idx = content.find('];', start_idx)
    if end_idx == -1:
        print('未找到 allQuestions 数组结束')
        return sentence_answer_pairs
    
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
        # 只添加包含 ______ 的问题
        if '______' in sentence:
            sentence_answer_pairs.append((sentence, correct_answer))
    
    # 去重（基于句子）
    seen = set()
    unique_pairs = []
    for sentence, answer in sentence_answer_pairs:
        if sentence not in seen:
            seen.add(sentence)
            unique_pairs.append((sentence, answer))
    
    return unique_pairs

# 生成音频文件
async def generate_audio(sentence, correct_answer, output_path, index):
    try:
        # 将 ______ 占位符替换为正确答案
        processed_sentence = sentence.replace('______', correct_answer)
        print(f"正在生成第 {index} 个音频: {processed_sentence}")
        # 使用 edge-tts 生成音频，语速设置为0.8（-20%）
        communicate = edge_tts.Communicate(
            processed_sentence, 
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
    # 提取句子和正确答案
    sentence_answer_pairs = extract_sentences()
    print(f"提取到 {len(sentence_answer_pairs)} 个句子")
    
    # 创建目录
    output_dir = 'voice/game_rencheng'
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成音频文件和映射
    audio_mapping = {}
    tasks = []
    
    for i, (sentence, correct_answer) in enumerate(sentence_answer_pairs):
        output_path = os.path.join(output_dir, f'sentence_{i}.mp3')
        # 映射使用原始句子（包含 ______）
        audio_mapping[sentence] = f'voice/game_rencheng/sentence_{i}.mp3'
        tasks.append(generate_audio(sentence, correct_answer, output_path, i))
    
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