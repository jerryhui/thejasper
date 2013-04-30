import VRScript
import lel_common
import Animation
import math
import time

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
	#		sMeshName - Name of renderable file (OBJ or FBX)
	#		location - Location within model (use VRScript's format)
	#		discoverCommand - voice command to discover this paranormal
	def __init__(self, name, sMeshName, location, discoverCommand, initState=ParanormalState.Hiding):
		lel_common.GenericObject.__init__(self, name, sMeshName, location, True, True, "Concave", True, "Static")
		self.state = initState
		self.discoverCommand = discoverCommand
		self.type = "paranormal"
		self.discoveredFBX = None
		self.capturedFBX = None
		self.animObj = None
		self.discoveredAnimPlaymode = VRScript.Core.PlayMode.Loop
		self.capturedAnimPlaymode = VRScript.Core.PlayMode.Once
		print(self.name + " initialized. Current state=" + str(self.state))
	
	# Converts this Paranormal to a string.
	def __str__(self):
		return self.getName()

	# Returns the name of this paranormal.
	def getName(self):
		return self.name + " the " + self.type

	def IsCaptured(self):
		return (self.state == ParanormalState.Captured)

	# Sets the animation file to play when this paranormal is discovered.
	# Set this to null if a programmatic animation is to be used; implement DiscoveredAnimation()
	# to provide programmatic animation.
	# Inputs:
	#	file - file name of FBX
	#	mode(OPT) - playback mode; as VRScript.Core.PlayMode
	def SetDiscoveredAnimation(self, file, mode=VRScript.Core.PlayMode.Loop, preAngles=[0,0,0], preScale=VRScript.Math.Vector(1,1,1)):
		self.discoveredFBX = Animation.AnimationMeta(self.name + "_discovered", file, mode, preScale, preAngles)
		print ("Set discovery anim for " + str(self) + " to " + file)

	# Discovers this paranormal. Note that the interactive method that calls this function
	# will have to perform validation on whether the interaction was correct.
	def Discover(self):
		if (self.state == ParanormalState.Hiding):
			self.state = ParanormalState.Discovered
			if (self.discoveredFBX is None):
				self.DiscoveredAnimation()
			else:
				print("Use FBX for " + str(self) + "-discovered")
				self.renderable(self.name).hide()
				self.animObj = Animation.AnimationObject(self.name + "_discovered")
				self.animObj.LoadAnimMeta(self.discoveredFBX)
				self.animObj.SetPosition(self.movable().getPose())
				self.animObj.Play(self.discoveredAnimPlaymode)

	# Sets the animation file to play when this paranormal is captured.
	# Set this to null if a programmatic animation is to be used; implement CapturedAnimation()
	# to provide programmatic animation.
	# Inputs:
	#	file - file name of FBX
	#	mode(OPT) - playback mode; as VRScript.Core.PlayMode
	def SetCapturedAnimation(self, file, mode=VRScript.Core.PlayMode.Once, preAngles=[0,0,0], preScale=VRScript.Math.Vector(1,1,1)):
		self.capturedFBX = Animation.AnimationMeta(self.name + "_discovered", file, mode, preScale, preAngles)

	# Captures this Paranormal. Note that the interactive method that calls this function
	# will have to perform validation on whether the interaction was correct.
	def Capture(self):
		if (self.state == ParanormalState.Discovered):
			self.state = ParanormalState.Captured
			self.CapturedAnimation()
		if (self.capturedFBX is None):
			print("Use CapturedAnimation()")
			self.CapturedAnimation()
		else:
			self.renderable(self.name).hide()
			self.animObj = Animation.AnimationObject(self.name + "_captured")
			# self.animObj.LoadAnimation(self.capturedFBX)
			self.animObj.LoadAnimMeta(self.capturedFBX)
			self.animObj.SetPosition(self.movable().getPose())
			self.animObj.Play(self.capturedAnimPlaymode)

	# Advances the state. 
	# Returns: True if state was advanced.
	def AdvanceState(self):
		if (self.state == ParanormalState.Hiding):
			self.Discover()
			return True
		elif (self.state == ParanormalState.Discovered):
			self.Capture()
			return True
		return False

	# Runs visual feedback of successful discovery.
	def DiscoveredAnimation(self):
		print("You have discovered "+str(self)+"!\n")
				
	# Runs visual feedback of successful capture.
	def CapturedAnimation(self):
		print("You have captured "+str(self)+"!\n")
		self.renderable(self.name).hide()
		if (self.animObj is not None):
			self.animObj.renderable('').hide()
	
	# Runs visual effect while idle.
	def IdleAnimation(self):
		# implement if idle animation via programming is wanted
		pass
	
	# Implements VRScript.Core.Behavior.OnUpdate.
	def OnUpdate(self, cbInfo):
		self.IdleAnimation()
		
	# Implements VRScript.Core.Behavior.OnButtonRelease.
	# Discovers/catches the paranormal by button click.
	def OnButtonRelease(self, cbInfo, btnInfo, intInfo):
		print(str(self) + " is clicked.")
		if (btnInfo.button == 0):
			self.AdvanceState()
	
class Ghost(Paranormal):
	def __init__(self, name, sMeshName, location, discoverCommand, initState=ParanormalState.Hiding, hoverDist=0.001, hoverSpeed=0.01):
		Paranormal.__init__(self, name, sMeshName, location, discoverCommand, initState)
		self.type = "ghost"
		self.hover = -1
		self.hoverDistance = hoverDist
		self.hoverSpeed = hoverSpeed
		self.shrinkCount = 0
		print("New ghost " + name + " created")
	
	def Discover(self):
		Paranormal.Discover(self)
		self.hover=0	# kicks off hovering
	
	def Capture(self):
		self.shrinkCount=10
		Paranormal.Capture(self)
		self.hover=-1	# turns off hovering
	
	def CapturedAnimation(self):
		print("Capture - shrink, shrink count=", self.shrinkCount)
		if (self.shrinkCount>0):
			m = self.movable().getPose()
			# m.postScale(VRScript.Math.Vector(50,50,50))
			m.postEuler(10,10,10)
			self.movable().setPose(m)
			self.shrinkCount -= 1
			time.sleep(.15)
			self.CapturedAnimation()
		else:
			self.shrinkCount = 0
			self.renderable(self.name).hide()
	
	def IdleAnimation(self):
		# Hover effect
		if (self.hover != -1):
			m = self.movable().getPose()
			m.preTranslation(VRScript.Math.Vector(0,0,math.sin(self.hover)*self.hoverDistance))
			self.movable().setPose(m)
			self.hover += self.hoverSpeed
			self.hover %= 360	
	
class EvilSoup(Paranormal):
	def __init__(self, name, sMeshName, location, discoverCommand, initState=ParanormalState.Hiding):
		Paranormal.__init__(self, name, sMeshName, location, discoverCommand, initState)
		self.type = "evil soup"
