from NMF.Models.Repository import *
from NMF.Expressions import *
from NMF.Collections.ObjectModel import *
from ..python import *


class ModelElement(object):
    """Defines the base class for a model element implementation"""
    # static
    EnforceModels = False
    PreferIdentifiers = False

    def __init__(self):
        super(ModelElement, self).__init__()
        self.Parent = None
        self._Children = None
        self._extensions = None
        self._deleting = False
        self._Model = None
        self.RelativeUri = None
        self.AbsoluteUri = None
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

    @Model.setter
    def Model(self, x):
        self._Model = x

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

    def OnPropertyChanged(self, propertyName, valueChangedEvent):
        pass

    def OnPropertyChanging(self, propertyName, e=None):
        pass
