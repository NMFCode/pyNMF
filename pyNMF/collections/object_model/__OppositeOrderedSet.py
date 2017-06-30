from pyNMF.collections.object_model import ObservableOrderedSet


class ObservableOppositeOrderedSet(ObservableOrderedSet):
    """docstring for CompositionOrderedSet"""

    def SetOpposite(self, item, newParent):
        raise NotImplementedError()

    def __init__(self, parent):
        super(ObservableOppositeOrderedSet, self).__init__()
        self.Parent = parent

    def Add(self, item):
        if super(ObservableOppositeOrderedSet, self).Add(item):
            self.SetOpposite(item, self.Parent)

    def Clear(self):
        for item in self._items:
            if item.parent is self.Parent:
                self.SetOpposite(item, None)
        super(ObservableOppositeOrderedSet, self).Clear()

    def Remove(self, item):
        if item.parent is self.Parent:
            self.SetOpposite(item, None)
        super(ObservableOppositeOrderedSet, self).Remove(item)