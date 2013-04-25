import VRScript
import lel_common
import HouseObjects
import Paranormal

# Represents the game engine of The Jasper.
class HauntedHouseEngine(lel_common.LELScenario):
	def __init__(self):
		lel_common.LELScenario.__init__(self)
		self.paranormals = []		#list of paranormals in this scene
		
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
		print("Added paranormal " + p + " to this scene.")

	# Gets the total number of paranormals in this house.
	def ParanormalCount(self):
		return len(self.paranormals)

	# Gets the number of captured paranormals.
	def CapturedParanormalCount(self):
		cnt = 0
		for p in paranormals
			if (p.IsCaptured()):
				cnt += 1
		return cnt

# user = VRScript.Core.Entity('User0')

# scene.create_entity("DoorLeft", "models\\DoorLeft.osg", [-5.09199479842989,-4.40669061564667,-6.72643819712604e-018], True, True, "Concave", True, "Static")
# scene.set_physics_properties("DoorLeft", [1.0, 0.25, 0.9, 1, 0.5])
# scene.create_entity("DoorLeft_1", "models\\DoorLeft_1.osg", [-3.40250259842728,-4.42017033590422,-6.54019670039207e-018], True, True, "Concave", True, "Static")
# scene.set_physics_properties("DoorLeft_1", [1.0, 0.25, 0.9, 1, 0.5])
# scene.create_entity("ghost-man", "models\\ghost-man.osg", [-4.73176827151701,-7.42980466055885,3.38395973816167e-017], True, True, "Concave", True, "Static")
# scene.set_physics_properties("ghost-man", [1.0, 0.25, 0.9, 1, 0.5])

doorL = HouseObjects.Door("DoorLeft", "models\\DoorLeft.osg", [-5.09199479842989,-4.40669061564667,-6.72643819712604e-018], True, -90)
#scene.set_physics_properties("DoorLeft", [1.0, 0.25, 0.9, 1, 0.5])

doorR = HouseObjects.Door("DoorLeft_1", "models\\DoorLeft_1.osg", [-3.40250259842728,-4.42017033590422,-6.54019670039207e-018], True, 90)
#scene.set_physics_properties("DoorLeft_1", [1.0, 0.25, 0.9, 1, 0.5])

ghostMan = Paranormal.Paranormal("ghostMan", "models\\ghost-man.osg", [-4.73176827151701,-7.42980466055885,3.38395973816167e-017], "LOOK")