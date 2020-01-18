class MyGifts:
    def __init__(self, gifts_of_mine, wish_count_list):
        self.__gifts_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list
        self.gifts = self.__parse()

    def __parse(self):
        gifts = []
        for gift in self.__gifts_of_mine:
            gifts.append(self.__matching(gift))

        return gifts

    def __matching(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
                break

        return {
            'wishes_count': count,
            'book': gift.book,
            'id': gift.id
        }


class MyGift:
    def __init__(self):
        pass
