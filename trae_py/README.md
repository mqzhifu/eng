# 少儿英文学习

一个面向少儿的英语语法学习 Web 应用，通过小游戏的方式让学习英语变得简单有趣。

## 功能模块

### 主页功能
- **字典汇总** - 查看完整的英语语法词典，包含所有知识点和详细解释
- **小游戏** - 通过有趣的小游戏巩固学习，边玩边学更轻松
- **我的** - 个人中心，查看打卡记录和学习进度

### 游戏列表

| 游戏 | 文件 | 说明 | 难度 |
|------|------|------|------|
| 人称代词填空 | game_rencheng.html | 练习 I/You/He/She/It/We/They 的用法 | 简单 |
| 反义词连连看 | game_antonyms.html | 找出成对的反义词，锻炼记忆力 | 简单 |
| 疑问句翻译 | game_translate.html | 将英语疑问句翻译成中文，练习特殊疑问句 | 中等 |
| 系动词填空 | game_verb.html | 选择正确的系动词(am/is/are/was/were)填空 | 简单 |
| 近似词多选 | game_synonyms.html | 选择所有与中文意思匹配的近似词 | 中等 |
| 单词排序 | game_sort.html | 点击单词，将它们拖放到正确的位置，完成句子 | 简单 |
| 翻版记忆短语 | game_memory.html | 翻开卡片，找到英文和中文对应的短语 | 中等 |
| 英语问答 | game_qa.html | 回答英语问题，选择正确答案 | 简单 |
| 动物词汇 | game_animal.html | 学习动物相关词汇 | 简单 |
| 家庭成员 | game_family.html | 学习家庭成员相关词汇 | 简单 |

## 项目结构

```
├── index.html              # 主页
├── game_index.html         # 游戏列表页
├── dict.html               # 字典汇总页
├── my.html                 # 个人中心
├── game_*.html             # 各游戏页面
├── css/
│   └── style.css           # 样式文件
├── js/
│   ├── common.js           # 公共配置
│   └── responsivevoice.js  # 语音库
├── data/
│   ├── game_qa.json        # 问答数据
│   ├── game_animal.json    # 动物词汇数据
│   ├── game_antonyms.json  # 反义词数据
│   ├── game_family.json    # 家庭成员数据
│   ├── game_memory.json    # 记忆游戏数据
│   ├── game_rencheng.json  # 人称代词数据
│   ├── game_sort.json      # 排序游戏数据
│   ├── game_synonyms.json  # 近似词数据
│   ├── game_translate.json # 翻译游戏数据
│   └── game_verb.json      # 系动词数据
├── voice/                  # TTS 生成的音频文件
│   ├── game_animal/
│   ├── game_antonyms/
│   ├── game_family/
│   ├── game_memory/
│   ├── game_qa/
│   ├── game_rencheng/
│   ├── game_sort/
│   ├── game_synonyms/
│   ├── game_translate/
│   └── game_verb/
├── image/                  # 图片资源
└── py/
    └── app.py              # Flask 后端服务
```

## 技术栈

- **前端**: HTML5, CSS3, JavaScript
- **后端**: Python Flask
- **语音合成**: edge-tts (微软 Edge 语音合成)
- **数据存储**: JSON 文件

## 快速开始

### 环境要求

- Python 3.8+
- Flask
- edge-tts

### 安装依赖

```bash
pip install flask edge-tts
```

### 启动服务

```bash
cd py
python app.py
```

服务将在 `http://localhost:8090` 启动。

### 访问应用

打开浏览器访问: http://localhost:8090

## API 接口

### 获取游戏数据

```
GET /api/game/<game_name>
```

返回指定游戏的 JSON 数据。

### 文字转语音

```
GET /api/tts?text=<text>&game=<game_name>
```

参数:
- `text`: 要转换的文本
- `game`: 游戏名称（用于缓存目录）

返回: MP3 音频文件

## 特色功能

- 语音朗读 - 使用微软 Edge TTS 提供自然流畅的英语发音
- 音频缓存 - 自动缓存生成的音频，提升响应速度
- 响应式设计 - 适配各种屏幕尺寸
- 打卡记录 - 记录学习进度

## 许可证

MIT License
