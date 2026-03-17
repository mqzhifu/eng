import os
import json
import asyncio
from edge_tts import Communicate

# 提取 game_memory.html 中的短语
def extract_phrases():
    phrases = [
        "get up",
        "get on",
        "get off",
        "get in",
        "get to",
        "get ready for",
        "get back",
        "get dressed",
        "come on",
        "come in",
        "come out",
        "come back",
        "come from",
        "come true",
        "come over",
        "come up",
        "take off",
        "take out",
        "take away",
        "take back",
        "take care",
        "take a walk",
        "take a rest",
        "take a look",
        "put on",
        "put off",
        "put up",
        "put down",
        "put away",
        "put out",
        "put back",
        "put into",
        "turn on",
        "turn off",
        "turn up",
        "turn down",
        "turn left",
        "turn right",
        "turn around",
        "turn into"
    ]
    return phrases

# 生成音频文件
async def generate_audio(phrases):
    # 创建输出目录
    output_dir = "../voice/game_memory"
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成音频文件和映射
    mapping = {}
    
    for i, phrase in enumerate(phrases):
        # 生成音频文件
        output_file = os.path.join(output_dir, f"sentence_{i}.mp3")
        
        # 生成音频
        communicate = Communicate(phrase, "en-US-AriaNeural", rate="-20%")
        with open(output_file, "wb") as f:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
        
        # 添加到映射
        mapping[phrase] = f"voice/game_memory/sentence_{i}.mp3"
        
        print(f"Generated audio for: {phrase}")
    
    # 保存映射文件
    mapping_file = os.path.join(output_dir, "mapping.json")
    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {len(phrases)} audio files")
    print(f"Mapping file saved to: {mapping_file}")

if __name__ == "__main__":
    phrases = extract_phrases()
    asyncio.run(generate_audio(phrases))
