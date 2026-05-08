import json
from pathlib import Path
from hashlib import md5
from _hashlib import HASH
from sys import argv

import questionary

from pvz_miaodouzi import PLANTS, Rarity


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


def main():
    if len(argv) > 1:
        path = Path(argv[1])
    else:
        print("用法: edit-savedata save.json")
        return

    rarity_choices = [
        questionary.Choice(title=member.name, value=member) for member in Rarity
    ]

    selected_rarities = questionary.checkbox(
        "选择要开启的卡牌稀有度：", choices=rarity_choices
    ).ask()

    if not selected_rarities:
        print("未选择任何稀有度，退出")
        return

    selected_set = set(selected_rarities)

    plant_ids = [card.plantId for card in PLANTS if card.xiyoudu in selected_set]

    save_data = load_save(path)
    save_data["scores"] = plant_ids

    write_save(path, save_data)

    print(f"已写入 {len(plant_ids)} 个 plantId 到 save.json")


if __name__ == "__main__":
    main()
