import VRScript


# ------------------------- BALL ------------------------- #

class AnimationObject(VRScript.Core.Behavior):
	def __init__(self, entity=None):
		VRScript.Core.Behavior.__init__(self,entity)
		self.name = "Animation"

	def OnInit(self, info):
		self.attach(VRScript.Core.Interactible(self.name, self.renderable('')))
		self.interactible(self.name).enableGrab(False)
		self.interactible(self.name).enableSelection(True)
	def LoadAnimation(self, file):
		print("load animation:")
		print(file)
		
		mat = VRScript.Math.Matrix()
		mat.preScale(VRScript.Math.Vector(.1,.1,.1))
		mat.preAxisAngle(45,VRScript.Math.Vector(1,0,0))
		
		self.mesh = VRScript.Resources.Mesh(self.getName(), file, mat)
		self.attach(VRScript.Core.Renderable(self.getName(), self.mesh))
		self.renderable('').show()
		self.attach(VRScript.Core.Animable(self.getName(), self.mesh))
		
	def OnButtonRelease(self, cbInfo,btInfo, user):
		self.Play(VRScript.Core.PlayMode.Loop)
	def Play(self, mode):
		self.anim = VRScript.Core.AnimationStrip('Take 001', 0.0, 0.0, 0, mode)
		self.animable('').play(self.anim)
	def Stop(self):
		self.animable('').stop()

# ------------------------ SCENE ------------------------ #


	
a = AnimationObject("BUG")
a.LoadAnimation("Test.fbx")
#a.Play();
# a.Play(VRScript.Core.PlayMode.Stay);
#a.Stop();
# ------------------------- END ------------------------- #
