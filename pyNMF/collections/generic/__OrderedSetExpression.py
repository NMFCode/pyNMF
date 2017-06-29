class OrderedSetExpression(object):
    """docstring for OrderedSetExpression"""

    def __init__(self):
        super(OrderedSetExpression, self).__init__()

    def Add(self, item):
        raise NotImplementedError()

    def Clear(self):
        raise NotImplementedError()

    def Remove(self, item):
        raise NotImplementedError()

    @property
    def Count(self):
        raise NotImplementedError()