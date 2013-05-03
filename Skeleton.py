import VRScript
import math
import Util as util

class Joint(VRScript.Core.Behavior):
	def __init__(self, entity=None):
		VRScript.Core.Behavior.__init__(self,entity)
		self.jointsize = 0.025
		
	def OnInit(self, info):
		print('r_'+self.getName())
		#if self.getName() == 'kinectSkeleton_Hand_L' or self.getName() == 'kinectSkeleton_Hand_R':
		renderable = VRScript.Core.Renderable('r_'+self.getName(),VRScript.Resources.Sphere(self.jointsize))
		#else:
			# if(self.getName() == 'kinectSkeleton_Hand_L'):
				# wand2 = VRScript.Core.Entity('User1Hand')
				# renderable = wand.renderable('User1Hand')
			# else:
				# wand = VRScript.Core.Entity('User0Hand')
				# renderable = wand.renderable('User0Hand')
				
		#renderable = VRScript.Core.Renderable('r_'+self.getName(),VRScript.Resources.Cylinder(0.02, 0.03))
		matprops = VRScript.Core.MaterialProperties(util.red,util.red,util.white,util.red,1.0,1.0,1,True)
		renderable.setMaterialProperties(matprops)
		#renderable.show()
		self.attach(renderable)
		
		# if self.getName() == 'kinectSkeleton_Foot_L' or self.getName() == 'kinectSkeleton_Foot_R':
			# physical = VRScript.Core.Physical(self.getName(), VRScript.Resources.Sphere(self.jointsize))
			# #physprops = VRScript.Core.PhysicsProperties(1,0,0,0,0)
			# physical.setPhysicsProperties(util.phys_light)
			# physical.setCollisionType(VRScript.Core.CollisionType.Dynamic)
			# physical.enableDebugVisual(True)
			# self.attach(physical)
	
	# def OnUpdate(self, info):
		# if self.getName() == 'kinectSkeleton_Foot_L' or self.getName() == 'kinectSkeleton_Foot_R':
			# physical = VRScript.Core.Physical(self.getName(), VRScript.Resources.Sphere(self.jointsize))
			# physical.setPhysicsProperties(util.phys_light)
			# #physical.setConstraints(VRScript.Math.Vector(1,1,1),VRScript.Math.Vector(1,1,1))
			# physical.setCollisionType(VRScript.Core.CollisionType.Dynamic)
			# self.attach(physical)
		
	def setPosition(self, vect):
		mat = self.movable().getPose()
		mat.makeTranslation(vect)
		self.movable().setPose(mat)
		
