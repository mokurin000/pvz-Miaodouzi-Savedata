import os
import sys
from pathlib import Path

from pvz_miaodouzi.edit_save import edit_savedata, main


def bundle_main():
    if sys.platform == "win32":
        appdata = Path(os.getenv("AppData")).parent or Path(
            os.getenv("UserProfile") / "AppData",
        )

        savedata = Path(appdata) / "LocalLow" / "MiaoDouzi" / "抽卡版PVZ"
        if savedata.exists():
            edit_savedata(savedata)
            return

    main()


if __name__ == "__main__":
    bundle_main()
