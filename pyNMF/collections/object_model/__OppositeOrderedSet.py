from pyNMF.collections.object_model import ObservableOrderedSet


class ObservableOppositeOrderedSet(ObservableOrderedSet):
    """docstring for CompositionOrderedSet"""

    def _SetParent(self, newParent):
        raise NotImplementedError()

    def __init__(self, parent):
        super(ObservableOppositeOrderedSet, self).__init__()
        self.parent = parent

    def Add(self, item):
        if super(ObservableOppositeOrderedSet, self).Add(item):
            self._SetParent(self.parent)

    def Clear(self):
        for item in self._items:
            if item.parent is self.parent:
                self._SetParent(None)
        super(ObservableOppositeOrderedSet, self).Clear()

    def Remove(self, item):
        if item.parent is self.parent:
            self._SetParent(None)
        self.remove(item)