class ModelElement(object):
    """Defines the base class for a model element implementation"""
    # static
    EnforceModels = False
    PreferIdentifiers = False

    def __init__(self):
        super(ModelElement, self).__init__()
        self.__parent = None
        self.__children = None
        self.__extensions = None
        self.__deleting = False
        self.Deleted = EventHandler()

    @property
    def Model(self):
        current = self
        while current is not None:
            model = current
            if model is not None:
                return model
            else:
                current = current.parent

    @property
    def Parent(self):
        return self._Parent

    @Parent.setter
    def Parent(self, x):
        self._Parent = x

    def Resolve(relativeUri):
        raise NotImplementedError("Not Implemented")

    def GetRelativePathForChild(child):
        raise NotImplementedError("Not Implemented")

    def OnPropertyChanged(self, propertyName, valueChangedEvent, feature):
        pass

    def OnPropertyChanging(self, propertyName, valueChangedEvent, feature):
        pass
