import VRScript
import lel_common
import HouseObjects
import Paranormal

user = VRScript.Core.Entity('User0')

# Represents score of current game.
class ScoreObject(VRScript.Core.Behavior):
	def __init__(self):
		VRScript.Core.Behavior.__init__(self, "EnvObject")
	
	def OnInit(self,cbInfo):
		# create score object
		ft = VRScript.Core.FontText("Score", "0/0")
		ft.show()
		self.attach(ft)
		# r = VRScript.Core.Renderable("Score", ft)
		# r.show()
		bowlingball = VRScript.Resources.Sphere(0.25)
		renderable = VRScript.Core.Renderable(self.getName(), bowlingball)
		renderable.show()
		self.attach(renderable)
		
	def OnUpdate(self,cbInfo):
		m = user.movable().getPose()
		m.postTranslation(VRScript.Math.Vector(-4,2,5))
		self.movable().setPose(m)

# Represents the game engine of The Jasper.
#	Paranormals[] paranormals - list of paranormals in this scene
#	user - User0 entity
#	bool showScore - whether to show the score in front of the user
class HauntedHouseEngine(lel_common.LELScenario):
	def __init__(self):
		lel_common.LELScenario.__init__(self)
		self.paranormals = []
		self.showScore = True
		self.env = ScoreObject()
		
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
		m = user.movable().getPose()
		m.postEuler(rotation[1],rotation[2],rotation[3])
		m.preTranslation(VRScript.Math.Vector(movement[1],movement[2],movement[3]))
		user.movable().setPose(m)
	
	# Displays score in front of user.
	def ShowScore(self):
		pass

theJasper = HauntedHouseEngine()

# secondFloor = theJasper.create_entity("SecondFloor", "models\\Upstairs\\2f.osg", [-5,-14.40669061564667,-6.72643819712604e-018], True, True, "Concave", True, "Static")

doorL = theJasper.AddObject(HouseObjects.Door("DoorLeft", "models\\DoorLeft.osg", [-5.09199479842989,-4.40669061564667,-6.72643819712604e-018], True, -90))
theJasper.set_physics_properties("DoorLeft", [1.0, 0.25, 0.9, 1, 0.5])

doorR = theJasper.AddObject(HouseObjects.Door("DoorLeft_1", "models\\DoorLeft_1.osg", [-3.40250259842728,-4.42017033590422,-6.54019670039207e-018], True, 90))
theJasper.set_physics_properties("DoorLeft_1", [1.0, 0.25, 0.9, 1, 0.5])

ghostMan = theJasper.AddParanormal(Paranormal.Ghost("ghostMan", "001-01start.fbx", [0,0,0], "LOOK", ParanormalState.Discovered))
ghostMan.SetDiscoveredAnimation("001-01start.fbx", VRScript.Core.PlayMode.Loop, [90,0,0], VRScript.Math.Vector(0.01,0.01,0.01))
# ghostMan.SetCapturedAnimation("jc-001.fbx")