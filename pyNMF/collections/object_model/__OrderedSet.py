from pyNMF.collections.generic import OrderedSetExpression


class CollectionEvent(object):
    """docstring for CollectionEvent"""

    def __init__(self):
        super(CollectionEvent, self).__init__()

    def __iadd__(self, other):
        pass

    def __isub__(self, other):
        pass


class ObservableOrderedSet(OrderedSetExpression):
    """docstring for CompositionOrderedSet"""

    def __init__(self):
        super(ObservableOrderedSet, self).__init__()
        self._items = list()
        self.CollectionChanged = CollectionEvent()
        self.CollectionChanging = CollectionEvent()

    def Add(self, item):
        if item not in self._items:
            self._items.append(item)
            return True
        else:
            return False

    def Clear(self):
        del self._items[:]

    def Remove(self, item):
        self._items.remove(item)

    def __getitem__(self, item):
        return self._items[item]

    @property
    def Count(self):
        return len(self._items)
