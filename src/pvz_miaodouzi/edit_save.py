import errno
from pathlib import Path
from sys import argv

import pypinyin
import questionary
from questionary import Choice

from pvz_miaodouzi import PLANTS, Rarity, load_save, write_save


def pinyin_match(filter_text: str, choice: Choice):
    title = choice.title.lower()

    pinyin = pypinyin.lazy_pinyin(title)

    return filter_text.lower() in "".join(pinyin) or \
        filter_text.lower() in "".join(p[0] for p in pinyin)


def handle_file_error(e: OSError, operation: str) -> None:
    """统一的文件错误处理 helper"""
    match e.errno:
        case errno.ENOENT | errno.ENOTDIR:
            print(f"无法{operation}存档：文件或路径不存在")
        case errno.EPERM | errno.EACCES:
            print(f"无法{operation}存档：权限不足")
        case errno.ENOSPC:
            print(f"无法{operation}存档：磁盘空间不足")
        case errno.EISDIR:
            print(f"无法{operation}存档：目标是目录而非文件")
        case _:
            print(f"无法{operation}存档：未知错误：{e}")


def main():
    if len(argv) > 1:
        path = Path(argv[1])
    else:
        print("用法: edit-savedata save.json")
        return

    instruction_ctrl = "\n空格开关, ↑↓移动, Ctrl-I反选, Ctrl-A全选"
    instruction = instruction_ctrl.replace("Ctrl-", "")

    # ==================== 模式选择 ====================
    mode = questionary.select(
        "请选择编辑模式：",
        choices=[
            questionary.Choice("按卡牌（可单独开启/关闭每张卡）", value="card"),
            questionary.Choice("按卡组（按稀有度批量开启）", value="set"),
        ],
        instruction="\n"
        "· 卡组模式会【清空】当前已持有的卡牌，只保留本次选择的稀有度卡牌\n"
        "· 卡牌模式会保留当前存档中的卡牌，你可以按需增删",
    ).ask()

    if not mode:
        print("未选择模式，退出")
        return

    # ==================== 读取存档 ====================
    try:
        save_data = load_save(path)
    except OSError as e:
        handle_file_error(e, "加载")
        return
    except Exception as e:
        print(f"未知错误：{e}")
        return

    current_scores = set(save_data.get("scores", []))

    # ==================== 卡组模式 ===================
    if mode == "set":
        rarity_choices = [
            questionary.Choice(title=member.name, value=member) for member in Rarity
        ]

        selected_rarities = questionary.checkbox(
            "选择要开启的卡牌稀有度：",
            choices=rarity_choices,
            instruction=instruction,
        ).ask()

        if not selected_rarities:
            print("未选择任何稀有度，退出")
            return

        selected_set = set(selected_rarities)
        plant_ids = [card.plant_id for card in PLANTS if card.rarity in selected_set]

        save_data["scores"] = plant_ids
        print(f"已选择 {len(plant_ids)} 个 plantId")

    # ==================== 卡牌模式 ====================
    else:  # mode == "card"
        # 构建卡牌选择列表
        choices = []
        for card in sorted(PLANTS, key=lambda c: (c.rarity, c.plant_id)):
            checked = card.plant_id in current_scores

            title = f"[{card.plant_id:03}-{card.rarity.name}] {card.namea} - 阳光:{card.cost}"
            if card.is_mogu:
                title += " [夜间]"

            choices.append(
                questionary.Choice(
                    title=title,
                    value=card.plant_id,
                    checked=checked,
                )
            )

        selected_ids = questionary.checkbox(
            "选择要持有的卡牌：",
            choices=choices,
            instruction=f"{instruction_ctrl}\n输入阳光, ID或拼音搜索",
            use_search_filter=True,
            search_filter_fn=pinyin_match,
            use_jk_keys=False,
        ).ask()

        if selected_ids is None:  # 用户取消
            return

        save_data["scores"] = selected_ids
        print(f"已选择 {len(selected_ids)} 个 plantId")

    # ==================== 写入存档 ====================
    try:
        write_save(path, save_data)
        print(f"存档写入成功！路径：{path}")
    except OSError as e:
        handle_file_error(e, "写出")
    except Exception as e:
        print(f"未知错误：{e}")


if __name__ == "__main__":
    main()
