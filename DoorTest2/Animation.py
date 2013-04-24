import VRScript

# Represents an animation that can be played.
class AnimationObject(VRScript.Core.Behavior):
	# class AnimationObject(VRScript.Core.Behavior):
	# 	def __init__(self, entity=None):
	# 		VRScript.Core.Behavior.__init__(self,entity)
	# 		self.name = "Animation"
	# 
	# 	def OnInit(self, info):
	# 		self.attach(VRScript.Core.Interactible(self.name, self.renderable('')))
	# 		self.interactible(self.name).enableGrab(False)
	# 		self.interactible(self.name).enableSelection(True)		
	
	# Load an animation file.
	# Inputs:
	#		file - file name (FBX file; in FBX 2009 or earlier)
	#		VRScript.Math.Vector preScale - scale this animation before showing
	#		preAngle - degree to rotate this animation before showing
	#		VRScript.Math.Vector preAxis - axis to rotate this animation before showing
	def LoadAnimation(self, file, preScale=VRScript.Math.Vector(1,1,1), preAngle=0, preAxis=VRScript.Math.Vector(1,0,0)):
		print("load animation:")
		print(file)
		
		mat = VRScript.Math.Matrix()
		mat.preScale(preScale)
		mat.preAxisAngle(preAngle,preAxis)
		
		self.mesh = VRScript.Resources.Mesh(self.getName(), file, mat)
		self.attach(VRScript.Core.Renderable(self.getName(), self.mesh))
		self.renderable('').show()
		self.attach(VRScript.Core.Animable(self.getName(), self.mesh))
	
	# Move this animation to the given Matrix.
	# Input:
	#		VRScript.Math.Matrix m - destination pose matrix
	def SetPosition(self, m):
		set.movable().setPose(m)
	
	# Play the animation.
	#	Inputs:
	#		VRScript.Core.PlayMode mode - mode of playback
	def Play(self, mode):
		self.anim = VRScript.Core.AnimationStrip('Take 001', 0.0, 0.0, 0, mode)
		self.animable('').play(self.anim)
		
	def Stop(self):
		self.animable('').stop()