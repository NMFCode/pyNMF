from pdb import set_trace as bp
from XmlIdentifierDelay import XmlAddToCollectionDelay, XmlSetPropertyDelay

# def bp():
#     pass

XMI_NS = "http://www.omg.org/XMI"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"


class SAXElementState(object):
    """State required to generate bindings for a specific element."""

    def __init__(self, **kw):
        super(SAXElementState, self).__init__()
        # The binding instance being created for this element.
        self.bindingInstance = None
        # The schema binding for the element being constructed.
        # Generally ignored, except at the top level this is the only way to
        # associate a binding instance created from an xsi:type description with
        # a specific element
        self.elementBinding = None
        self.parentState = kw.get('parent_state', None)
        self.__contentHandler = kw.get('content_handler', None)
        self._collectionAdditions = []
        self._propertySettings = []
        self.__content = []

    # Create the binding instance for this element.
    def __constructElement(self, type_class, attrs, constructor_parameters=None):

        if constructor_parameters is None:
            constructor_parameters = []

        xsiAttrs = filter(lambda x: x[0] == XSI_NS, attrs.getNames())
        for attr in xsiAttrs:
            if (attr[1] == 'type'):
                cls_name = attrs.getValue(attr).upper()
                if (cls_name in self.__contentHandler.types_dict):
                    self.bindingInstance = self.__contentHandler.types_dict[cls_name](
                        *constructor_parameters)
                else:
                    raise Exception("Unkown type " + cls_name + " when trying to resolve xsi type")
            elif (attr[1] == 'nil'):
                # TODO
                pass
            else:
                raise Exception("Unkown XSI Attribute " + attr[1])

        if self.bindingInstance == None:
            self.bindingInstance = type_class(*constructor_parameters)

        self.parseAttributes(attrs)

        return self.bindingInstance

    def addCollectionAdditionDelay(self, collection):
        self._collectionAdditions.append(XmlAddToCollectionDelay(self, collection))

    def addPropertySettingDelay(self, propertyName, value):
        self._propertySettings.append(XmlSetPropertyDelay(self, propertyName, value))

    def startBindingElement(self, type_class, attrs):
        """Actions upon entering an element that will produce a binding instance.

        Wrapper for constructElement

        @param type_class: The Python type (class) of the binding instance
        @param attrs: The XML attributes associated with the element
        @type attrs: C{xml.sax.xmlreader.Attributes}
        @return: The generated binding instance
        """
        self.__constructElement(type_class, attrs)
        return self.bindingInstance

    def endBindingElement(self):
        """Perform any end-of-element processing."""
        # at this point only the element instance exists, it is not populated yet
        return (self.bindingInstance, self._collectionAdditions, self._propertySettings)

    # decides if an attribute can be handled or should be later
    def parseAttributes(self, attrs):
        # Set instance attributes
        # bp()
        for attr_name in attrs.getNames():

            # Ignore xmlns and xsi attributes
            if (attr_name[0] is not None and attr_name[0] in (XMI_NS, XSI_NS)):
                # print("XMI attr: " + attr_name[0] + " " + attr_name[1])
                # Ignore, we already handled those
                continue
            value = attrs.getValue(attr_name)
            if (value[:2] == '//'):
                self.addPropertySettingDelay(attr_name, value)
            else:
                self.parseAttribute(attr_name, value)

    def parseAttribute(self, attr, value):
        if (attr == None):
            return
        if (isinstance(attr, tuple)):
            if (attr[0] is not None and attr[0] in (XMI_NS, XSI_NS)):
                print("Error: Cannot set xsi/xmi attributes after instance initialization")
                return
            attr = attr[1]  # ignore namespace

        if value[:2] == '//':
            if value[2] == '@':
                # TODO: not only support parent container references... REDO when Model Repositroy is implemented
                value = (value[3:]).encode('ascii', errors='ignore')
                attr_container, index = value.split('.')
                index = int(index)
                attr_container = attr_container.upper()
                attr_container = str(attr_container)
                try:
                    value = self.parentState.bindingInstance.GetModelElementForReference(
                        attr_container, index)
                except Exception, e:
                    from pdb import set_trace
                    set_trace()
                    value = self.parentState.bindingInstance.GetModelElementForReference(
                        attr_container, index)
                    raise e
            else:
                print("ERROR: XLinks are not supported, skipping (" + self.value + ")")
                return
        else:
            if (isinstance(value, unicode)):
                value = str(value)
            # is bool or number
            if (value in ('True', 'true')):
                value = True
            elif (value in ('False', 'false')):
                value = False
            else:
                tmpv = value
                try:
                    tmpv = float(tmpv)
                except ValueError, e:
                    pass
                else:
                    if (tmpv.is_integer()):
                        value = int(tmpv)
                    else:
                        value = tmpv

        # setattr(self.saxState.bindingInstance, self.propertyName, self.value)
        plain_name = attr.encode('ascii', errors='ignore')
        plain_name = plain_name.upper()
        self.bindingInstance.SetFeature(plain_name, value)

    def contentHandler(self):
        """Reference to the xml.sax.handler.ContentHandler that is processing the document."""
        return self.__contentHandler

    __contentHandler = None
