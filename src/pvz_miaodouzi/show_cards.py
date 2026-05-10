from pvz_miaodouzi import CardInfo, ZOMBIES, PLANTS


def display_cards(cards: list[CardInfo], is_zombie: bool = False):
    for card in sorted(cards, key=lambda c: c.rarity if not is_zombie else ()):
        print(
            f"[{card.rarity.name if not is_zombie else '僵尸卡'}] {card.namea} ID: {card.plant_id}, 费用：{card.cost}, {f'CD: {card.cool_down:.1f}'.removesuffix('.0')}s"
        )
        print(card.jieshao)


def main():
    display_cards(PLANTS)
    print("-----")
    display_cards(ZOMBIES, is_zombie=True)


if __name__ == "__main__":
    main()
