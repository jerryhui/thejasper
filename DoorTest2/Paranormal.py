import VRScript
import lel_common
import Animation

# Represents a paranormal living in the Jasper. Serves as the base class for all paranormals.
# Remarks:
# 	All paranormals have three states in The Jasper:
# 		1) Hiding (pre-discovery)
#					The paranormal is not out in the open. Player can discover it by interacting with it
#					using voice commands or controller. Once discovered, it advances to the next state.
#			2) Discovered
#					The paranormal is out in the open, visually prominent. Player can now capture it by
#					interaction through voice or controller. Once captured, the paranormal will advance to
#					the Captured state.
#			3) Captured
#					The paranormal is now captured. Players will not be able to see it anymore.
#
#		As the state advances, there can be a different animation. Animations can be programmatic 
#		or pre-rendered using FBX.
class Paranormal(lel_common.GenericObject):
	# Constructor.
	# Input:
	#		name - Name of paranormal (for display)
	#		location - Location within model (use VRScript's format)
	#		discoverCommand - voice command to discover this paranormal
	def __init__(self, name, location, discoverCommand):
		self.name = name
		self.location = location
		self.isCaptured = False
		self.discoverCommand = discoverCommand
		self.type = "paranormal"
	
	# Converts this Paranormal to a string.
	def __str__(self):
		return self.getName()

	# Returns the name of this paranormal.
	def getName(self):
		return self.name + " the " + self.type

	# Captures this Paranormal.
	def Capture(self, command):
		# check if correct capture command was used
		if command != self.discoverCommand:
			return False
			
		self.isCaptured = True
		self.CaptureAnimation()
		
	# Runs visual feedback of successful capture.
	def CaptureAnimation(self):
		print "You have captured ", self, "!\n"
		
		
class Ghost(Paranormal):
	def __init__(self, name, location, discoverCommand):
		Paranormal.__init__(self, name, location, discoverCommand)
		self.type = "ghost"
		
class EvilSoup(Paranormal):
	def __init__(self, name, location, discoverCommand):
		Paranormal.__init__(self, name, location, discoverCommand)
		self.type = "evil soup"