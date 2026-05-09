import json
from pathlib import Path
from hashlib import md5
from _hashlib import HASH

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from pvz_miaodouzi.rarity import Rarity, RARITY_BY_ID


class CardInfo(BaseModel):
    model_config = ConfigDict(
        validate_by_alias=True,
        alias_generator=to_camel,
    )

    namea: str
    """卡牌名称"""

    jieshao: str
    """卡牌简介"""

    cost: int
    """阳光花费"""

    cool_down: float
    """冷却时间（秒）"""

    is_mogu: bool
    """是否为夜间作物"""

    plant_id: int
    """卡组内 ID，植物与僵尸分别为一组"""

    xiyoudu_: Rarity = Field(validation_alias="xiyoudu")

    @property
    def rarity(self) -> Rarity:
        """稀有度"""
        return RARITY_BY_ID.get(self.plant_id, self.xiyoudu_)


DATA_PATH = Path(__file__).parent / "data"


with (DATA_PATH / "Plants.json").open("r", encoding="utf-8") as f:
    PLANTS: list[CardInfo] = [CardInfo.model_validate(item) for item in json.load(f)]

with (DATA_PATH / "Zombies.json").open("r", encoding="utf-8") as f:
    ZOMBIES: list[CardInfo] = [CardInfo.model_validate(item) for item in json.load(f)]


def load_save(path: Path) -> dict:
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
