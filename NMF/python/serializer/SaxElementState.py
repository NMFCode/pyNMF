from pdb import set_trace as bp
# def bp():
#     pass

class XSINil(object):
    """docstring for XSINil"""
    def __init__(self):
        super(XSINil, self).__init__()
        

class SAXElementState (object):
    """State required to generate bindings for a specific element.

    If the document being parsed includes references to unrecognized elements,
    a DOM instance of the element and its content is created and treated as a
    wildcard element.
    """

    # An expanded name corresponding to xsi:nil
    __XSINilTuple = XSINil

    # The binding instance being created for this element.  When the
    # element type has simple content, the binding instance cannot be
    # created until the end of the element has been reached and the
    # content of the element has been processed accumulated for use in
    # the instance constructor.  When the element type has complex
    # content, the binding instance must be created at the start of
    # the element, so contained elements can be properly stored.
    __bindingInstance = None

    # The schema binding for the element being constructed.
    __elementBinding = None

    def setElementBinding(self, element_binding):
        """Record the binding to be used for this element.

        Generally ignored, except at the top level this is the only way to
        associate a binding instance created from an xsi:type description with
        a specific element."""
        self.__elementBinding = element_binding

    def setTargetContainer(self, target_container):
        self.__targetContainer = target_container
    __targetContainer = None

    def getTargetContainer(self):
        return self.__targetContainer        

    def getElementBinding(self):
        return self.__elementBinding

    def getBindingInstance(self):
        return self.__bindingInstance

    # The nearest enclosing complex type definition
    def enclosingCTD(self):
        """The nearest enclosing complex type definition, as used for
        resolving local element/attribute names.

        @return: An instance of L{basis.complexTypeDefinition}, or C{None} if
        the element is top-level
        """
        return self.__enclosingCTD
    __enclosingCTD = None

    # The factory that is called to create a binding instance for this
    # element; None if the binding instance was created at the start
    # of the element.
    __delayedConstructor = None    

    # An xml.dom.Node corresponding to the (sub-)document
    __domDocument = None

    __domDepth = None

    def __init__(self, **kw):
        super(SAXElementState, self).__init__()
        self.__bindingInstance = None
        self.__parentState = kw.get('parent_state')
        self.__contentHandler = kw.get('content_handler')
        self.__content = []
        parent_state = self.parentState()
        
        if parent_state is not None:
            self.__enclosingCTD = parent_state.enclosingCTD()
            self.__domDocument = parent_state.__domDocument
        if self.__domDocument is not None:
            print("__domDocument: is not None")
            self.__domDepth = parent_state.__domDepth + 1        

    def setEnclosingCTD(self, enclosing_ctd):
        print("\tSet Enclosing CTD to " + str(enclosing_ctd))
        """Set the enclosing complex type definition for this element.

        @param enclosing_ctd: The scope for a local element.
        @type enclosing_ctd: L{basis.complexTypeDefinition}
        @return: C{self}
        """
        self.__enclosingCTD = enclosing_ctd

    # Create the binding instance for this element.
    def __constructElement(self, type_class, attrs, constructor_parameters=None):
        
        if constructor_parameters is None:
            constructor_parameters = []
        self.__bindingInstance = type_class(*constructor_parameters)
        

        self.attrs = attrs
        

        return self.__bindingInstance

    def startBindingElement(self, type_class, attrs):
        """Actions upon entering an element that will produce a binding instance.

        Wrapper for constructElement

        @param type_class: The Python type (class) of the binding instance                    
        @param attrs: The XML attributes associated with the element
        @type attrs: C{xml.sax.xmlreader.Attributes}
        @return: The generated binding instance
        """        
        print("\tstartBindingElement")
        self.__constructElement(type_class, attrs)
        return self.__bindingInstance

    def endBindingElement(self):
        """Perform any end-of-element processing."""

        #at this point only the element instance exists, it is not populated yet
        #add to parent        
        
        #if it's None it's the root element which is not contained anywhere        
        tc = self.__targetContainer        
        if self.__targetContainer != None:
            self.__targetContainer.Add(self.__bindingInstance) 
        else:
            print(str(self.__bindingInstance) + " DOES NOT HAVE CONTAINER. IS ROOT ELEMENT?")            
        return self.__bindingInstance

    #handles the parsing and resolving attributes for an element
    def parseAttributes(self):
        # Set instance attributes    
        #bp()
        for attr_name in self.attrs.getNames():
            
            # Ignore xmlns and xsi attributes

            if (attr_name[0] is not None and attr_name[0] in ("http://www.omg.org/XMI")):
                continue

            # attributes           
            plain_name = attr_name[1].encode('ascii', errors='ignore')
            plain_name = plain_name.upper()               
            value = self.attrs.getValue(attr_name)

            if (value[:2] == '//'):
                if(value[2] == '@'):
                    #TODO: not only support parent container references...
                    value = (value[3:]).encode('ascii', errors='ignore')
                    attr_container, index = value.split('.')
                    index = int(index)
                    attr_container = attr_container.upper()    

                    try:             
                        value = self.parentState().getBindingInstance().GetModelElementForReference(attr_container, index)                    
                    except Exception, e:
                        from pdb import set_trace
                        set_trace()
                        raise e
                else:                    
                    print("ERROR: XLinks are not supported (" + value + ")")                    
                    continue
            plain_name = str(plain_name)            
            if (isinstance(value, unicode)):
                value = str(value)
            self.__bindingInstance.SetFeature(plain_name, value)



    def contentHandler(self):
        """Reference to the C{xml.sax.handler.ContentHandler} that is processing the document."""
        return self.__contentHandler
    __contentHandler = None

    def parentState(self):
        """Reference to the SAXElementState of the element enclosing this
        one."""
        return self.__parentState        
    __parentState = None

    def setParentState(self, new_parentState):
        self.__parentState = new_parentState