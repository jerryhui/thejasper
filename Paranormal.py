# Paranormal.py
# Contains all classes that represent paranormals in The Jasper.
#	class ParanormalState
#	class Paranormal(lel_common.GenericObject)
#	class Ghost(Paranormal)
#	class GhostFlyaway(Ghost)
# class Lurcher(Paranormal)
#	class Crawler(Paranormal)

import VRScript
import lel_common
import Animation
import math
import random
import time
import JasperConfig
import JasperEngine
import weakref

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
	#		string name - Name of paranormal (for display)
	#		string sMeshName - Name of renderable file (OBJ or FBX)
	#		int[3] location - Location within model (use VRScript's format)
	#		string discoverCommand - command to discover this paranormal
	#		ParanormalState initState - initial state of paranormal
	#		string captureCommand - command to catch this paranormal (default: CLICK)
	def __init__(self, name, sMeshName, location, discoverCommand, initState=ParanormalState.Hiding, captureCommand="CLICK"):
		lel_common.GenericObject.__init__(self, name, JasperConfig.MonstersDir + sMeshName, location, True, True, "Concave", True, "Static")
		self.discoverCommand = discoverCommand		# command(s) that will discover this paranormal
		self.captureCommand = captureCommand			# command(s) that will capture this paranormal
		self.type = "paranormal"		# human-friendly name for this type
		self.discoveredFBX = None		# animation file for discovery state
		self.discoveredAudio = None	# audio to play when discovered
		self.capturedFBX = None			# animation file for captured state
		self.capturedAudio = None		# audio to play when captured
		self.animObj = None					# animation object to hold discovered/captured animation
		self.discoveredAnimPlaymode = VRScript.Core.PlayMode.Loop		# how discovered animation should be played
		self.capturedAnimPlaymode = VRScript.Core.PlayMode.Once			# how captured animation should be played
		self.userDist = 0						# distance from user
		self.userProxTrigger = -1		# longest distance from user that will trigger OnUserProximity()
		self.isStaring = False			# set to True if paranormal should always rotate to face user
		self.state = ParanormalState.Hiding		# starting state of this paranormal
		if (initState == ParanormalState.Discovered):
			print("Init discover " + str(self))
			self.Discover()
		elif (initState == ParanormalState.Captured):
			self.state == ParanormalState.Discovered
			self.Capture()
		print(self.name + " initialized. Current state=" + str(self.state))
	
	# Converts this Paranormal to a string.
	def __str__(self):
		return self.getName()  + " the " + self.type

	# Returns the name of this paranormal.
	def getName(self):
		return self.name

	# Returns true if this paranormal is captured.
	def IsCaptured(self):
		return (self.state == ParanormalState.Captured)

	# Sets the distance from the user that will trigger OnUserProximity event.
	# Input:
	#	pd - distance that will trigger event.
	def SetUserProximityTrigger(self, pd):
		self.userProxTrigger = pd
	
	# Sets the flag for staring behavior.
	# Input:
	#	stare - set to True if paranormal should face user all the time
	def SetStaring(self, stare):
		self.isStaring = stare
	
	# Sets the animation file to play when this paranormal is discovered.
	# Set this to None if a programmatic animation is to be used; implement DiscoveredAnimation()
	# to provide programmatic animation.
	# Inputs:
	#	file - file name of FBX
	#	mode(OPT) - playback mode; as VRScript.Core.PlayMode
	def SetDiscoveredAnimation(self, file, mode=VRScript.Core.PlayMode.Loop, preAngles=[0,0,0], preScale=VRScript.Math.Vector(1,1,1)):
		self.discoveredFBX = Animation.AnimationMeta(self.name + "_discovered", file, mode, preScale, preAngles)
		print ("Set discovery anim for " + str(self) + " to " + file)

	# Sets the audio file to play when this paranormal is discovered.
	# Inputs:
	#	file - file name of audio
	#	loop(OPT) - True if sound should be looped whenever the paranormal is discovered; default=True
	def SetDiscoveredSound(self, file, loop=True):
		self.discoveredAudio = Animation.AudioObj(self.name + "_discovered", file, loop, self)
		print ("Set discovered audio for " + str(self) + " to " + file)
		
	# Discovers this paranormal. Note that the interactive method that calls this function
	# will have to perform validation on whether the interaction was correct.
	def Discover(self):
		if (self.state == ParanormalState.Hiding):
			self.state = ParanormalState.Discovered
			# play animation
			if (self.discoveredFBX is None):
				self.DiscoveredAnimation()
			else:
				print("Use FBX for " + str(self) + "-discovered")
				self.renderable(self.name).hide()
				self.animObj = Animation.AnimationObject(self.name + "_discovered")
				self.animObj.LoadAnimMeta(self.discoveredFBX)
				self.animObj.SetPosition(self.movable().getPose())
				self.animObj.Play(self.discoveredAnimPlaymode)
			# play audio
			if (self.discoveredAudio is not None):
				self.discoveredAudio.Play()

	# Sets the animation file to play when this paranormal is captured.
	# Set this to null if a programmatic animation is to be used; implement CapturedAnimation()
	# to provide programmatic animation.
	# Inputs:
	#	file - file name of FBX
	#	mode(OPT) - playback mode; as VRScript.Core.PlayMode
	def SetCapturedAnimation(self, file, mode=VRScript.Core.PlayMode.Once, preAngles=[0,0,0], preScale=VRScript.Math.Vector(1,1,1)):
		self.capturedFBX = Animation.AnimationMeta(self.name + "_discovered", file, mode, preScale, preAngles)

	# Sets the audio file to play when this paranormal is captured.
	# Inputs:
	#	file - file name of audio
	#	loop(OPT) - True if sound should be looped whenever the paranormal is discovered; default=False
	def SetCapturedSound(self, file, loop=False):
		self.capturedAudio = Animation.AudioObj(self.name + "_captured", file, loop, self)
		print ("Set discovered audio for " + str(self) + " to " + file)
		
	# Captures this Paranormal. Note that the interactive method that calls this function
	# will have to perform validation on whether the interaction was correct.
	def Capture(self):
		if (self.state == ParanormalState.Discovered):
			self.state = ParanormalState.Captured
			print(str(self) + ' is captured!')
			# play animation
			if (self.capturedFBX is None):
				print("Use CapturedAnimation()")
				self.CapturedAnimation()
			else:
				self.renderable(self.name).hide()
				self.animObj = Animation.AnimationObject(self.name + "_captured")
				self.animObj.LoadAnimMeta(self.capturedFBX)
				self.animObj.SetPosition(self.movable().getPose())
				self.animObj.Play(self.capturedAnimPlaymode)
			# play audio
			if (self.discoveredAudio is not None):
				self.discoveredAudio.Stop(self.capturedAudio is None, -0.5)
			if (self.capturedAudio is not None):
				self.capturedAudio.Play()
				
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
		if (self.renderable(self.name).isVisible()):
			print("You have captured "+str(self)+"!\n")
			self.renderable(self.name).hide()
		if (self.animObj is not None):
			self.animObj.renderable('').hide()
	
	# Runs visual effect while idle.
	def IdleAnimation(self):
		# implement if idle animation via programming is wanted
		pass

	# Calculates the distance between self and User0.
	# Returns:
	#	(float) distance between self and User0
	def UserDistance(self):
		m = self.movable().getPose()					
		uv = JasperEngine.User.movable().getPose().getTranslation()
		sv = m.getTranslation()
		d = uv-sv	
		return d.length()
	
	# This is triggered when the user is nearby. Implement if interaction is desired.
	def OnUserProximity(self):
		pass
	
	def OnInit(self, cbInfo):
		lel_common.GenericObject.OnInit(self, cbInfo)
	
	def StareAtUser(self):
		pM = self.movable().entityToSelf('User0')
		uM = JasperEngine.User.movable().entityToSelf(self.name)
		
		pTrans = pM.getTranslation()
		uTrans = uM.getTranslation()
		
		dotProd = pTrans.dot(uTrans)
		lengthProd = pTrans.length() * uTrans.length()
		cosVal = dotProd/lengthProd
		cosVal = min(1, max(-1, cosVal))	# clamp val to [-1,1]
		# print("{0}/{1} = {2}".format(dotProd, lengthProd, cosVal))
		angle = math.degrees(math.acos(-cosVal))

		pM = self.movable().getPose()
		pTrans = pM.getTranslation()
		
		if (math.floor(angle)>0):
			pM = pM.postAxisAngle(-1, VRScript.Math.Vector(0, 0, 1))
			print("{0} at angle {1} with user".format(self,angle))
		pM.setTranslation(pTrans)
		self.movable().setPose(pM)

		
		# pM = self.movable().selfToWorld()
		# pTrans = pM.getTranslation()
		# # pM = VRScript.Math.Matrix()
	
		# um = JasperEngine.User.movable().selfToWorld()
		
		# ueu = um.getEuler()
		# peu = pM.getEuler()
		# if (ueu.x - peu.x > 0):
			# pM = pM.postEuler(1, peu.y, peu.z)
		# else:
			# pM = pM.postEuler(-1, peu.y, peu.z)
		
		# pM.setTranslation(pTrans)
		# self.movable().setPose(pM)
	
	# Implements VRScript.Core.Behavior.OnUpdate.
	def OnUpdate(self, cbInfo):
		if (self.isStaring and self.state!=ParanormalState.Captured):
			# rotate to face user
			self.StareAtUser()
		
		if (self.userProxTrigger > 0):
			# implements user distance checking
			d = self.UserDistance()
			if (self.userDist != d):
				self.userDist = d
				if (d <= self.userProxTrigger):
					self.OnUserProximity()
					# print("{0}.userDist={1}".format(self,d))
		if (self.state == ParanormalState.Discovered):
			self.IdleAnimation()
		elif (self.state == ParanormalState.Captured):
			self.CapturedAnimation()
			
	# Implements VRScript.Core.Behavior.OnButtonRelease.
	# Discovers/catches the paranormal by button click.
	def OnButtonRelease(self, cbInfo, btnInfo, intInfo):
		print(str(self) + " is clicked.")
		if ("CLICK" in self.captureCommand and btnInfo.button < 3):
			self.AdvanceState()
		
