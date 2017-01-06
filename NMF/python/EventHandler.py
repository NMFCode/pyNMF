class EventHandler(object):
	"""docstring for EventHandler"""
	def __init__(self):
		super(EventHandler, self).__init__()

	def Invoke(self, sender, eventArgs):
		# tell all listeners...
		pass	
		
	def __iadd__(self, other):
		return self

	def __isub__(self, other):
		return self