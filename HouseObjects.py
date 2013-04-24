import VRScript
import lel_common

# Author: Jerry Hui
# Created: 4/19/2013

# Represents a door in The Jasper Hotel.
class Door(lel_common.GenericObject):
	def __init__(self, sName, sMeshName, position, bVis, bPhysics, physicsShape, interact, physicsType):
		lel_common.GenericObject.__init__(self, sName, sMeshName, position, bVis, bPhysics, physicsShape, interact, physicsType)
		self.isOpen = False
		self.motionState = 0	# 0=no motion; >0=open; <0=close

	def OnInit(self, cbInfo):
		lel_common.GenericObject.OnInit(self, cbInfo)
		self.physical('').setConstraints(VRScript.Math.Vector(1,1,0), VRScript.Math.Vector(1,1,1))
		
	def OnUpdate(self, cbInfo):
		if (self.motionState == 0): # no motion
			return
		
		if (self.motionState > 0): # opening
			self.Rotate(1,0,0)
			self.motionState -= 1
			return
		
		if (self.motionState < 0): # closing
			self.Rotate(-1,0,0)
			self.motionState += 1
			return
		
	def Rotate(self,x,y,z):
		# Rotates this door at the given degree.
		m = self.movable().getPose()
		m.postEuler(x,y,z)
		self.movable().setPose(m)
		
		# below is an attempt to make door open/close by physics engine; do when there's extra time
		# self.physical('').applyImpulse(VRScript.Math.Vector(5,5,0), VRScript.Math.Vector(.125,.125,0))
		# self.physical('').applyImpulse(VRScript.Math.Vector(-2,-2,0), VRScript.Math.Vector(-.125,-.125,0))
	
	# Opens this door.
	def Open(self):
		if (self.isOpen):
			return
		print("Open door " + self.name)
		if (self.motionState==0):
			self.motionState = 1
		elif (self.motionState<0):	# door is currently closing; flip direction
			self.motionState += 90
		self.isOpen = True

	# Closes this door.
	def Close(self):
		if (self.isClose):
			return
		print("Close door " + self.name)
		if (self.motionState==0):
			self.motionState = -90
		elif (self.motionState>0):	# door is currently opening; flip direction
			self.motionState -= 90
		self.isOpen = False
	
	# Toggle this door on left click.
	def OnButtonRelease(self, cbInfo, btInfo, user):
		print("Yo")
		if (btInfo.button == 5):
			if (self.isOpen):
				self.Close()
			else:
				self.Open()
