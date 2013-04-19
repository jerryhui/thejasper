import VRScript
import lel_common

# A Door instance is a door that will open and close when user approaches, with animation and audio.
class Door(lel_common.GenericObject):
	def __init__(self, sName, sMeshName, position, bVis, bPhysics, physicsShape, interact, physicsType):
		lel_common.GenericObject.__init__(self, sName, sMeshName, position, bVis, bPhysics, physicsShape, interact, physicsType)
		self.isOpen = False

	def OnInit(self, cbInfo):
		lel_common.GenericObject.OnInit(self, cbInfo)
		self.physical('').setConstraints( VRScript.Math.Vector(1,1,0), VRScript.Math.Vector(1,1,1) )
		
	def Rotate(self,x,y,z):
		# Rotates this door at the given degree.
		#m = self.movable().getPose()
		#m.postEuler(x,y,z)
		#self.movable().setPose(m)
		self.physical('').applyImpulse( VRScript.Math.Vector(5,5,0), VRScript.Math.Vector(.125,.125,0) )
		self.physical('').applyImpulse( VRScript.Math.Vector(-2,-2,0), VRScript.Math.Vector(-.125,-.125,0) )
	
	# Opens this door.
	def Open(self):
		print("Open door " + self.name)
		self.Rotate(90,0,0)
		self.isOpen = True

	# Closes this door.
	def Close(self):
		print("Close door " + self.name)
		self.Rotate(-90,0,0)
		self.isOpen = False
	
	# Toggle this door on left click.
	def OnButtonRelease(self, cbInfo, btInfo, user):
		print("Yo")
		if (btInfo.button == 5):
			if (self.isOpen):
				self.Close()
			else:
				self.Open()
