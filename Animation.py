# Animation.py
# Contains classes that handle audio and animations.
#	class AudioObj(VRScript.Core.Behavior)
#	class AnimationMeta
#	class AnimationObject(VRScript.Core.Behavior)

import VRScript
import JasperConfig
import JasperEngine

# Represents an audio.
# Remarks: 
#	This is a wrapper class that enhances audio functionality in VRScript. It 
#	provides delayed loading (load when requested), fading, and distance-fade.
class AudioObj(VRScript.Core.Behavior):
	def __init__(self, name, file, loop=False, parent=None):
		VRScript.Core.Behavior.__init__(self,name)
		self.name = name
		self.file = ""
		self.SetFile(file)
		self.loop = loop
		self.audible = None
		self.fadingDir = 0		# >0: fade in; <0: fade out
		self.fadingCur = 1
		self.parent = parent
		self.dist = 0
		self.curGain = 1
		if (parent is not None):
			print("Parent for this sound set to " + str(parent))
		
	def __str__(self):
		return self.name
	
	# Sets the audio file.
	# Inputs:
	#	file - path and name of audio file
	#	prefix (OPT) - prefix to file path (default=JasperConfig.MusicDir)
	def SetFile(self, file, prefix=JasperConfig.MusicDir):
		self.file = prefix + file
	
	# Attaches this AudioObj to an object in the scene for distance decay.
	# Input:
	#	parent - parent object from which this sound eminates
	def SetParent(self,parent):
		self.parent = parent
	
	# Creates a new instance of Audible.
	# Input:
	#	namePrefix - a prefix to add in front of this Audible's name
	# Output:
	#	VRScript.Core.Audible
	def MakeAudible(self,namePrefix=""):
		aud = VRScript.Core.Audible(namePrefix+self.name, self.file)
		audioProp = aud.getAudioProperties()
		audioProp.loop = self.loop
		aud.setAudioProperties(audioProp)
		if (self.parent is not None):
			m = self.parent.movable().getPose()
			self.movable().setPose(m)
			print("MakeAudible() - set parent to " + str(self.parent.getName()))
		# else:
		self.audible = aud
		return aud
	
	# Returns the current instance of Audible.
	# Output:
	#	VRScript.Core.Audible; None if it hasn't been created
	def GetAudible(self):
		return self.audible
	
	# Plays this sound, with optional fade in.
	# Inputs:
	#	bool fadeIn (OPT) - True is fade in should be used; default = False
	#	float fadeInStep(OPT) - step to fade in
	def Play(self,fadeIn=False,fadeInStep=1.1):
		aud = self.GetAudible()
		if (aud is None): aud = self.MakeAudible()
		if (fadeIn):
			self.FadeIn(fadeInStep)
		if (not aud.isPlaying()):
			aud.play()

	# Stops this sound, with optional fade out.
	# Inputs:
	#	bool fadeOut (OPT) - True is fade out should be used; default = False
	#	float fadeOutStep(OPT) - step to fade out
	def Stop(self,fadeOut=False,fadeOutStep=-0.95):
		aud = self.GetAudible()
		if (aud is None): return
		if (fadeOut):
			self.FadeOut(fadeOutStep)
		else:
			aud.stop()

	# Sets the gain of playback.
	# Input:
	#	float g (OPT) - output gain
	def SetGain(self,g):
		if (g != self.curGain):
			aud = self.GetAudible()
			if (aud is None): return
			audioProp = aud.getAudioProperties()
			audioProp.gain = g
			aud.setAudioProperties(audioProp)
			self.curGain = g
	
	# Begins fading in this sound.
	# Note: Audible must already be playing; best call through Play()
	# Input:
	#	step(OPT) - factor to bump up per frame; default = 1.1
	def FadeIn(self,step=1.1):
		if (step>1 and step<2):
			self.fadingDir = step
		else:
			self.fadingDir = 1.1
		self.fadingCur = 0.1
		print("Begin fade in " + self.name)

	# Begins fading out this sound.
	# Input:
	#	step(OPT) - factor to bump down per frame; default = -0.95
	def FadeOut(self,step=-0.95):
		if (step<0 and step>-1):
			self.fadingDir = step
		else:
			self.fadingDir = -0.95
		self.fadingCur = 1
		print("Begin fade out " + self.name)
	
	def OnUpdate(self,cbInfo):
		totalGain = 1
	
		if (self.fadingDir < 0):
			# fade out
			totalGain = self.fadingCur
			self.fadingCur *= (self.fadingDir*-1)
			if (self.fadingCur < 0.01):
				# fade out finished
				self.fadingDir = 0
				self.fadingCur = 1
				self.GetAudible().stop()
				return
		elif (self.fadingDir > 0):
			# fade in
			totalGain = self.fadingCur
			self.fadingCur *= self.fadingDir
			if (self.fadingCur > 0.95):
				# fade in finished
				self.fadingDir = 0
				self.fadingCur = 1
				self.SetGain(1)
				return
				
		# adjust volume according to distance from user0
		aud = self.GetAudible()
		if (aud is not None):
			if (aud.isPlaying()):
				if (self.parent is not None):
					m = self.parent.movable().getPose()					
					uv = JasperEngine.User.movable().getPose().getTranslation()
					sv = m.getTranslation()
					d = uv-sv
					dist = int(d.length())
					
					if (dist != 0):
						if (dist > 30):
							totalGain *= (1/(dist-29))
						elif (dist > 50):
							totalGain = 0

					if (dist != self.dist):
						self.dist = dist
						# print ("{0} dist={1}, gain->{2}".format(self,str(dist),totalGain))
						
		self.SetGain(totalGain)
		

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
