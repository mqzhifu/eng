import os
import json
import asyncio
from edge_tts import Communicate

# 提取的问题和答案数据
data_source = [
    # 1. 问候与自我介绍
    {"category": "问候与自我介绍", "question": "How are you today?", "correctAnswer": "I'm fine.", "chineseQuestion": "你今天好吗？", "chineseAnswer": "我很好。"},
    {"category": "问候与自我介绍", "question": "What's your name?", "correctAnswer": "My name is Tom.", "chineseQuestion": "你叫什么名字？", "chineseAnswer": "我叫汤姆。"},
    {"category": "问候与自我介绍", "question": "How old are you?", "correctAnswer": "I'm ten years old.", "chineseQuestion": "你几岁？", "chineseAnswer": "我十岁。"},
    {"category": "问候与自我介绍", "question": "Where are you from?", "correctAnswer": "I'm from China.", "chineseQuestion": "你来自哪里？", "chineseAnswer": "我来自中国。"},
    {"category": "问候与自我介绍", "question": "Nice to meet you.", "correctAnswer": "Nice to meet you, too.", "chineseQuestion": "很高兴见到你。", "chineseAnswer": "我也是。"},
    {"category": "问候与自我介绍", "question": "How do you do?", "correctAnswer": "How do you do?", "chineseQuestion": "你好。", "chineseAnswer": "你好。"},
    {"category": "问候与自我介绍", "question": "Where do you live?", "correctAnswer": "I live in China.", "chineseQuestion": "你住在哪里？", "chineseAnswer": "我住在中国。"},
    
    # 2. 学校与学习
    {"category": "学校与学习", "question": "What's your favorite subject?", "correctAnswer": "My favorite subject is English.", "chineseQuestion": "你最喜欢的科目是什么？", "chineseAnswer": "我最喜欢英语。"},
    {"category": "学校与学习", "question": "What's in your schoolbag?", "correctAnswer": "A book and a pencil.", "chineseQuestion": "书包里有什么？", "chineseAnswer": "书和铅笔。"},
    {"category": "学校与学习", "question": "Who is your teacher?", "correctAnswer": "Miss Li is my teacher.", "chineseQuestion": "你的老师是谁？", "chineseAnswer": "李老师。"},
    {"category": "学校与学习", "question": "What do you do in class?", "correctAnswer": "I read and write.", "chineseQuestion": "你在课上做什么？", "chineseAnswer": "我读书写字。"},
    {"category": "学校与学习", "question": "Do you like English?", "correctAnswer": "Yes, I do.", "chineseQuestion": "你喜欢英语吗？", "chineseAnswer": "喜欢。"},
    {"category": "学校与学习", "question": "Where is your classroom?", "correctAnswer": "It's over there.", "chineseQuestion": "教室在哪里？", "chineseAnswer": "在那边。"},
    {"category": "学校与学习", "question": "Is this your book?", "correctAnswer": "Yes, it is.", "chineseQuestion": "这是你的书吗？", "chineseAnswer": "是。"},
    {"category": "学校与学习", "question": "What color is your pen?", "correctAnswer": "It's blue.", "chineseQuestion": "你的笔是什么颜色？", "chineseAnswer": "蓝色。"},
    {"category": "学校与学习", "question": "Can you read it?", "correctAnswer": "Yes, I can.", "chineseQuestion": "你会读吗？", "chineseAnswer": "会。"},
    {"category": "学校与学习", "question": "What time do you go to school?", "correctAnswer": "At seven o'clock.", "chineseQuestion": "你几点上学？", "chineseAnswer": "七点。"},
    {"category": "学校与学习", "question": "How do you go to school?", "correctAnswer": "I go to school on foot.", "chineseQuestion": "你怎么去上学？", "chineseAnswer": "我步行去上学。"},
    
    # 3. 家庭
    {"category": "家庭", "question": "How many people are in your family?", "correctAnswer": "Four people.", "chineseQuestion": "你家有几口人？", "chineseAnswer": "四口人。"},
    {"category": "家庭", "question": "Do you have a sister/brother?", "correctAnswer": "Yes, I do.", "chineseQuestion": "你有姐妹 / 兄弟吗？", "chineseAnswer": "有。"},
    {"category": "家庭", "question": "What's your father's job?", "correctAnswer": "He is a doctor.", "chineseQuestion": "爸爸是做什么工作的？", "chineseAnswer": "他是医生。"},
    {"category": "家庭", "question": "Do you love your family?", "correctAnswer": "Yes, very much.", "chineseQuestion": "你爱你的家人吗？", "chineseAnswer": "非常爱。"},
    {"category": "家庭", "question": "Where is your home?", "correctAnswer": "My home is here.", "chineseQuestion": "你家在哪里？", "chineseAnswer": "我家在这里。"},
    {"category": "家庭", "question": "Is this your family photo?", "correctAnswer": "Yes, it is.", "chineseQuestion": "这是全家福吗？", "chineseAnswer": "是。"},
    
    # 4. 动物
    {"category": "动物", "question": "What's this?", "correctAnswer": "It's a dog.", "chineseQuestion": "这是什么？", "chineseAnswer": "这是一只狗。"},
    {"category": "动物", "question": "What's that?", "correctAnswer": "It's a cat.", "chineseQuestion": "那是什么？", "chineseAnswer": "那是一只猫。"},
    {"category": "动物", "question": "What does a dog say?", "correctAnswer": "Woof, woof.", "chineseQuestion": "狗怎么叫？", "chineseAnswer": "汪汪。"},
    {"category": "动物", "question": "Can a bird fly?", "correctAnswer": "Yes, it can.", "chineseQuestion": "鸟会飞吗？", "chineseAnswer": "会。"},
    {"category": "动物", "question": "Can a fish walk?", "correctAnswer": "No, it can't.", "chineseQuestion": "鱼会走路吗？", "chineseAnswer": "不会。"},
    {"category": "动物", "question": "Do you like pandas/cats?", "correctAnswer": "No, I don't.", "chineseQuestion": "你喜欢熊猫 / 猫吗？", "chineseAnswer": "不喜欢。"},
    {"category": "动物", "question": "What color is the panda?", "correctAnswer": "Black and white.", "chineseQuestion": "熊猫是什么颜色？", "chineseAnswer": "黑白相间。"},
    {"category": "动物", "question": "Where do monkeys live?", "correctAnswer": "In the tree.", "chineseQuestion": "猴子住在哪里？", "chineseAnswer": "在树上。"},
    {"category": "动物", "question": "How many legs does a dog have?", "correctAnswer": "Four legs.", "chineseQuestion": "狗有几条腿？", "chineseAnswer": "四条腿。"},
    
    # 5. 食物与水果
    {"category": "食物与水果", "question": "Do you like apples/rice?", "correctAnswer": "Yes, I do.", "chineseQuestion": "你喜欢苹果 / 米饭吗？", "chineseAnswer": "喜欢。"},
    {"category": "食物与水果", "question": "What's your favorite fruit?", "correctAnswer": "Bananas.", "chineseQuestion": "你最喜欢的水果是什么？", "chineseAnswer": "香蕉。"},
    {"category": "食物与水果", "question": "Are you hungry/thirsty?", "correctAnswer": "Yes, I am.", "chineseQuestion": "你饿 / 渴吗？", "chineseAnswer": "是的。"},
    {"category": "食物与水果", "question": "What do you want to eat/drink?", "correctAnswer": "I want bread and water.", "chineseQuestion": "你想吃 / 喝什么？", "chineseAnswer": "我想吃面包喝水。"},
    {"category": "食物与水果", "question": "Is this an orange?", "correctAnswer": "Yes, it is.", "chineseQuestion": "这是橙子吗？", "chineseAnswer": "是。"},
    {"category": "食物与水果", "question": "What color is a strawberry?", "correctAnswer": "Red.", "chineseQuestion": "草莓是什么颜色？", "chineseAnswer": "红色。"},
    
    # 6. 颜色
    {"category": "颜色", "question": "What color is it?", "correctAnswer": "It's red.", "chineseQuestion": "它是什么颜色？", "chineseAnswer": "红色。"},
    {"category": "颜色", "question": "What color is the sky?", "correctAnswer": "Blue.", "chineseQuestion": "天空是什么颜色？", "chineseAnswer": "蓝色。"},
    {"category": "颜色", "question": "What color is your bag?", "correctAnswer": "It's black.", "chineseQuestion": "你的包是什么颜色？", "chineseAnswer": "黑色。"},
    {"category": "颜色", "question": "What color are your eyes?", "correctAnswer": "Black.", "chineseQuestion": "你的眼睛是什么颜色？", "chineseAnswer": "黑色。"},
    {"category": "颜色", "question": "Do you like green/red?", "correctAnswer": "No, I don't.", "chineseQuestion": "你喜欢绿色 / 红色吗？", "chineseAnswer": "不喜欢。"},
    
    # 7. 数字与数学
    {"category": "数字与数学", "question": "What's two plus three?", "correctAnswer": "Five.", "chineseQuestion": "二加三等于几？", "chineseAnswer": "五。"},
    {"category": "数字与数学", "question": "How many hands do you have?", "correctAnswer": "Two.", "chineseQuestion": "你有几只手？", "chineseAnswer": "两只。"},
    {"category": "数字与数学", "question": "What's ten minus four?", "correctAnswer": "Six.", "chineseQuestion": "十减四等于几？", "chineseAnswer": "六。"},
    {"category": "数字与数学", "question": "How many legs do you have?", "correctAnswer": "Two.", "chineseQuestion": "你有几条腿？", "chineseAnswer": "两条。"},
    {"category": "数字与数学", "question": "How many seasons in a year?", "correctAnswer": "Four.", "chineseQuestion": "一年有几个季节？", "chineseAnswer": "四个。"},
    {"category": "数字与数学", "question": "How many months in a year?", "correctAnswer": "Twelve.", "chineseQuestion": "一年有几个月？", "chineseAnswer": "十二个。"},
    {"category": "数字与数学", "question": "How many minutes are there in an hour?", "correctAnswer": "Sixty.", "chineseQuestion": "一小时有多少分钟？", "chineseAnswer": "六十分钟。"},
    {"category": "数字与数学", "question": "How many seconds are there in a minute?", "correctAnswer": "Sixty.", "chineseQuestion": "一分钟有多少秒？", "chineseAnswer": "六十秒。"},
    {"category": "数字与数学", "question": "How many hours are there in a day?", "correctAnswer": "Twenty-four.", "chineseQuestion": "一天有多少个小时？", "chineseAnswer": "二十四个小时。"},
    
    # 8. 天气
    {"category": "天气", "question": "How's the weather today?", "correctAnswer": "It's sunny.", "chineseQuestion": "今天天气怎么样？", "chineseAnswer": "晴天。"},
    {"category": "天气", "question": "Is it rainy today?", "correctAnswer": "Yes, it is.", "chineseQuestion": "今天下雨吗？", "chineseAnswer": "下。"},
    {"category": "天气", "question": "Is it cold/hot today?", "correctAnswer": "Yes, it is.", "chineseQuestion": "今天冷 / 热吗？", "chineseAnswer": "是的。"},
    {"category": "天气", "question": "Do you like sunny/rainy days?", "correctAnswer": "Yes, I do.", "chineseQuestion": "你喜欢晴天 / 雨天吗？", "chineseAnswer": "喜欢。"},
    {"category": "天气", "question": "What weather do you like?", "correctAnswer": "I like sunny days.", "chineseQuestion": "你喜欢什么天气？", "chineseAnswer": "我喜欢晴天。"},
    {"category": "天气", "question": "Is it snowing?", "correctAnswer": "No, it isn't.", "chineseQuestion": "下雪吗？", "chineseAnswer": "不下。"},
    
    # 9. 时间
    {"category": "时间", "question": "What time is it?", "correctAnswer": "It's eight o'clock.", "chineseQuestion": "几点了？", "chineseAnswer": "八点。"},
    {"category": "时间", "question": "What day is it today?", "correctAnswer": "Monday.", "chineseQuestion": "今天星期几？", "chineseAnswer": "星期一。"},
    {"category": "时间", "question": "Is it Sunday today?", "correctAnswer": "Yes, it is.", "chineseQuestion": "今天是星期日吗？", "chineseAnswer": "是。"},
    {"category": "时间", "question": "What day is tomorrow?", "correctAnswer": "Tuesday.", "chineseQuestion": "明天星期几？", "chineseAnswer": "星期二。"},
    {"category": "时间", "question": "When do you get up?", "correctAnswer": "At six thirty.", "chineseQuestion": "你几点起床？", "chineseAnswer": "六点半。"},
    {"category": "时间", "question": "When do you eat breakfast?", "correctAnswer": "At seven.", "chineseQuestion": "你几点吃早饭？", "chineseAnswer": "七点。"},
    {"category": "时间", "question": "When do you go to bed?", "correctAnswer": "At nine.", "chineseQuestion": "你几点睡觉？", "chineseAnswer": "九点。"},
    {"category": "时间", "question": "Is it morning now?", "correctAnswer": "Yes, it is.", "chineseQuestion": "现在是早上吗？", "chineseAnswer": "是。"},
    {"category": "时间", "question": "Is it afternoon now?", "correctAnswer": "Yes, it is.", "chineseQuestion": "现在是下午吗？", "chineseAnswer": "是。"},
    {"category": "时间", "question": "How many days in a week?", "correctAnswer": "Seven.", "chineseQuestion": "一周有几天？", "chineseAnswer": "七天。"},
    
    # 10. 爱好与运动
    {"category": "爱好与运动", "question": "What do you like to do?", "correctAnswer": "I like to play.", "chineseQuestion": "你喜欢做什么？", "chineseAnswer": "我喜欢玩。"},
    {"category": "爱好与运动", "question": "Do you like drawing/singing?", "correctAnswer": "Yes, I do.", "chineseQuestion": "你喜欢画画 / 唱歌吗？", "chineseAnswer": "喜欢。"},
    {"category": "爱好与运动", "question": "Can you swim/dance?", "correctAnswer": "Yes, I can.", "chineseQuestion": "你会游泳 / 跳舞吗？", "chineseAnswer": "会。"},
    {"category": "爱好与运动", "question": "Do you like football/basketball?", "correctAnswer": "Yes, I do.", "chineseQuestion": "你喜欢足球 / 篮球吗？", "chineseAnswer": "喜欢。"},
    {"category": "爱好与运动", "question": "What's your hobby?", "correctAnswer": "I like reading.", "chineseQuestion": "你的爱好是什么？", "chineseAnswer": "我喜欢阅读。"},
    {"category": "爱好与运动", "question": "Do you like running?", "correctAnswer": "Yes, I do.", "chineseQuestion": "你喜欢跑步吗？", "chineseAnswer": "喜欢。"},
    {"category": "爱好与运动", "question": "What sport do you like?", "correctAnswer": "I like ping-pong.", "chineseQuestion": "你喜欢什么运动？", "chineseAnswer": "我喜欢乒乓球。"}
]

async def generate_audio(text, output_path, voice="en-US-AriaNeural", rate="-20%"):
    """生成音频文件"""
    try:
        communicate = Communicate(text, voice, rate=rate)
        with open(output_path, "wb") as f:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
        return True
    except Exception as e:
        print(f"生成音频失败: {text}, 错误: {e}")
        return False

async def main():
    # 创建输出目录
    output_dir = r"D:\code\test\voice\game_qa"
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成答案音频
    print("开始生成答案音频...")
    for i, item in enumerate(data_source):
        answer = item["correctAnswer"]
        output_path = os.path.join(output_dir, f"answer_{i}.mp3")
        print(f"生成答案: {answer}")
        success = await generate_audio(answer, output_path)
        if not success:
            print(f"生成失败: {answer}")
    
    print("\n答案音频生成完成！")

if __name__ == "__main__":
    asyncio.run(main())
