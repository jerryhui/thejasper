# JasperEngine.py
# This contains the main game engine classes.
# 	class EnvObject(VRScript.Core.Behavior)
# 	class HauntedHouseEngine(lel_common.LELScenario)

import VRScript
import lel_common
import HouseObjects
import Paranormal
import Animation

User = VRScript.Core.Entity('User0')	# User entity, declared for global reference.

GroundObjects = ['simpleHouse']		# list of objects that shouldn't create collision events

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
		self.textAlpha = 1
		self.textStep = 0
		self.textHold = 1000
		
	# Initializes all stats.
	def OnInit(self,cbInfo):
		# create score text
		self.scoreText = VRScript.Core.FontText('Score', 'You have caught {0} out of {1} ghosts'.format(self.paranormalCaptured,self.paranormalTotal))
		self.scoreText.setColor(VRScript.Core.Color(1,1,0,self.textAlpha))
		self.scoreText.setHeight(.05)
		self.scoreText.show()
		self.attach(self.scoreText)

		# attach score text to user such that it is visible at all times
		self.movable().setParent('User0Head')
		m = self.movable().getPose()
		m.preTranslation(VRScript.Math.Vector(0, .75, .45))
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
		if (n < self.paranormalTotal):
			self.scoreText.setText('You have caught {0} out of {1} ghosts'.format(self.paranormalCaptured,self.paranormalTotal))
		else:
			self.scoreText.setText('Congratulations! You have caught all {0} ghosts'.format(self.paranormalTotal))
	
	# Add background music.
	# Inputs:
	#	file - path to music file
	def AddMusic(self,file):
		if (file not in self.bkgMusicFiles):
			self.bkgMusicFiles.append(file)
			# print("Added {0} to bkgMusic; total music count={1}".format(file, len(self.bkgMusicFiles)))
		# else:
			# print("DEBUG: music {0} not added".format(file))
	
	# Updates game stats. Perform rendering update ONLY when there's an actual change.
	def OnUpdate(self, cbInfo):
		# fade in/out text or hold
		if (self.textHold > 0):
			self.textHold -= 1
		elif (self.textHold ==0):
			self.textStep = -.001
		
		if (self.textStep != 0):
			self.textAlpha += self.textStep
			if (self.textStep>0 and self.textAlpha >= 0.9):
				self.textAlpha = 1
				self.textHold = 2500
				self.textStep = 0
				print("Stop fade in")
			elif (self.textStep<0 and self.textAlpha <= 0.1):
				self.textAlpha = 0
				self.textHold = -99
				self.textStep = 0
				print("Stop fade out")
			self.scoreText.setColor(VRScript.Core.Color(1,1,0,self.textAlpha))

		# check/update score text
		n = self.house.CapturedParanormalCount()
		if (n != self.paranormalCaptured):
			self.SetCaptured(n)
			print("Begin fade in text")
			self.textStep = 0.001
				
		# check/advance background music
		if (self.bkgMusicIndex < len(self.bkgMusic)):
			aud = self.bkgMusic[self.bkgMusicIndex].GetAudible()
			if (aud is None):
				aud = self.bkgMusic[self.bkgMusicIndex].MakeAudible()
				aud.SetGain(0.75)
			if (not aud.isPlaying()):
				self.bkgMusicIndex = (self.bkgMusicIndex+1) % len(self.bkgMusic)
				print("Advance bkgMusicIndex to " + str(self.bkgMusicIndex))
				# self.bkgMusic[self.bkgMusicIndex].play()
				self.bkgMusic[self.bkgMusicIndex].Play(True,1.025)
	
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
	
	def Factory(self, objName, coordArr, param1=None, param2=None):
		cnt = 0
		if (objName == "bottle"):
			# Wine bottle
			for coords in coordArr:
				self.AddObject(HouseObjects.BumpableObj("bottle{0}".format(cnt), "Furniture\\bottle.ive", coords,"bottle-roll.wav", [1.0, 0.8, 0.8, .8, 0.5]))
				cnt += 1
		if (objName == "door"):
			# Wooden door
			for coords in coordArr:
				door = self.AddObject(HouseObjects.Door("WoodenDoor{0}".format(cnt), "Furniture\\brDoor.ive", coords, True, -90))
				if (param1[cnt] != 0):
					door.SetPreEuler([param1[cnt],0,0])
				cnt += 1
	
	def CreateGround(self):
		ground = VRScript.Core.Behavior("GroundPlane")
		ground_plane = VRScript.Resources.Box(VRScript.Math.Vector(50,50,.25), VRScript.Math.Point(0,0,-.25))
		ground.attach(VRScript.Core.Renderable("GroundPlaneRender", ground_plane))
		
		p = VRScript.Core.Physical("GroundPlanePhysics",ground_plane)
		pprop = VRScript.Core.PhysicsProperties(0, .0, 1, 1, .5)
		p.setPhysicsProperties(pprop)
		p.setCollisionType(VRScript.Core.CollisionType.Static)
		ground.attach(p)
		ground.renderable('').show()
		ground.movable().setPose(VRScript.Math.Matrix())
		
		GroundObjects.extend(["GroundPlane"])
		print(GroundObjects)