import VRScript
import lel_common
import HouseObjects
import Paranormal

# Represents the game engine of The Jasper.
class HauntedHouseEngine(lel_common.LELScenario):
	def __init__(self):
		lel_common.LELScenario.__init__(self)
		self.paranormals = []		#list of paranormals in this scene
		self.user = VRScript.Core.Entity('User0')
		
	# Add an object to this haunted house.
	# Inputs:
	#		obj - Object to add (should be of base type VRScript.Core.Behavior)
	def AddObject(self, obj):
		self.static_objects.append(obj)
		obj.parentScene = self
		return obj
		
	# Add a paranormal to this haunted house.
	# Inputs:
	#		p - Paranormal to add (should be of base type Paranormal.Paranormal)
	def AddParanormal(self, p):
		self.AddObject(p)
		self.paranormals.append(p)
		print("Added paranormal " + str(p) + " to this scene.")
		return p

	# Gets the total number of paranormals in this house.
	def ParanormalCount(self):
		return len(self.paranormals)

	# Gets the number of captured paranormals.
	def CapturedParanormalCount(self):
		cnt = 0
		for p in self.paranormals:
			if (p.IsCaptured()):
				cnt += 1
		return cnt
		
	# Moves the user.
	# Inputs:
	#	movement - 3-d array of motion [x,y,z]
	#	rotation - 3-d array of rotation [x,y,z]
	def MoveUser(self,movement,rotation):
		print("Move user around")
		m = self.user.movable().getPose()
		m.postEuler(rotation[1],rotation[2],rotation[3])
		m.preTranslation(VRScript.Math.Vector(movement[1],movement[2],movement[3]))
		self.user.movable().setPose(m)

# user = VRScript.Core.Entity('User0')

# scene.create_entity("DoorLeft", "models\\DoorLeft.osg", [-5.09199479842989,-4.40669061564667,-6.72643819712604e-018], True, True, "Concave", True, "Static")
# scene.set_physics_properties("DoorLeft", [1.0, 0.25, 0.9, 1, 0.5])
# scene.create_entity("DoorLeft_1", "models\\DoorLeft_1.osg", [-3.40250259842728,-4.42017033590422,-6.54019670039207e-018], True, True, "Concave", True, "Static")
# scene.set_physics_properties("DoorLeft_1", [1.0, 0.25, 0.9, 1, 0.5])
# scene.create_entity("ghost-man", "models\\ghost-man.osg", [-4.73176827151701,-7.42980466055885,3.38395973816167e-017], True, True, "Concave", True, "Static")
# scene.set_physics_properties("ghost-man", [1.0, 0.25, 0.9, 1, 0.5])

theJasper = HauntedHouseEngine()

# secondFloor = theJasper.create_entity("SecondFloor", "models\\Upstairs\\2f.osg", [-5,-14.40669061564667,-6.72643819712604e-018], True, True, "Concave", True, "Static")

doorL = theJasper.AddObject(HouseObjects.Door("DoorLeft", "models\\DoorLeft.osg", [-5.09199479842989,-4.40669061564667,-6.72643819712604e-018], True, -90))
theJasper.set_physics_properties("DoorLeft", [1.0, 0.25, 0.9, 1, 0.5])

doorR = theJasper.AddObject(HouseObjects.Door("DoorLeft_1", "models\\DoorLeft_1.osg", [-3.40250259842728,-4.42017033590422,-6.54019670039207e-018], True, 90))
theJasper.set_physics_properties("DoorLeft_1", [1.0, 0.25, 0.9, 1, 0.5])

ghostMan = theJasper.AddParanormal(Paranormal.Ghost("ghostMan", "models\\ghost-man.osg", [-4.73176827151701,-7.42980466055885,3.38395973816167e-017], "LOOK"))
# ghostMan.SetDiscoveredAnimation("jc-002-A.fbx")
# ghostMan.SetCapturedAnimation("jc-001.fbx")