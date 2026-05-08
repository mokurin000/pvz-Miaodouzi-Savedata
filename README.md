# pvz-Miaodouzi-Savedata

> 起因是主播习惯性修改《抽卡版》的金币，毕竟看起来难刷又不影响抽卡 结果直接出现大大的“作弊者”标
>
> 于是机缘巧合之下用 CyberChef 猜出来了 hash 计算算法

《植物大战僵尸》抽卡版存档 md5 计算代码

## 用法

```bash
# 下载脚本本体
curl -sSLO https://github.com/mokurin000/pvz-Miaodouzi-Savedata/raw/refs/heads/main/md5_calc.py
# 计算正确的 MD5MD5MD5
python3 md5_calc.py
```

## 存档位置

- Windows: `%appdata%\..\LocalLow\MiaoDouzi\抽卡版PVZ`
- Android:
    - 单用户: `/storage/emulated/0/Android/com.MiaoDouzi.PVZ/files/`
    - 多用户: `/data/media/[USER]/Android/com.MiaoDouzi.PVZ/files/`
