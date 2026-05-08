import os
import json
from collections import defaultdict


def main():
    props = defaultdict(dict)

    for file in os.listdir("."):
        if not file.endswith(".json"):
            continue

        with open(file, "r", encoding="utf-8") as f:
            data: dict = json.load(f)

        if not file.startswith("Cardproperties") and not file.startswith("CardClick"):
            continue

        path_id = data["m_GameObject"]["m_PathID"]

        for useless in [
            "m_GameObject",
            "m_Enabled",
            "m_Name",
            "m_Script",
            "isPlantIns",
            "plant",
            "copyCard",
            "lastPos",
            "data3",
            "cardState",
            "xuankage",
            "xuankage2",
            "normal",
            "normal2",
            "normal3",
            "nowcoolDown",
            "xifenID",
            "linshiID",
            "linshiSpeed",
            "isLinshi",
            "thisClick",
            "findThis",
            "liveTime",
            "trueLiveTime",
        ]:
            if useless in data:
                data.pop(useless)
        props[path_id] |= data

    objects = sorted(
        props.values(),
        key=lambda d: d["plantId"],
    )

    plants = []
    zombies = []
    for obj in objects:
        is_zombie = obj["zuobi"]["m_FileID"] != 0
        obj.pop("zuobi")

        if is_zombie:
            zombies.append(obj)
        else:
            plants.append(obj)

    with open("Plants.json", "w", encoding="utf-8") as f:
        json.dump(plants, f, indent=4, ensure_ascii=False)
    with open("Zombies.json", "w", encoding="utf-8") as f:
        json.dump(zombies, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
