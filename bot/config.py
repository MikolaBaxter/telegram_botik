import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def parse_int_list(value: str) -> list[int]:
    return [int(x.strip()) for x in value.split(",") if x.strip()]


@dataclass
class Config:
    bot_token: str
    bot_name: str
    chat_url: str
    support_url: str
    admin_ids: list[int]


def load_config() -> Config:
    admin_ids = parse_int_list(os.getenv("ADMIN_IDS", ""))
    # Для совместимости со старым .env можно временно использовать CURATOR_IDS.
    if not admin_ids:
        admin_ids = parse_int_list(os.getenv("CURATOR_IDS", ""))

    cfg = Config(
        bot_token=os.getenv("BOT_TOKEN", ""),
        bot_name=os.getenv("BOT_NAME", "Наш проект"),
        chat_url=os.getenv("CHAT_URL", ""),
        support_url=os.getenv("SUPPORT_URL", ""),
        admin_ids=admin_ids,
    )

    if not cfg.bot_token:
        raise ValueError("BOT_TOKEN не указан в .env")
    if not cfg.admin_ids:
        raise ValueError("ADMIN_IDS не указан или пустой в .env")
    return cfg


config = load_config()
