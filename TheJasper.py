import VRScript
import lel_common
import HouseObjects
import Paranormal
import Animation

# The Jasper - A Haunted House for CAVE
# Modeling: Jerry Chen, Natalie Flunker, Hasti Mirkia
# Program: Jerry Hui
#
# Created for DS501, Spring 2013


User = VRScript.Core.Entity('User0')	# User entity, declared for global reference.

# Represents game stats and any other information that needs constant updating in CAVE.
class EnvObject(VRScript.Core.Behavior):
	def __init__(self,house):
		VRScript.Core.Behavior.__init__(self, "EnvObject")
		self.paranormalTotal = 0		# total count of paranormals
		self.paranormalCaptured = 0		# number of captured paranormals
		self.house = house		# associated lel_scenario object
		self.bkgMusic = []		# list of background music objects
		self.bkgMusicFiles = []	# list of music files
		self.bkgMusicIndex = 0	# points to current background music
		self.name = "JasperEnvironment"
	
	# Initializes all stats.
	def OnInit(self,cbInfo):
		# User.physical('').enableProximity(True)	# enable proximity check on User0
	
		# create score text
		self.scoreText = VRScript.Core.FontText('Score', 'You have caught {0} out of {1} ghosts'.format(self.paranormalCaptured,self.paranormalTotal))
		self.scoreText.setColor(VRScript.Core.Color(1,1,0))
		self.scoreText.setHeight(.05)
		self.scoreText.show()
		self.attach(self.scoreText)
		
		self.movable().setParent('User0Head')
		m = self.movable().getPose()
		m.preTranslation(VRScript.Math.Vector(0, 1, 0.75))
		self.movable().setPose(m)
		
		# sets up background music
		for i in range(len(self.bkgMusicFiles)):
			# aud = VRScript.Core.Audible("{0}_bkg{1}".format(self.name,i),self.bkgMusicFiles[i])
			aud = Animation.AudioObj("{0}_bkg{1}".format(self.name,i),self.bkgMusicFiles[i])
			self.bkgMusic.append(aud)
			print(str(aud))
			self.attach(aud.MakeAudible())
		self.bkgMusicIndex = len(self.bkgMusic)-1	# always begin with track 1
		
	# Sets the number of total paranormals.
	# Input:
	#	n - Total number of paranormals
	def SetTotal(self, n):
		self.paranormalTotal = n
		
	# Sets caught count and updates text.
	# Input:
	#	n - Number of caught paranormals
	def SetCaptured(self, n):
		self.paranormalCaptured = n
		self.scoreText.setText('You have caught {0} out of {1} ghosts'.format(self.paranormalCaptured,self.paranormalTotal))
	
	# Add background music.
	# Inputs:
	#	file - path to music file
	def AddMusic(self,file):
		if (file not in self.bkgMusicFiles):
			self.bkgMusicFiles.append(file)
			print("Added {0} to bkgMusic; total music count={1}".format(file, len(self.bkgMusicFiles)))
		else:
			print("DEBUG: music {0} not added".format(file))
	
	# Updates game stats. Perform rendering update ONLY when there's an actual change.
	def OnUpdate(self, cbInfo):
		# check/update score text
		n = self.house.CapturedParanormalCount()
		if (n != self.paranormalCaptured):
			self.SetCaptured(n)
			
		# check/advance background music
		if (self.bkgMusicIndex < len(self.bkgMusic)):
			aud = self.bkgMusic[self.bkgMusicIndex].GetAudible()
			if (aud is None):
				aud = self.bkgMusic[self.bkgMusicIndex].MakeAudible()
			if (not aud.isPlaying()):
				self.bkgMusicIndex = (self.bkgMusicIndex+1) % len(self.bkgMusic)
				print("Advance bkgMusicIndex to " + str(self.bkgMusicIndex))
				# self.bkgMusic[self.bkgMusicIndex].play()
				self.bkgMusic[self.bkgMusicIndex].Play(True,1.05)

# Represents the game engine of The Jasper.
#	Paranormals[] paranormals - list of paranormals in this scene
#	user - User0 entity
#	bool showScore - whether to show the score in front of the user
#	string[] bkgMusic - list of background music files
class HauntedHouseEngine(lel_common.LELScenario):
	def __init__(self):
		lel_common.LELScenario.__init__(self)
		self.paranormals = []
		self.showScore = True
		self.env = EnvObject(self)
		
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
		self.env.SetTotal(len(self.paranormals))
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
		m = User.movable().getPose()
		m.postEuler(rotation[1],rotation[2],rotation[3])
		m.preTranslation(VRScript.Math.Vector(movement[1],movement[2],movement[3]))
		User.movable().setPose(m)
	
	# Displays score in front of user.
	def ShowScore(self):
		pass
	
	# Add background music.
	# Inputs:
	#	file - path to music file
	def AddMusic(self,file):
		print("DEBUG: HauntedHouse.AddMusic()")
		self.env.AddMusic(file)

		
#------------------------------------------------------------------------------		

theJasper = HauntedHouseEngine()

theJasper.create_entity("fullHouse", "Models\\bigHouse.ive", [-5.09199479842989,-4.40669061564667,-6.72643819712604e-018], True, False, "Concave", False, "Static")
theJasper.create_ground_plane()


# doorL = theJasper.AddObject(HouseObjects.Door("DoorLeft", "models\\DoorLeft.osg", [-5.09199479842989,-4.40669061564667,-6.72643819712604e-018], True, -90))
# theJasper.set_physics_properties("DoorLeft", [1.0, 0.25, 0.9, 1, 0.5])

# doorR = theJasper.AddObject(HouseObjects.Door("DoorLeft_1", "models\\DoorLeft_1.osg", [-3.40250259842728,-4.42017033590422,-6.54019670039207e-018], True, 90))
# theJasper.set_physics_properties("DoorLeft_1", [1.0, 0.25, 0.9, 1, 0.5])

# boxMonster = theJasper.AddParanormal(Paranormal.Paranormal("boxMonster", "models\\boxmon.osg", [1,1,0], "TOUCH"))

# ghostMan = theJasper.AddParanormal(Paranormal.Ghost("ghostMan", "models\\ghost-man.osg", [0,0,0], "LOOK"))
# ghostMan.SetDiscoveredAnimation("001-01start.fbx", VRScript.Core.PlayMode.Loop, [90,0,0], VRScript.Math.Vector(0.01,0.01,0.01))
# ghostMan.SetCapturedAnimation("jc-001.fbx")

theJasper.AddMusic("lux.wav")