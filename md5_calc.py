from hashlib import md5
from _hashlib import HASH


def hash_digest(h: HASH) -> HASH:
    return md5(h.digest())


def main():
    with open("save.json", "rb") as f:
        h = md5(f.read())
        save_3md5 = hash_digest(hash_digest(h)).hexdigest()

    with open("save.json.md5", "w", encoding="utf-8") as f:
        f.write(save_3md5)


if __name__ == "__main__":
    main()
