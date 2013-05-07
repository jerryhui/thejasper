# HouseObjects.py
# Contains objects that have additional interactive behaviors.
# class ProxTrigger(VRScript.Core.Behavior)
#	class Door(lel_common.GenericObject)
#	class BumpableObj(lel_common.GenericObject)

import VRScript
import lel_common
import Animation
import JasperConfig
import JasperEngine

# A ProxTrigger will call a list of functions (no param) when user comes within a given range of parentObj.
class ProxTrigger(VRScript.Core.Behavior):
	def __init__(self, name, parentObj, userProxTrigger=4.99, actions=[], oneTimeTrigger=True, willReset=False):
		VRScript.Core.Behavior.__init__(self, "Trigger_" + name)
		self.actions = []
		self.actions.extend(actions)
		self.userProxTrigger = distance
		self.userDist = -1
		self.parentObj = parentObj
		self.oneTimeTrigger = oneTimeTrigger	# set to True if trigger actions are run only once per distance breach
		self.willReset = willReset		# set to True if trigger is reset when user gets out of range
		self.triggerFired = False		# state of whether this trigger has been fired

	# Calculates the distance between parent and User0.
	# Returns:
	#	(float) distance between parentObj and User0
	def UserDistance(self):
		m = self.parentObj.movable().getPose()					
		uv = JasperEngine.User.movable().getPose().getTranslation()
		sv = m.getTranslation()
		d = uv-sv	
		return d.length()
		
	def OnUpdate(self, cbInfo):
		if (not self.triggerFired):
			d = self.UserDistance()
			if (self.userDist != d):
				self.userDist = d
				if (d <= self.userProxTrigger):
					if (self.oneTimeTrigger):
						self.triggerFired = True
					for act in self.actions:
						act()
		elif (self.willReset):
				d = self.UserDistance()
				if (self.userDist != d):
					self.userDist = d
					if (d > self.userProxTrigger):
						self.triggerFired = False
				
