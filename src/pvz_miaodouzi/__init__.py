import json
from enum import IntEnum
from pathlib import Path
from hashlib import md5
from _hashlib import HASH

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
    PLANTS: list[CardInfo] = [CardInfo.model_validate(item) for item in json.load(f)]

with (DATA_PATH / "Zombies.json").open("r", encoding="utf-8") as f:
    ZOMBIES: list[CardInfo] = [CardInfo.model_validate(item) for item in json.load(f)]


def load_save(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_save(path: Path, data: dict):
    def hash_digest(h: HASH) -> HASH:
        return md5(h.digest())

    json_bytes = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode(
        "utf-8"
    )
    with path.open("wb") as f:
        f.write(json_bytes)

    h = md5(json_bytes)
    save_3md5 = hash_digest(hash_digest(h)).hexdigest()

    with path.with_suffix(".json.md5").open("w", encoding="utf-8") as f:
        f.write(save_3md5)
