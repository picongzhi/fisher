class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(good) for good in goods]

    def __map_to_trade(self, good):
        return dict(
            id=good.id,
            time=good.create_datetime.strftime('%Y-%m-%d') if good.create_datetime else '未知',
            user_name=good.user.nickname
        )


class MyTrades:
    def __init__(self, trades_of_mine, trade_count_list):
        self.__trades_of_mine = trades_of_mine
        self.__trade_count_list = trade_count_list
        self.trades = self.__parse()

    def __parse(self):
        trades = []
        for trade in self.__trades_of_mine:
            trades.append(self.__matching(trade))

        return trades

    def __matching(self, wish):
        count = 0
        for trade_count in self.__trade_count_list:
            if wish.isbn == trade_count['isbn']:
                count = trade_count['count']
                break

        return {
            'count': count,
            'book': wish.book,
            'id': wish.id
        }
