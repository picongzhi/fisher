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