# A Door instance is a door that will open and close when user approaches, with animation and audio.
#		bool isOpen		- True if the object is the model of an open door
#		float openAngle - the angle to turn in order to OPEN the door
#		Animation.AudioObj soundFX	- sound effect of opening and closing this door
#		Door[] slaveDoors	- a list of other doors that should share the same open/close state with this door
class Door(lel_common.GenericObject):
	# Constructor.
	# Inputs:
	#		sName - name of this object
	#		sMeshName - OBJ file name
	#		position - 3-element array containing the initial coordinates of this object
	#		isOpen - set to True if the object is the model of an open door
	#		openAngle - the angle to turn in order to OPEN the door
	def __init__(self, sName, sMeshName, position, isOpen, openAngle):
		lel_common.GenericObject.__init__(self, sName, JasperConfig.ModelsDir + sMeshName, position, True, True, "Concave", True, "Static")
		self.isOpen = isOpen
		self.openAngle = openAngle
		self.soundFX = Animation.AudioObj(sName + "_fx", "door.wav")
		self.soundFX.SetParent(self)
		self.slaveDoors = []
		self.masterDoorPtr = None

	# Adds a door that should share the same state as this door.
	# Remarks:
	#		Have only ONE door out of a group to be the "master" door. All state checking will be done
	#		from the master door.
	# Input:
	#		door - another Door object
	def AddSlaveDoor(self,door):
		if (type(door) is not Door): return
		door.slaveDoors = []
		self.slaveDoors.append(door)
		door.masterDoorPtr = self
		self.masterDoorPtr = None
		print("Added {0} as slave to {1}".format(door.name, self.name))

	# Sets the sound effect to the opening and closing of this door.
	# Input:
	#	file - path to file (relative to JasperConfig.MusicDir)
	def SetSoundFX(self, file):
		self.soundFX.SetFile(file)

	def OnInit(self, cbInfo):
		lel_common.GenericObject.OnInit(self, cbInfo)
		# self.physical('').setConstraints( VRScript.Math.Vector(1,1,0), VRScript.Math.Vector(1,1,1) )
		
	# Rotates this door at the given Euler angles.
	def Rotate(self,x,y,z):
		m = self.movable().getPose()
		m.postEuler(x,y,z)
		self.movable().setPose(m)
		if (type(self.soundFX) is Animation.AudioObj): 
			self.soundFX.Play()
	
	# Opens this door.
	# Input:
	#	skipSlave(OPT) - for internal use only: do not check/open slave doors.
	#	justOpen(OPT) - just open this door without checking master/slave; necessary to stop recursion
	def Open(self, skipSlave=False, justOpen=False):
		if (justOpen or self.masterDoorPtr is None):
			# this is a master door
			print("Open door " + self.name)
			self.Rotate(self.openAngle,0,0)
			self.isOpen = True
			if (justOpen or not skipSlave):
				self.SetAllDoors()
		else:
			self.masterDoorPtr.Open()

	# Closes this door.
	# Input:
	#	skipSlave(OPT) - for internal use only: do not check/close slave doors.
	#	justClose(OPT) - just close this door without checking master/slave; necessary to stop recursion
	def Close(self, skipSlave=False, justClose=False):
		if (justClose or self.masterDoorPtr is None):
			print("Close door " + self.name)
			self.Rotate(self.openAngle*-1,0,0)
			self.isOpen = False
			if (justClose or not skipSlave):
				self.SetAllDoors()
		else:
			self.masterDoorPtr.Close()
	
	# Do a one-pass on all slave doors and open/close them according to CURRENT state of this door.
	def SetAllDoors(self):
		for slaveDoor in self.slaveDoors:
			if (self.isOpen != slaveDoor.isOpen):
				if (self.isOpen): 
					slaveDoor.Open(True,True)
				else:
					slaveDoor.Close(True,True)
	
	def OnUpdate(self, cbInfo):
		lel_common.GenericObject.OnUpdate(self, cbInfo)
	
	# Toggle this door on left click.
	# Implements VRScript.Core.Behavior.OnButtonRelease
	def OnButtonRelease(self, cbInfo, btInfo, user):
		print("Door" + self.name + " clicked")
		if (btInfo.button == 0):
			if (self.isOpen):
				self.Close()
			else:
				self.Open()
				
class BumpableObj(lel_common.GenericObject):
	def __init__(self,sName, sMeshName, position):
		lel_common.GenericObject.__init__(self, sName, JasperConfig.ModelsDir + sMeshName, position, True, True, "Concave", True, "Dynamic")
		self.bumpedSound = None
		self.physicsValues = [2.0, 0.25, 0.9, 1, 0.5]
		
	def SetBumpedSound(self,file):
		self.bumpedSound = Animation.AudioObj(self.name + "_BumpedSound", file, False)
	
	def OnButtonRelease(self,cbInfo,btnInfo,user):
		print(self.name + ".OnButtonRelease()")
		m = self.movable().entityToSelf('User0')
		
		vBackToFront = VRScript.Math.Vector(0,1,0)
		vBackToFront = m.transform(vBackToFront)
		
		p = self.physical('')
		p.setCollisionType(VRScript.Core.CollisionType.Dynamic)
		p.applyImpulse(vBackToFront, VRScript.Math.Vector(0,0,0))
	
	def OnCollision(self,cbInfo,intInfo):
		if (intInfo.otherEntity.getName() != "GroundPlane"):
			print(self.name + ".OnCollision() with " + intInfo.otherEntity.getName())
			m = self.movable().entityToSelf('User0')
			
			vBackToFront = VRScript.Math.Vector(0,1,0)
			vBackToFront = m.transform(vBackToFront)
			
			p = self.physical('')
			p.setCollisionType(VRScript.Core.CollisionType.Dynamic)
			p.applyImpulse(vBackToFront, VRScript.Math.Vector(0,0,0))
		
			if (self.bumpedSound is not None):
				print(self.name + "sound.Play()")
				self.bumpedSound.Play()