import VRScript

# Represents metadata for an animation that will be loaded later.
#	name - human readable name for animation
#	file - path to FBX
#	VRScript.Core.PlayMode playMode - mode of animation playback
#	VRScript.Math.Vector preScale - scale animation before loading
#	[int,int,int] preAngles - rotate animation before laoding
class AnimationMeta:
	def __init__(self, name, file, playMode=VRScript.Core.PlayMode.Loop, preAngles=[0,0,0], preScale=VRScript.Math.Vector(1,1,1)):
		self.name = name
		self.file = file
		self.playMode=playMode
		self.preScale = preScale
		self.preAngles = preAngles
	def getName(self):
		return self.name
	def __str__(self):
		return self.name

# Represents an animation that can be played.
class AnimationObject(VRScript.Core.Behavior):
	# class AnimationObject(VRScript.Core.Behavior):
	def __init__(self, name):
		VRScript.Core.Behavior.__init__(self,name)
	
	# 
	# 	def OnInit(self, info):
	# 		self.attach(VRScript.Core.Interactible(self.name, self.renderable('')))
	# 		self.interactible(self.name).enableGrab(False)
	# 		self.interactible(self.name).enableSelection(True)		
	
	def LoadAnimMeta(self, meta):
		self.LoadAnimation(meta.file, meta.preScale, meta.preAngles)
	
	# Load an animation file.
	# Inputs:
	#		file - file name (FBX file; in FBX 2009 or earlier)
	#		preAngle - degree to rotate this animation before showing
	#		VRScript.Math.Vector preScale - scale this animation before showing
	def LoadAnimation(self, file, preAngles=[0,0,0], preScale=VRScript.Math.Vector(1,1,1)):
		print("load animation: " +file)
		
		mat = VRScript.Math.Matrix()
		mat.preScale(preScale)

		v = [VRScript.Math.Vector(1,0,0),VRScript.Math.Vector(0,1,0),VRScript.Math.Vector(0,0,1)]
		for i in range(len(preAngles)):
			a = preAngles[i]
			if (a!=0):
				mat.preAxisAngle(a, v[i])
					
		self.mesh = VRScript.Resources.Mesh(self.getName(), file, mat)
		self.attach(VRScript.Core.Renderable(self.getName(), self.mesh))
		self.renderable('').show()
		self.attach(VRScript.Core.Animable(self.getName(), self.mesh))
	
	# Move this animation to the given Matrix.
	# Input:
	#		VRScript.Math.Matrix m - destination pose matrix
	def SetPosition(self, m):
		print ("set position")
		self.movable().setPose(m)
	
	# Play the animation.
	#	Inputs:
	#		VRScript.Core.PlayMode mode - mode of playback
	def Play(self, mode=VRScript.Core.PlayMode.Once):
		self.anim = VRScript.Core.AnimationStrip('Take 001', 0.0, 0.0, 0, mode)
		self.animable('').play(self.anim)
		
	def Stop(self):
		self.animable('').stop()
