class XmlIdentifierDelay(object):
	"""docstring for XmlIdentifierDelay"""
	def __init__(self, saxState):
		super(XmlIdentifierDelay, self).__init__()
		self.saxState = saxState

	def execute(self):
		raise Exception("Not implemented")


class XmlAddToCollectionDelay(XmlIdentifierDelay):
	"""docstring for XmlAddToCollectionDelay"""
	def __init__(self, saxState, targetCollection):
		super(XmlAddToCollectionDelay, self).__init__(saxState)
		self.targetCollection = targetCollection

	def execute(self):
		self.targetCollection.Add(self.saxState.bindingInstance)

class XmlSetPropertyDelay(XmlIdentifierDelay):
	"""docstring for XmlSetPropertyDelay"""
	def __init__(self, saxState, propertyName, value):
		super(XmlSetPropertyDelay, self).__init__(saxState)
		self.propertyName = propertyName
		self.value = value

	def execute(self):
		self.saxState.parseAttribute(self.propertyName, self.value)
