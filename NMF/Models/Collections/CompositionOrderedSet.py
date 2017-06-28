from ...Collections.Generic import OrderedSetExpression


class CollectionEvent(object):
    """docstring for CollectionEvent"""

    def __init__(self):
        super(CollectionEvent, self).__init__()

    def __iadd__(self, other):
        pass

    def __isub__(self, other):
        pass


class ObservableCompositionOrderedSet(list, OrderedSetExpression):
    """docstring for CompositionOrderedSet"""

    def __init__(self, parent):
        super(ObservableCompositionOrderedSet, self).__init__()
        self.parent = parent
        self.CollectionChanged = CollectionEvent()
        self.CollectionChanging = CollectionEvent()

    def Add(self, item):
        if (item not in self):
            self.append(item)

    def Clear():
        # find better implementation
        for i in range(len(self)):
            self.pop()

    def Remove(self, item):
        self.items.remove(item)

    @property
    def Count(self):
        return len(self)
