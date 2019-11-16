class KV:
	key = None
	value = None
	
	def __init__(self, key, value):
		self.key = key
		self.value = value
	
	def __str__(self):
		return "%s\t%s" % (str(key), str(value))