class Ghost(Paranormal):
	def __init__(self, name, sMeshName, location, discoverCommand, initState=ParanormalState.Hiding, hoverDist=0.001, hoverSpeed=0.01):
		# debug: must set defautl Ghost properties that are needed for Discovered or Captured,
		# in case user wants initial state something other than Hiding
		self.hover = -1
		self.hoverDistance = hoverDist
		self.hoverSpeed = hoverSpeed
		self.shrinkCount = 0
		Paranormal.__init__(self, name, sMeshName, location, discoverCommand, initState)
		self.type = "ghost"
		self.SetDiscoveredSound("moan.wav")
		self.SetCapturedSound("scream1.wav")
		self.SetUserProximityTrigger(4)
		self.SetStaring(True)
		print("New ghost " + name + " created")
	
	def Discover(self):
		Paranormal.Discover(self)
		self.hover=0	# kicks off hovering
	
	def Capture(self):
		self.shrinkCount=20
		Paranormal.Capture(self)
		self.hover=-1	# turns off hovering
	
	# Shrink the ghost into oblivion!
	def CapturedAnimation(self):
		if (self.shrinkCount>0):
			print("Capture - shrink, shrink count=", self.shrinkCount)
			m = self.movable().getPose()
			m.preScale(VRScript.Math.Vector(0.9,0.9,0.9))
			self.movable().setPose(m)
			self.shrinkCount -= 1
		else:
			self.renderable('').hide()
	
	def IdleAnimation(self):
		# Hover effect
		if (self.hover != -1):
			m = self.movable().getPose()
			m.preTranslation(VRScript.Math.Vector(0,0,math.sin(self.hover)*self.hoverDistance))
			self.movable().setPose(m)
			self.hover += self.hoverSpeed
			self.hover %= 360
			
	def OnUserProximity(self):
		Paranormal.OnUserProximity(self)
		if (self.state == ParanormalState.Hiding):
			print("You've found {0} by proximity!".format(self))
			self.AdvanceState()

