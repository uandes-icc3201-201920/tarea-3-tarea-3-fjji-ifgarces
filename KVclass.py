""" UNUSED """

class KV:
	key = None
	value = None
	type = None
	
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.type = type(value)
		assert(type(key) == int and key >= 0)
	
	def __str__(self):
		return "%s\t%s\t%s" % (str(key), str(value), str(self.type))
	
	def TabPrint(self):      # tiene sentido para el tabulate
		return (self.key, self.value, self.type)