class Skeleton(VRScript.Core.Behavior):
	user = VRScript.Core.Entity('User0')
	user_head = VRScript.Core.Entity('User0Head')
	user_hand = VRScript.Core.Entity('User0Hand')
	correction_quat = VRScript.Math.Quat()
	prevState = False
	R2D = 57.29578 
	HIP_CENTER = 0
	SPINE = 1
	SHOULDER_CENTER = 2
	HEAD = 3
	SHOULDER_L = 4
	ELBOW_L = 5
	WRIST_L = 6
	HAND_L = 7
	SHOULDER_R = 8
	ELBOW_R = 9
	WRIST_R = 10
	HAND_R  = 11
	HIP_L   = 12
	KNEE_L = 13
	ANKLE_L = 14
	FOOT_L = 15
	HIP_R = 16
	KNEE_R = 17
	ANKLE_R = 18
	FOOT_R = 19
	NUM_JOINTS = 20
	joint_names = {HIP_CENTER:'Hip_Center',SPINE:'Spine',SHOULDER_CENTER:'Shoulder_Center',HEAD:'Head',
					SHOULDER_L:'Shoulder_L',ELBOW_L:'Elbow_L',WRIST_L:'Wrist_L',HAND_L:'Hand_L',
					SHOULDER_R:'Shoulder_R',ELBOW_R:'Elbow_R',WRIST_R:'Wrist_R',HAND_R:'Hand_R',
					HIP_L:'Hip_L',KNEE_L:'Knee_L',ANKLE_L:'Ankle_L',FOOT_L:'Foot_L',
					HIP_R:'Hip_R',KNEE_R:'Knee_R',ANKLE_R:'Ankle_R',FOOT_R:'Foot_R'}
					
	def __init__(self,entity=None, recvData = False, tcp_ip = None, tcp_port = None, num_floats = None):
		VRScript.Core.Behavior.__init__(self,entity)
		self.joints = list()
		self.receiveData = recvData
		self.connected = False
		self.corrected = False
		
		for i in range(0,20):
			j = Joint(self.getName()+"_"+Skeleton.joint_names[i])
			self.joints.append(j)

		self.data = list()
		self.vData = list()	#data converted to VRScript vectors
			
	def SetJointData(self, dataList):
		#print(str(len(dataList)))
		#better way to move the tuple to the list than this?
		self.data = list()
		i = 1
		while(i < 61):
			self.data.append(dataList[i])
			i=i+1
		
	def OnInit(self, info):
		print("init skel")
	
	def GetHandCenter(self):
		handR = self.GetJointPosition(Skeleton.HAND_R)
		handL = self.GetJointPosition(Skeleton.HAND_L)
		#print(handR.x, handR.y, handR.z)
		#print(handL.x, handL.y, handL.z)
		return ((handR + handL) * 0.5)
	
	def GetHandDistance(self):
		handR = self.GetJointPosition(Skeleton.HAND_R)
		handL = self.GetJointPosition(Skeleton.HAND_L)
		vec = handR - handL
		return vec.length()
		
	def GetJointPosition(self, jointIndex):
		#todo: bounds check
		return self.joints[jointIndex].movable().selfToWorld().getTranslation()
		
	def VectorFromTo(self, indexFrom, indexTo):
		fromJoint = self.joints[indexFrom].movable().selfToWorld().getTranslation()
		toJoint = self.joints[indexTo].movable().selfToWorld().getTranslation()
		vec = toJoint-fromJoint
		vec = vec.normalize()
		return vec
		
	def AngleBetween(self, indexMiddle, indexTo, indexTo2):
		vec1 = self.VectorFromTo(indexMiddle, indexTo)
		vec2 = self.VectorFromTo(indexMiddle, indexTo2)
		dotAngle = vec1.dot(vec2)
		angle = math.degrees(math.acos(dotAngle))
		return angle
		
	def LeftRayCast(self):
		return self.VectorFromTo(Skeleton.SHOULDER_L, Skeleton.WRIST_L)
		
	def RightRayCast(self):
		return self.VectorFromTo(Skeleton.SHOULDER_R, Skeleton.WRIST_R)
		
	def UpdateSkeleton(self, info):
		user_pos = self.user_head.movable().selfToWorld().getTranslation()
		user_rot = self.user.movable().selfToWorld().getQuat()
		#debug
		#user_pos.x += -5.25529762045281
		#user_pos.y += -5.17094851606241
		#print(self.user_head.movable().selfToWorld().toString())
		#data = kinectInfo.data
		#print(self.data[1])
		#print(str(len(self.data)))
		#if(len(self.data) > 0):
		self.vData = util.listToVectors(self.data, Skeleton.NUM_JOINTS)
		headpos = self.vData[Skeleton.HEAD]
		#handpos = self.vData[Skeleton.HAND_R]
		#print(handpos.x, handpos.y, handpos.z)
		#user_handpos = self.user_hand.movable().selfToWorld().getTranslation()
		
		#check for button4 to set correction quat
		#if (VRScript.Util.getControllerState()['button'][0]):
		if(self.corrected == False and self.data[0] != 0):
			#this is rotating the skeleton so it's z-up instead of y-up (which is what kinect sends over)
			print("corrected")
			shoulderpos = self.vData[Skeleton.SHOULDER_CENTER]
			hippos = self.vData[Skeleton.HIP_CENTER]
			BodyToHead = shoulderpos-hippos
			BodyToHead.normalize()
			dot = BodyToHead.dot(VRScript.Math.Vector(0,0,1))
			angle = -math.acos(dot)*Skeleton.R2D
			print(angle)
			mat = VRScript.Math.Matrix()
			mat.makeEuler(0,angle, 0)
			#mat.makeEuler(0,-7.0, 0)
			self.correction_quat = mat.getQuat()
			self.corrected = True
			print(self.correction_quat.x, self.correction_quat.y, self.correction_quat.z, self.correction_quat.w)
		
		#print(data)
		 # for j in self.joints:
			 # jpos = j.movable().getPose().getTranslation()
			 # print(j.getName(),jpos.x,jpos.y,jpos.z)
			# j.setPosition(VRScript.Math.Vector())
			
		#9/26/12 - below was uncommented before
		#relativeJoints = list()
		
		for i in range(0, Skeleton.NUM_JOINTS):
		#for i in range(10, 12):
			#print(data[i].x,data[i].y,data[i].z)
			joint = self.joints[i]
			prevpos = joint.movable().getPose().getTranslation()
			jointpos = self.vData[i]
			
			headrelativepos = jointpos - headpos
			#v = headrelativepos.normalize()
			v = jointpos
			q = user_rot * self.correction_quat
			headrelativepos = q.rotate(headrelativepos)
			headrelativepos += user_pos
			
			#headrelativepos.y += 1
			if i != Skeleton.HEAD:
				headrelativepos.z += 0.15
				
			#q2 = VRScript.Math.Quat(headrelativepos.x,headrelativepos.y,headrelativepos.z)
			#mat = VRScript.Math.Matrix().makeQuat(q2)
			#v = mat.getEuler()
				
			#if i == HAND_R:
			#	print(headrelativepos.x,headrelativepos.y,headrelativepos.z,user_handpos.x,user_handpos.y,user_handpos.z)
			joint.setPosition(headrelativepos)
			#relativeJoints.append(headrelativepos.x)
			#relativeJoints.append(headrelativepos.y)
			#relativeJoints.append(headrelativepos.z)
			
			#9/26/12 - below was uncommented before for training..
			#relativeJoints.append(v.x)
			#relativeJoints.append(v.y)
			#relativeJoints.append(v.z)
			
			#if i == Skeleton.HAND_R or i == Skeleton.HAND_L:
			#	print(v.x,v.y,v.z)
			
			#if joint.getName() == self.getName()+'_Hand_L' or joint.getName() == self.getName()+'_Hand_R':
			#impulse = headrelativepos - prevpos
			#joint.physical('').applyImpulse(impulse,VRScript.Math.Vector())
			#self.joints[i].setPosition(VRScript.Math.Vector(vData[i].x+user_pos.x,vData[i].y+user_pos.y,vData[i].z+user_pos.z))
			#self.joints[i].setPosition(VRScript.Math.Vector(vData[i].x,vData[i].y,vData[i].z))
		
			if False:#training:
				if svmData.fileOpen:
					cntr = VRScript.Util.getControllerState()
					if cntr['button'][1] and self.prevState == False:
						svmData.nextLabel()
					if cntr['button'][2]:
						svmData.closeFile()
					
					svmData.writeToFile(relativeJoints)
					self.prevState = cntr['button'][1]
		
	#def OnUpdate(self, info):
		#print("Update")
		#print(self.user_head.movable().selfToWorld().toString())
		#if self.receiveData:
		#	self.CalculateElbowWristAngle(info)
		#else:
			#self.UpdateSkeleton(info)