# Represents a ghost that flies straight up and away when captured.
class GhostFlyaway(Ghost):
	def Capture(self):
		self.flyCount=50
		self.flyDistance=0.01
		Paranormal.Capture(self)
		if (type(self.capturedAudio) is Animation.AudioObj):
			self.capturedAudio.SetParent(None)
		self.hover=-1	# turns off hovering
	
	# Sends the ghost up high heavens...
	def CapturedAnimation(self):
		if (self.flyCount>0):
			print("Capture - fly away count=", self.flyCount)
			m = self.movable().getPose()
			m.preTranslation(VRScript.Math.Vector(0,0,self.flyDistance))
			self.movable().setPose(m)
			self.flyCount -= 1
			self.flyDistance *= 2
		else:
			self.renderable('').hide()

# A Lurcher, when discovered, rushes forward and then disappears (captured)
class Lurcher(Paranormal):
	def __init__(self, name, sMeshName, location, discoverCommand, initState=ParanormalState.Hiding):
		Paranormal.__init__(self, name, sMeshName, location, discoverCommand, initState)
		self.type = "lurcher"
		self.SetStaring(True)
		self.physicsValues = [3.0, 0.9, 0.995, 1, 0.5]
		self.lastVec = VRScript.Math.Vector(0,0,0)
		print("{0} created.".format(self))

	# def OnInit(self,cbInfo):
		# Paranormal.OnInit(self,cbInfo)
		
	# Lurcher always moves toward player when idle.
	def OnUpdate(self, cbInfo):
		# if (cbInfo.frameCount % 5):
		if (self.isStaring and self.state!=ParanormalState.Captured):
			# rotate to face user
			self.StareAtUser()
		# else:	
			# # move towards user using Physics
			# # m = self.movable().selfToEntity('User0')
			# m = self.movable().selfToWorld()
			
			# vBackToFront = VRScript.Math.Vector(0,-1,0)
			# vBackToFront = m.transform(vBackToFront)
			# vBackToFront = vBackToFront.normalize()
			# vBackToFront = vBackToFront * 0.2
			# vBackToFront.z = 0
			
			# p = self.physical()
			# p.setCollisionType(VRScript.Core.CollisionType.Dynamic)
			
			# # attempt to stop this Lurcher in its track if angle changes
			# if (vBackToFront != self.lastVec):
				# print("vBackToFront {0},{1},{2}".format(vBackToFront.x, vBackToFront.y, vBackToFront.z))
				# self.lastVec = vBackToFront
				# # if (cbInfo.frameCount % 5 == 0):
					# # p.zeroMotion()
			
			# p.applyImpulse(vBackToFront, VRScript.Math.Vector(0,0,0))

		if (self.state == ParanormalState.Captured):
			self.CapturedAnimation()
			
