import VRScript
import lel_common
import Animation

# A Door instance is a door that will open and close when user approaches, with animation and audio.
class Door(lel_common.GenericObject):
	# Constructor.
	# Inputs:
	#		sName - name of this object
	#		sMeshName - OBJ file name
	#		position - 3-element array containing the initial coordinates of this object
	#		isOpen - set to True if the object is the model of an open door
	#		openAngle - the angle to turn in order to OPEN the door
	def __init__(self, sName, sMeshName, position, isOpen, openAngle):
		lel_common.GenericObject.__init__(self, sName, sMeshName, position, True, True, "Concave", True, "Static")
		self.isOpen = isOpen
		self.openAngle = openAngle
		self.soundFX = Animation.AudioObj(sName + "_fx", "door.wav")

	def OnInit(self, cbInfo):
		lel_common.GenericObject.OnInit(self, cbInfo)
		self.physical('').setConstraints( VRScript.Math.Vector(1,1,0), VRScript.Math.Vector(1,1,1) )
		# self.attach(VRScript.Resources.Collider(self.name, VRScript.Resources.Sphere(2)))
		
	def Rotate(self,x,y,z):
		# Rotates this door at the given degree.
		m = self.movable().getPose()
		m.postEuler(x,y,z)
		self.movable().setPose(m)
		if (type(self.soundFX) is Animation.AudioObj): 
			self.soundFX.Play()
		#self.physical('').applyImpulse( VRScript.Math.Vector(5,5,0), VRScript.Math.Vector(.125,.125,0) )
		#self.physical('').applyImpulse( VRScript.Math.Vector(-2,-2,0), VRScript.Math.Vector(-.125,-.125,0) )
	
	# Opens this door.
	def Open(self):
		print("Open door " + self.name)
		self.Rotate(self.openAngle,0,0)
		self.isOpen = True

	# Closes this door.
	def Close(self):
		print("Close door " + self.name)
		self.Rotate(self.openAngle*-1,0,0)
		self.isOpen = False
	
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
		lel_common.GenericObject.__init__(self, sName, sMeshName, position, True, True, "Concave", True, "Kinematic")
		self.bumpedSound = None
		
	def SetBumpedSound(self,file):
		self.bumpedSound = Animation.AudioObj(sName + "_BumpedSound", file)
		
	def OnCollision(self,cbInfo):
		if (type(self.bumpedSound) is Animation.AudioObj):
			self.bumpedSound.Play()