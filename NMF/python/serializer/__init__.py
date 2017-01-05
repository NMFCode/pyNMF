import xml.sax
import xml.sax.handler
import io
from ModelContentHandler import ModelContentHandler


def serialize(xml_doc, types):
    """
    @param xml_doc xml document as str
    @param types list featuring all types
    """
    # create lookup dict
    types_dict = {}
    for t in types:
        types_dict[t.__name__.upper()] = t    
    print types_dict
    # setup parser
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, True)
    parser.setFeature(xml.sax.handler.feature_namespace_prefixes, False)
    content_handler = ModelContentHandler(types_dict)
    parser.setContentHandler(content_handler)
    parser.parse(io.BytesIO(xml_doc))
    return content_handler.rootObject

if __name__ == '__main__':
    with open('My.xmi', 'r') as xml_doc:
        CreateFromDocument(xml_doc.read())
