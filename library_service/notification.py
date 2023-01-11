import os

from notifiers import get_notifier


def notification(message: str):
    telegram = get_notifier("telegram")
    telegram.notify(
        # token=os.getenv("token"),
        token="5835285216:AAErzVIj-a3znQODfRO2_UsRJrOHPpBV_7E",
        # chat_id=os.getenv("chatId"),
        chat_id=358763586,
        message=message,
    )
