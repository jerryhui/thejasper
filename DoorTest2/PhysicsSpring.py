import VRScript
import math
import lel_common
from system import System
from mass import Mass
from springs import CylinderSpring, RubberSpring, DoubleHelixSpring, SingleHelixSpring

class PhysicsSpring(GenericObject):
	def __init__(self, sName, sMeshName, transform, bVis, bPhysics, physicsShape, interact, mass, tension, damping, length, second_tracker):
		GenericObject.__init__(self, sName, sMeshName, transform, bVis, bPhysics, physicsShape, interact)
		self.lastDir = VRScript.Math.Vector(0,0,0)
		self.rate = 30
		self.physicsSystem = None
		self.massTracker = None
		self.massObject = None
		self.init = False
		self.m = mass
		self.k = tension
		self.d = damping
		self.l = length
		self.tracker = second_tracker
		self.objectState = 2	#0 is tracked,1 is virtual lab, 2 is kinetics
		self.force = 0.0
		
	def OnInit(self, cbInfo):
		self.attach(VRScript.Core.Renderable(self.name, VRScript.Resources.Mesh(self.name, self.meshName)))
		self.renderable(self.name).setVisible(self.bVisible)

	# def OnUpdate(self, cbInfo):
		# if(self.tracker == True):
			# wand = VRScript.Core.Entity('User1Head')
		# else:
			# wand = VRScript.Core.Entity('User0Hand')
		
		# m = wand.movable().selfToWorld()
		# vTrans = VRScript.Math.Vector(m.getTranslation())
		# #vTrans = VRScript.Math.Vector(-4.5, -4.5, 1.5)
		
		# if(self.init == False):
			# self.physicsSystem = System(timestep=1./self.rate, gravity=9.84, viscosity=0.04)
			# self.massTracker = Mass(m=0.1, pos=(vTrans.x, vTrans.y, vTrans.z+0.1))
			# self.massTracker.fixed = 1
			# self.massObject = Mass(self.m, pos=(vTrans.x, vTrans.y, vTrans.z-0.1))
			# self.spring = CylinderSpring(self.massTracker, self.massObject, self.k, self.l, self.d) 
			# self.physicsSystem.insertMass(self.massTracker)
			# self.physicsSystem.insertMass(self.massObject)
			# self.physicsSystem.insertSpring(self.spring)
			# self.init = True
		
		# if(self.objectState == 2):
			# self.massTracker.pos = vTrans
			# #self.massObject.pos = vTrans
			# self.physicsSystem.step()
			# massObj = VRScript.Math.Matrix()
			# massObj.setTranslation(self.massObject.pos)
			# #print(str(self.massObject.pos.x))
			# #print(str(self.massObject.pos.y))
			# #print(str(self.massObject.pos.z))
			# self.movable().setPose(massObj)
		# elif(self.objectState == 1):
			# self.physical(self.name).setCollisionType(VRScript.Core.CollisionType.Dynamic)
		# elif(self.objectState == 0):
			# self.movable().setPose(m)