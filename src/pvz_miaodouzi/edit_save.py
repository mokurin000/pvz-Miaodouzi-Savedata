import errno
from pathlib import Path
from sys import argv

import questionary

from pvz_miaodouzi import PLANTS, Rarity, load_save, write_save


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

    # 稀有度选择
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

    # ==================== 读取存档 ====================
    try:
        save_data = load_save(path)
    except OSError as e:
        handle_file_error(e, "加载")
        return
    except Exception as e:
        print(f"未知错误：{e}")
        return

    # ==================== 写入存档 ====================
    save_data["scores"] = plant_ids

    try:
        write_save(path, save_data)
    except OSError as e:
        handle_file_error(e, "写出")
        return
    except Exception as e:
        print(f"未知错误：{e}")
        return

    print(f"已成功写入 {len(plant_ids)} 个 plantId 到存档文件")


if __name__ == "__main__":
    main()
