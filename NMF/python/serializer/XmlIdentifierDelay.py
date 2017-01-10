class XmlIdentifierDelay(object):
	"""docstring for XmlIdentifierDelay"""
	def __init__(self, saxState):
		super(XmlIdentifierDelay, self).__init__()
		self.saxState = saxState

	def OnResolveIdentifiedObject(self):
		raise Exception("Not implemented")


class XmlAddToCollectionDelay(XmlIdentifierDelay):
	"""docstring for XmlAddToCollectionDelay"""
	def __init__(self, saxState, targetCollection):
		super(XmlAddToCollectionDelay, self).__init__(saxState)
		self.targetCollection = targetCollection

	def OnResolveIdentifiedObject(self):
		targetCollection.Add(saxState.bindingInstance)

class XmlSetPropertyDelay(XmlIdentifierDelay):
	"""docstring for XmlAddPropertyDelay"""
	def __init__(self, saxState, propertyName, value):
		super(XmlAddPropertyDelay, self).__init__(saxState)
		self.propertyName = propertyName
		self.value = value

	def OnResolveIdentifiedObject(self):
		setattr(self.saxState.bindingInstance, self.propertyName, self.value)
		
		
		
		