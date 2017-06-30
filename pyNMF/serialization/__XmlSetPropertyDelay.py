class XmlSetPropertyDelay(object):
    """docstring for XmlSetPropertyDelay"""

    def __init__(self, instance, propertyName, value):
        super(XmlSetPropertyDelay, self).__init__()
        self._propertyName = propertyName
        self._instance = instance
        self._value = value

    def execute(self, resolve):
        parent = self._instance.bindingInstance
        collection = parent.GetCollectionForFeature(self._propertyName)
        if collection is not None:
            values_split = self._value.split(' ')
            for value in values_split:
                resolved = resolve(value)
                if resolved is not None:
                    collection.Add(resolved)
        else:
            resolved = resolve(self._value)
            if resolved is not None:
                parent.SetFeature(self._propertyName, resolved)
