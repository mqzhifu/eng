import os
import re
import json
import asyncio
from edge_tts import Communicate

async def generate_audio():
    # 读取HTML文件
    with open('../game_animal.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取动物名称
    animal_pattern = r'answer:\s*"([^"]+)"'
    animals = re.findall(animal_pattern, content)

    # 调试信息
    print(f"Found {len(animals)} animals:")
    print(animals)

    # 去重
    unique_animals = list(set(animals))
    unique_animals.sort()

    # 调试信息
    print(f"Unique animals ({len(unique_animals)}):")
    print(unique_animals)

    # 创建输出目录
    output_dir = '../voice/game_animal'
    os.makedirs(output_dir, exist_ok=True)

    # 生成音频文件和映射
    mapping = {}

    for i, animal in enumerate(unique_animals):
        # 替换空格为下划线，用于文件名
        filename = f"{animal.replace(' ', '_')}.mp3"
        filepath = os.path.join(output_dir, filename)
        
        # 生成音频
        text = animal
        communicate = Communicate(text, "en-US-AriaNeural", rate="-20%")
        await communicate.save(filepath)
        
        # 添加到映射
        mapping[animal] = f"voice/game_animal/{filename}"
        
        print(f"Generated audio for: {animal}")

    # 保存映射
    with open(os.path.join(output_dir, 'mapping.json'), 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    print("\nAudio generation completed!")
    print(f"Generated {len(unique_animals)} audio files.")
    print(f"Mapping saved to: {os.path.join(output_dir, 'mapping.json')}")

if __name__ == "__main__":
    asyncio.run(generate_audio())