import os

from notifiers import get_notifier
from dotenv import load_dotenv


load_dotenv()


def notification(message: str):
    telegram = get_notifier("telegram")
    telegram.notify(
        token=os.getenv("token"),
        chat_id=os.getenv("chatId"),
        message=message,
    )
