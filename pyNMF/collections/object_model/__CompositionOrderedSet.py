from pyNMF.collections.object_model import ObservableOrderedSet


class CollectionEvent(object):
    """docstring for CollectionEvent"""

    def __init__(self):
        super(CollectionEvent, self).__init__()

    def __iadd__(self, other):
        pass

    def __isub__(self, other):
        pass


class ObservableCompositionOrderedSet(ObservableOrderedSet):
    """docstring for CompositionOrderedSet"""

    def __init__(self, parent):
        super(ObservableCompositionOrderedSet, self).__init__()
        self.parent = parent

    def Add(self, item):
        if super(ObservableCompositionOrderedSet, self).Add(item):
            item.parent = self.parent

    def Clear(self):
        for item in self._items:
            if item.parent is self.parent:
                item.parent = None
        super(ObservableCompositionOrderedSet, self).Clear()

    def Remove(self, item):
        if item.parent is self.parent:
            item.parent = None
        self.remove(item)
