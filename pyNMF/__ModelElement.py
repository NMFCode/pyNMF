from pyNMF import EventHandler
from pyNMF.collections.generic import Enumerable

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
        if self.__parent is None:
            return None
        else:
            return self.__parent.Model

    @property
    def Parent(self):
        return self.__parent

    @Parent.setter
    def Parent(self, newParent):
        old_parent = self.__parent
        if newParent is not old_parent:
            old_model = None
            if old_parent is not None:
                old_model = old_parent.Model
            self.__parent = newParent
            new_model = None
            if newParent is not None:
                new_model = newParent.Model
            if new_model is not old_model:
                self.PropagateNewModel(new_model, old_model, self)

    def Resolve(self, relativeUri):
        relativeUri = str(relativeUri)
        if relativeUri is None or relativeUri == '':
            return self
        segments = relativeUri.split('/')
        current = self
        for segment in segments:
            if current is None:
                return None
            if segment != '':
                current = current._GetModelElementForPathSegment(segment)
        return current

    def _GetModelElementForPathSegment(self, segment):
        if segment is None:
            return self
        if segment.startswith('#'):
            q_string = segment[1:]
            for child in self.Children:
                if not child.IsIdentified:
                    continue
                if child.ToIdentifierString().upper() == q_string:
                    return child
            return None
        reference, index = ModelHelper.ParseSegment(segment)
        return self.GetModelElementForReference(reference, index)

    def GetModelElementForReference(self, reference, index):
        pass

    def _GetRelativePathForChild(child):
        raise NotImplementedError("Not Implemented")

    def OnPropertyChanged(self, propertyName, valueChangedEvent):
        pass

    def OnPropertyChanging(self, propertyName, valueChangedEvent):
        pass

    def OnCollectionChanging(self, propertyName, changeEvent):
        pass

    def OnCollectionChanged(self, propertyName, changeEvent):
        pass

    def GetRelativePathForNonIdentifiedChild(self, element):
        return None

    def GetAttributeValue(self, attribute_name, index):
        return None

    def GetCollectionForFeature(self, feature):
        return None

    def SetFeature(self, feature, value):
        raise Exception()

    def GetCompositionName(self, container):
        return None

    def CreateUriFromGlobalIdentifier(self, fragment, absolute):
        return None

    def PropagateNewModel(self, new_model, old_model, subtree_root):
        pass

    @property
    def IsIdentified(self):
        return False

    @property
    def ReferencedElements(self):
        return Enumerable.Empty()

    @property
    def Children(self):
        return Enumerable.Empty()

class Model(ModelElement):
    
    def __init__(self):
        super(Model, self).__init__()
        self.__ids = {}
    
    @property
    def Model(self):
        return self
    
    def UnregisterId(self, id):
        del self.__ids[id]
    
    def RegisterId(self, id, value):
        self.__ids[id] = value

    def ResolveId(self, id):
        return self.__ids.get(id)

class ModelHelper(object):

    @staticmethod
    def IndexOfReference(collection, element):
        pass

    @staticmethod
    def CreatePath(collection, index):
        return "@" + collection + "." + str(index)

    @staticmethod
    def ParseSegment(segment):
        if segment.startswith('@'):
            segment = segment[1:]
        dindex = segment.find('.')
        if dindex != -1:
            reference = segment[0:dindex]
            dindex = int(segment[dindex+1:])
            return reference.upper(), dindex
        else:
            return segment.upper(), 0
