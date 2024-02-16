<!--
 Copyright (C) 2024 OriginalFactor
 
 This file is part of TelegramGPTBot.
 
 TelegramGPTBot is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 TelegramGPTBot is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with TelegramGPTBot.  If not, see <http://www.gnu.org/licenses/>.
-->

# Telegram GPT Bot
使用python构建的TG机器人，接入OpenAI API。

## 依赖
- Python 3
- python-telegram-bot（pip package）
- pymongo（可选）（pip package）

## 一键setup（推荐）
参见[官网](https://git-scm.com/)，安装Git；
参见[官方教程](https://asdf-vm.com/guide/getting-started.html)
安装asdf后，参见[asdf-python Github页面](https://github.com/asdf-community/asdf-python)安装asdf-python插件；
安装`3.11.7`版本的python；
安装`pipenv`,参考[官方GitHub页面](https://github.com/pypa/pipenv?tab=readme-ov-file#installation)。
运行下面这段命令进入环境：
```sh
pipenv install
pipenv shell
```

## 运行
```sh
python3 ./main.py
```

## 配置

### 配置规范
```json
{
    "gpt-key": "OpenAI API Key，含Bearer", // 必填
    "gpt-url": "OpenAI API地址，默认为https://api.openai.com/", // 可选
    "tg-token": "Telegram机器人Token", // 必填
    "gpt-custom": {
        // 这里填gpt的参数，具体参考OpenAI API文档
    }, // 可选
    "system-prompt": "系统提示词", // 必填
    "enable-history": false, // 是否记录上下文，用`/cleanHistory [chatid]`命令清除
                             // 无参数清除当前聊天，可选，默认false
    "database": "数据库名称，若使用SQLite则文件名", // 可选
    "dbEngine": "sqlite3/mongodb", // 若启用`enable-history`则必填
    "mongo-host": "MongoDB的链接字符串，格式`mongodb://[用户名]:[密码]@<ip>:[端口]`，默认mongodb://127.0.0.1:27017" //可选
}
```

### 示例配置
```json
{
    "gpt-key": "Bearer XXXXX",
    "tg-token": "01234567:XXXXXXXX",
    "gpt-custom": {
        "temprature": 0.7,
        "max_tokens": 512
    },
    "system-prompt": "你是在你们公司推出的万能服务项目工作的一名服务员，你的目标是完美的解决用户提出的要求或问题。"
}
```