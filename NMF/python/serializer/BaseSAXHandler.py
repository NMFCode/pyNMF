import xml
from SaxElementState import SAXElementState

#from pdb import set_trace as bp
def bp():
    pass

class BaseSAXHandler (xml.sax.handler.ContentHandler, object):
    """A SAX handler class that maintains a stack of enclosing elements and
    manages namespace declarations.

    This is the base for ModelContentHandler
    """

    # The state for the element currently being processed
    def elementState(self):
        bp()
        return self.__elementState
    __elementState = None

    # The states for all enclosing elements
    # All states for which startElement has been called but not endElement
    # the current element will always be the top element
    __elementStateStack = []

    def reset(self):
        """Reset the state of the handler in preparation for processing a new
        document.
        """
        bp()
        self.__elementState = self.__elementStateConstructor(content_handler=self)
        self.__elementStateStack = []
        self.__rootObject = None
        # Note: setDocumentLocator is invoked before startDocument (which
        # calls this), so this method should not reset it.
        return self

    def __init__(self, **kw):
        """Create a new xml.sax.handler.ContentHandler instance to maintain state relevant to elements."""                
        bp()
        self.__elementStateConstructor = SAXElementState

    def startDocument(self):
        """Process the start of a document.

        This resets this handler for a new document.
        @note: setDocumentLocator is invoked before startDocument
        """
        bp()
        self.reset()

    def startElementNS(self, name, qname, attrs):
        """Process the start of an element."""    

        # Save the state of the enclosing element, and create a new
        # state for this element.
        bp()
        parent_state = self.__elementState
        self.__elementStateStack.append(self.__elementState)        
        self.__elementState = this_state = self.__elementStateConstructor(content_handler=self,
                                                                          parent_state=parent_state)
        return (this_state, parent_state)

    def endElementNS(self, name, qname):
        """Process the completion of an element."""        

        # Save the state of this element, and restore the state for
        # the parent to which we are returning.
        bp()
        this_state = self.__elementState
        parent_state = self.__elementState = self.__elementStateStack.pop()
        # Restore namespace context and prepare for new namespace directives

        return this_state


