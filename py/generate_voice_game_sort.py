import os
import json
import asyncio
from edge_tts import Communicate

# 提取 game_sort.html 中的句子
def extract_sentences():
    sentences = [
        "I love my family",
        "The cat is black",
        "We go to school",
        "She has a book",
        "He can play football",
        "They are happy",
        "The sun is shining",
        "I eat apples",
        "We drink water",
        "She likes dogs",
        "He reads a story",
        "The bird can fly",
        "I have a pen",
        "We watch TV",
        "She sings a song",
        "He runs fast",
        "They play games",
        "The flower is red",
        "I brush my teeth",
        "We learn English",
        "She dances well",
        "He draws a picture",
        "The dog barks loudly",
        "I wear a coat",
        "We go to the park",
        "She writes a letter",
        "He jumps high",
        "They eat lunch",
        "The moon is bright",
        "I listen to music",
        "We clean the room",
        "She cooks dinner",
        "He rides a bike",
        "They go swimming",
        "The tree is tall",
        "I wash my hands",
        "We play basketball",
        "She studies hard",
        "He watches a movie",
        "They go to bed",
        "The sky is blue",
        "I help my mom",
        "We plant flowers",
        "She plays the piano",
        "He does his homework",
        "They go to the zoo",
        "The snow is white",
        "I take a shower",
        "We go shopping",
        "She feeds the cat",
        "He plays computer games",
        "They go hiking",
        "The wind is blowing",
        "I read a book",
        "We play soccer",
        "She waters the plants",
        "He goes to work",
        "They have a picnic",
        "The rain is falling",
        "I make a cake",
        "We go to the beach",
        "She paints a picture",
        "He goes fishing",
        "They play baseball",
        "The fire is hot",
        "I take a walk",
        "We go to the museum",
        "She sews a dress",
        "He fixes the bike",
        "They go to the library",
        "The ice is cold",
        "I play with my friends",
        "We go to the cinema",
        "She takes a photo",
        "He climbs a mountain",
        "They go to the concert",
        "The grass is green",
        "I do exercise",
        "We go to the supermarket",
        "She dances ballet",
        "He plays the guitar",
        "They go to the aquarium",
        "The sand is soft",
        "I write a story",
        "We go to the amusement park",
        "She plays the violin",
        "He goes skiing",
        "They go to the botanical garden",
        "The rock is hard",
        "I play chess",
        "We go to the planetarium",
        "She plays the flute",
        "He goes camping",
        "They go to the art gallery"
    ]
    return sentences

# 生成音频文件
async def generate_audio(sentences):
    # 创建输出目录
    output_dir = "../voice/game_sort"
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成音频文件和映射
    mapping = {}
    
    for i, sentence in enumerate(sentences):
        # 生成音频文件
        output_file = os.path.join(output_dir, f"sentence_{i}.mp3")
        
        # 生成音频
        communicate = Communicate(sentence, "en-US-AriaNeural", rate="-20%")
        with open(output_file, "wb") as f:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
        
        # 添加到映射
        mapping[sentence] = f"voice/game_sort/sentence_{i}.mp3"
        
        print(f"Generated audio for: {sentence}")
    
    # 保存映射文件
    mapping_file = os.path.join(output_dir, "mapping.json")
    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {len(sentences)} audio files")
    print(f"Mapping file saved to: {mapping_file}")

if __name__ == "__main__":
    sentences = extract_sentences()
    asyncio.run(generate_audio(sentences))
