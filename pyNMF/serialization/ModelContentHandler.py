from SaxElementState import SAXElementState
from BaseSAXHandler import BaseSAXHandler
from __XmlSetPropertyDelay import XmlSetPropertyDelay
from pyNMF import Model


class ModelContentHandler(BaseSAXHandler):
    def __init__(self, types_dict):
        super(ModelContentHandler, self).__init__()
        self.types_dict = types_dict
        # delayAttributeStates gets iterated over when done parsing.
        # All the attributes are set as a last step to ensure,
        # references to instances can be resolved (see endDocument)
        self.__delays = []
        self.rootObject = None
        self.model = Model()

    def startElementNS(self, name, qname, attrs):
        """Parses an XML element"""
        thisState, parent_state = super(ModelContentHandler, self).startElementNS(name, qname,
                                                                                  attrs)

        # cannot handle unicode named attributes, convert everything to ascii
        plain_name = name[1].encode('ascii', errors='ignore')
        # The uppercase convention is in the C# code, too.
        # (not used necessarily, only used to find out what kind of element we're dealing with here)
        plain_name = plain_name.upper()

        if parent_state.elementBinding is None:
            # root element
            thisState.elementBinding = self.types_dict.get(plain_name)
        else:
            # get the type arguments for plain_name
            # (in case of a collection/generic this will be the type it contains e.g. List<TypeArgument>)
            # this will also be created for the root element but discarded since the root does not have a parent,
            # so ignore in case of root
            fullAttrTypeName = "_typeOf" + plain_name  # typeArgsOfSOMETHING gets automatically generated into the result

            if hasattr(parent_state.elementBinding,
                       fullAttrTypeName):  # check if parent knows what type the element should be
                thisState.elementBinding = getattr(parent_state.elementBinding, fullAttrTypeName)()

        if thisState.elementBinding is None:
            raise Exception("FATAL ERROR: Unkown type " + name[1] + "!")

        binding_object = thisState.startBindingElement(thisState.elementBinding, attrs)

        if self.rootObject is None:
            self.rootObject = binding_object
            self.rootObject.Parent = self.model
            # replace dummy parent state of root with itself
            thisState.parentState = thisState
        else:
            parent = thisState.parentState.bindingInstance
            collection = parent.GetCollectionForFeature(plain_name)
            if collection is not None:
                collection.Add(binding_object)
            else:
                parent.SetFeature(plain_name, binding_object)

    def endElementNS(self, name, qname):
        this_state = super(ModelContentHandler, self).endElementNS(name, qname)
        binding_object, newPropertySettings = this_state.endBindingElement()
        self.__delays += newPropertySettings

    def resolve(self, value):
        if value[0:3] == '#//':
            return self.rootObject.Resolve(value[3:])
        elif '#' in value:
            raise Exception("References across file boundaries currently not supported")
        else:
            return self.model.ResolveId(value)

    def endDocument(self):
        for d in self.__delays:
            d.execute(self.resolve)
