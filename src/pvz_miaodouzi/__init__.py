import json
from enum import IntEnum
from pathlib import Path

from pydantic import BaseModel


class Rarity(IntEnum):
    劣质卡 = 0
    普通卡 = 1
    稀有卡 = 2
    史诗卡 = 3
    传奇卡 = 4
    炼狱卡 = 5


class CardInfo(BaseModel):
    namea: str
    """卡牌名称"""

    jieshao: str
    """卡牌简介"""

    cost: int
    """阳光花费"""

    coolDown: float
    """冷却时间（秒）"""

    isMogu: bool
    """是否为夜间作物"""

    xiyoudu: Rarity
    """稀有度"""

    plantId: int
    """卡组内 ID，植物与僵尸分别为一组"""


DATA_PATH = Path(__file__).parent / "data"


with (DATA_PATH / "Plants.json").open("r", encoding="utf-8") as f:
    raw_data = json.load(f)

with (DATA_PATH / "Zombies.json").open("r", encoding="utf-8") as f:
    raw_data_zom = json.load(f)

PLANTS: list[CardInfo] = [CardInfo.model_validate(item) for item in raw_data]
ZOMBIES: list[CardInfo] = [CardInfo.model_validate(item) for item in raw_data_zom]
