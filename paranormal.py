class Paranormal(object):
	# Initializes a Paranormal.
	# Input:
	#		name - Name of paranormal (for display)
	#		location - Location within model (use VRScript's format)
	#		captureCommand - voice command to capture
	def __init__(self, name, location, captureCommand):
		self.name = name
		self.location = location
		self.isCaptured = False
		self.captureCommand = captureCommand
		self.type = "paranormal"
		
	def getName(self):
		return self.name + " the " + self.type
	
	def __str__(self):
		return self.getName()
	
	# Captures this Paranormal.
	def capture(self, command):
		# check if correct capture command was used
		if command != self.captureCommand:
			return False
			
		self.isCaptured = True
		self.captureAnimation()
		
	# Runs visual feedback of successful capture.
	def captureAnimation(self):
		print "You have captured ", self, "!\n"
		
		
class Ghost(Paranormal):
	def __init__(self, name, location, captureCommand):
		Paranormal.__init__(self, name, location, captureCommand)
		self.type = "ghost"
		
class EvilSoup(Paranormal):
	def __init__(self, name, location, captureCommand):
		Paranormal.__init__(self, name, location, captureCommand)
		self.type = "evil soup"