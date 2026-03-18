import os
import asyncio
from edge_tts import Communicate

# 要重新生成的单词和对应的文件
words_to_regenerate = [
    (2, "afraid"),
    (13, "big"),
    (50, "forest")
]

# 生成音频文件
async def regenerate_audio_files():
    # 目标目录
    output_dir = r'D:\code\test\voice\game_synonyms'
    if not os.path.exists(output_dir):
        print(f"创建目录: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)
    
    success_count = 0
    
    for index, word in words_to_regenerate:
        try:
            # 替换空格为下划线，用于文件名
            filename = f'word_{index}.mp3'
            filepath = os.path.join(output_dir, filename)
            
            # 生成音频
            print(f"开始生成: {word} -> {filename}")
            communicate = Communicate(word, "en-US-AriaNeural", rate="-20%")
            await communicate.save(filepath)
            
            # 检查文件是否生成成功
            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                print(f"生成音频成功: {word} -> {filename} (大小: {os.path.getsize(filepath)} 字节)")
                success_count += 1
            else:
                print(f"生成音频失败: {word} -> 文件为空或不存在")
                # 删除空文件
                if os.path.exists(filepath):
                    os.remove(filepath)
        except Exception as e:
            print(f"生成音频失败: {word} -> {e}")
    
    print(f"\n生成完成，共生成 {success_count} 个音频文件")

if __name__ == "__main__":
    print("重新生成失败的音频文件...")
    asyncio.run(regenerate_audio_files())