class Crawler(Paranormal):
	def __init__(self, name, sMeshName, location, discoverCommand, initState=ParanormalState.Hiding):
		Paranormal.__init__(self, name, sMeshName, location, discoverCommand, initState)
		self.crawlDistance = 5
		self.type = "crawler"
		print("New Crawler " + name)

	def OnInit(self,cbInfo):
		Paranormal.OnInit(self,cbInfo)
		p = self.physical('')
		if (type(p) is VRScript.Core.Physical):
			print ("p is a Physical")
		pProp = VRScript.Core.PhysicsProperties(1,1,.99,.99,.5)
		self.physical('').setPhysicsProperties(pProp)
	
	# Lurcher always moves toward player when idle.
	def OnUpdate(self, cbInfo):
		if (cbInfo.frameCount % 5):
			if (self.isStaring and self.state!=ParanormalState.Captured):
				# rotate to face user
				self.StareAtUser()
		else:	
			# move towards user using Physics
			# m = self.movable().selfToEntity('User0')
			m = self.movable().selfToWorld()
			
			vBackToFront = VRScript.Math.Vector(0,-1,0)
			vBackToFront = m.transform(vBackToFront)
			vBackToFront = vBackToFront.normalize()
			vBackToFront = vBackToFront * 0.2
			vBackToFront.z = 0
			
			p = self.physical()
			p.setCollisionType(VRScript.Core.CollisionType.Dynamic)
			
			# attempt to stop this Lurcher in its track if angle changes
			if (vBackToFront != self.lastVec):
				print("vBackToFront {0},{1},{2}".format(vBackToFront.x, vBackToFront.y, vBackToFront.z))
				self.lastVec = vBackToFront
				# if (cbInfo.frameCount % 5 == 0):
					# p.zeroMotion()
			
			p.applyImpulse(vBackToFront, VRScript.Math.Vector(0,0,0))

		if (self.state == ParanormalState.Captured):
			self.CapturedAnimation()