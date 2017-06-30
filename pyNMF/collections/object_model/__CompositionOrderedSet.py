from pyNMF.collections.object_model import ObservableOrderedSet


class ObservableCompositionOrderedSet(ObservableOrderedSet):
    """docstring for CompositionOrderedSet"""

    def __init__(self, parent):
        super(ObservableCompositionOrderedSet, self).__init__()
        self.parent = parent

    def Add(self, item):
        if super(ObservableCompositionOrderedSet, self).Add(item):
            item.Parent = self.parent

    def Clear(self):
        for item in self._items:
            if item.parent is self.parent:
                item.Parent = None
        super(ObservableCompositionOrderedSet, self).Clear()

    def Remove(self, item):
        if item.Parent is self.parent:
            item.Parent = None
        self.remove(item)
