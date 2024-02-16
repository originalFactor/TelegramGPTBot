import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler,\
    InlineQueryHandler
from httpx import post
from json import dumps, loads
from random import choices
from string import ascii_letters
from argparse import ArgumentParser
from sys import exit as sexit
from typing import Union

# 获取命令行参数
argparser = ArgumentParser(
    "Telegram ChatGPT 群管机器人"
)
argparser.add_argument('-c','--config',default='./config.json',help="配置文件")
argparser.add_argument('-?',action='help')
args = argparser.parse_args()

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - [%(levelname)s] %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("telegramGPTBot")

# 获取数据
try:
    with open(args.config) as f:
        config = loads(f.read())
except Exception as e:
    logger.fatal(f"初始化失败: {e}")
    sexit()
    
# 数据库引擎
if config.get("enable-history"):
    if config.get('dbEngine')=='sqlite3':
        from dbengine.sqlite.database import Database
        from dbengine.sqlite.table import Table
    elif config.get('dbEngine')=='mongodb':
        from dbengine.mongo.database import Database
        from dbengine.mongo.table import Table

# 随机生成id
async def randCode(k:int=8)->str:
    return ''.join(choices(ascii_letters+'0123456789',k=k))

# 初始化数据库
if config.get('enable-history'):
    db = Database(
        config.get('database','tgGPTbotdb'),
        config.get('mongo-host','mongodb://127.0.0.1:27017')
    )

# 用于处理/start命令的函数
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "您好！我是ChatGPT，很高兴为您提供帮助。"
    )

# 处理私聊和群聊
async def handle_message(update: Update, context:ContextTypes.DEFAULT_TYPE):
    flag = True
    if update.message.chat.type!='private': flag = False
    for entity in update.message.entities:
        if entity.type=='mention':
            if entity.user:
                if entity.user.username==context.bot.username:
                    flag = True
    if context.bot.username in update.message.text: flag = True
    if not flag: return
    reply = await chatgpt_reply(update.message.text,'chat'+str(update.effective_chat.id))
    await update.message.reply_text(
        f'{reply[0]}\r\n\t本次共使用{reply[1]}token'
    )

# 处理inline-mode，目前有问题
async def handle_inline_message(update:Update, context:ContextTypes.DEFAULT_TYPE):
    if not update.inline_query.query: return
    reply = await chatgpt_reply(update.inline_query.query)
    await context.bot.answer_inline_query(
        update.inline_query.id,
        [
            InlineQueryResultArticle(
                randCode(),
                "ChatGPT Answer",
                InputTextMessageContent(
                    f"{reply[0]}\n本次使用了{reply[1]}个Token"
                )
            )
        ]
    )

# 获取回复
async def chatgpt_reply(message:str,chatId:str='')->tuple[str,int]:
    response = await chatGPT_request(
        message,
        chatId=chatId,
        **config.get('gpt-custom',{})
    )
    await add_message(
        response["choices"][0]["message"]["content"],
        chatId,
        response['choices'][0]['message']['role']
    )
    return (response["choices"][0]["message"]["content"].strip(),response["usage"]["total_tokens"])

# 增加消息
async def add_message(message:str,chatId:str,role:str='user'):
    if config.get('enable-history'):
        await (await db.get(
            str(chatId),
            {
                "id": ("INTEGER","PRIMARY KEY","NOT NULL"),
                "role": ("TEXT","NOT NULL"),
                "content": ("TEXT","NOT NULL")
            }
        )).new({
            "role": role,
            "content": message
        })

# 获取消息
async def get_messages(message:str,chatId:str='')->list[dict[str,str]]:
    messages = []
    if config.get('enable-history') and chatId:
        messages = await (await db.get(
            chatId,
            {
                "id": ("INTEGER","PRIMARY KEY","NOT NULL"),
                "role": ("TEXT","NOT NULL"),
                "content": ("TEXT","NOT NULL")
            },
        )).get({},('role','content'))
        await add_message(message,chatId)
    return list([
        {
            "role": "system",
            "content": config.get('system-prompt','')
        }
    ] + [
        {
            "role": list(_)[1],
            "content": list(_)[2]
        }
        for _ in messages
    ] + [
        {
            "role": 'user',
            "content": message
        }
    ])

# GPT底层
async def chatGPT_request(
    prompt:str,
    model:str='gpt-3.5-turbo',
    chatId:str='',
    **kwargs
)->dict[str,str,int,list[dict[int,dict[str,str],str]],dict[int,int,int]]:
    api_data = {
        "model": model,
        "messages": await get_messages(prompt,chatId)
    }
    for key in kwargs.keys():
        api_data[key] = kwargs[key]
    json_data = dumps(api_data).encode()
    logger.info(json_data)
    response = post(
        url=config.get('gpt-url','https://api.openai.com/')+'v1/chat/completions',
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": config.get('gpt-key',''),
        },
        data=json_data,
        timeout=10000
    )
    logger.info(response.text)
    return response.json()

# 未知命令处理
async def unknown(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sorry, I didn't understand that command.")

# 清除聊天记录
async def clean_history(update:Update, context:ContextTypes.DEFAULT_TYPE):
    if context.args:
        await db.remove('chat'+context.args[0])
        await update.message.reply_text(
            f"Successfully cleaned message histories in chatid {context.args[0]}."
        )
    else:
        if await db.exists('chat'+str(update.effective_chat.id)):
            await (await db.get('chat'+str(update.effective_chat.id))).remove({})
            await update.message.reply_text(
                f"Successfully cleaned message histories in current chatid {update.effective_chat.id}."
            )
        else:
            await update.message.reply_text(
                f"No exist message history in current chatid {update.effective_chat.id}."
            )

# 主程序
if __name__ == "__main__":
    application = ApplicationBuilder().token(config.get('tg-token','')).build()
    application.add_handlers([
        CommandHandler(
            'start',
            start
        ),
        CommandHandler(
            'cleanHistory',
            clean_history
        ),
        MessageHandler(
            filters.TEXT&\
                (~filters.COMMAND),
            handle_message
        ),
        MessageHandler(
            filters.COMMAND,
            unknown
        )
    ])
    application.add_handler(InlineQueryHandler(handle_inline_message),255)
    application.run_polling()
