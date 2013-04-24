import VRScript
import lel_common
import Animation

# Enumerates all possible states of a paranormal. See documentation for Paranormal for more.
class ParanormalState:
	Hiding, Discovered, Captured = range(3)

# Represents a paranormal living in the Jasper. Serves as the base class for all paranormals.
# Remarks:
# 	All paranormals have three states in The Jasper:
# 		1) Hiding (pre-discovery)
#			The paranormal is not out in the open. Player can discover it by interacting with it
#			using voice commands or controller. Once discovered, it advances to the next state.
#		2) Discovered
#			The paranormal is out in the open, visually prominent. Player can now capture it by
#			interaction through voice or controller. Once captured, the paranormal will advance to
#			the Captured state.
#		3) Captured
#			The paranormal is now captured. Players will not be able to see it anymore.
#
#		As the state advances, there can be a different animation. Animations can be programmatic 
#		or pre-rendered using FBX.
class Paranormal(lel_common.GenericObject):
	# Constructor.
	# Input:
	#		name - Name of paranormal (for display)
	#		location - Location within model (use VRScript's format)
	#		discoverCommand - voice command to discover this paranormal
	def __init__(self, name, location, discoverCommand, initState=ParanormalState.Hiding):
		self.name = name
		self.location = location
		self.state = initState
		self.discoverCommand = discoverCommand
		self.type = "paranormal"
		self.discoveredFBX = ""
		self.capturedFBX = ""
		self.animObj = None
		self.discoveredAnimPlaymode = VRScript.Core.PlayMode.Loop
		self.capturedAnimPlaymode = VRScript.Core.PlayMode.Once
	
	# Converts this Paranormal to a string.
	def __str__(self):
		return self.getName()

	# Returns the name of this paranormal.
	def getName(self):
		return self.name + " the " + self.type

	# Sets the animation file to play when this paranormal is discovered.
	# Set this to null if a programmatic animation is to be used; implement DiscoveredAnimation()
	# to provide programmatic animation.
	# Inputs:
	#	file - file name of FBX
	#	mode(OPT) - playback mode; as VRScript.Core.PlayMode
	def SetDiscoveredAnimation(self, file, mode=VRScript.Core.PlayMode.Loop):
		self.discoveredFBX = file
		self.discoveredAnimPlaymode = mode

	# Discovers this paranormal. Note that the interactive method that calls this function
	# will have to perform validation on whether the interaction was correct.
	def Discover(self):
		if (self.state == ParanormalState.Hiding):
			self.state = ParanormalState.Discovered
			if (self.discoveredFBX == ""):
				self.DiscoveredAnimation()
			else:
				self.renderable(self.name).hide()
				self.animObj = Animation.AnimationObject(self.name + "_discovered")
				self.animObj.LoadAnimation(self.discoveredFBX)
				self.animObj.SetPosition(self.movable().getPose())
				self.animObj.Play(self.discoveredAnimPlaymode)

	# Runs visual feedback of successful discovery.
	def DiscoveredAnimation(self):
		print "You have discovered ", self, "!\n"
		
	# Sets the animation file to play when this paranormal is captured.
	# Set this to null if a programmatic animation is to be used; implement CapturedAnimation()
	# to provide programmatic animation.
	# Inputs:
	#	file - file name of FBX
	#	mode(OPT) - playback mode; as VRScript.Core.PlayMode
	def SetCapturedAnimation(self, file, mode=VRScript.Core.PlayMode.Once):
		self.capturedFBX = file
		self.capturedAnimPlaymode = mode

	# Captures this Paranormal. Note that the interactive method that calls this function
	# will have to perform validation on whether the interaction was correct.
	def Capture(self):
		if (self.state == Paranormal.Discovered):
			self.state = ParanormalState.Captured
			self.CapturedAnimation()
		if (self.capturedFBX == ""):
			self.CapturedAnimation()
		else:
			self.renderable(self.name).hide()
			self.animObj = Animation.AnimationObject(self.name + "_captured")
			self.animObj.LoadAnimation(self.capturedFBX)
			self.animObj.SetPosition(self.movable().getPose())
			self.animObj.Play(self.capturedAnimPlaymode)
				
	# Runs visual feedback of successful capture.
	def CapturedAnimation(self):
		print "You have captured ", self, "!\n"
	
	# Runs visual effect while idle.
	def IdleAnimation(self):
		# implement if idle animation via programming is wanted
		pass
	
	# Implements VRScript.Core.Behavior.OnUpdate.
	def OnUpdate(self, cbInfo):
		self.IdleAnimation()
	
class Ghost(Paranormal):
	def __init__(self, name, location, discoverCommand):
		Paranormal.__init__(self, name, location, discoverCommand)
		self.type = "ghost"
		
class EvilSoup(Paranormal):
	def __init__(self, name, location, discoverCommand):
		Paranormal.__init__(self, name, location, discoverCommand)
		self.type = "evil soup"
