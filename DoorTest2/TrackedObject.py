import VRScript
import math
import struct
from struct import *
import socket
import ctypes
import threading
from lel_common import GenericObject

class NetworkThread(threading.Thread):
	def __init__(self, tcp_ip=None, tcp_port=None, num_floats=None):
		threading.Thread.__init__(self)
		if tcp_ip is None:         tcp_ip = '127.0.0.1'
		if tcp_port is None:     tcp_port = 19950
		if num_floats is None: num_floats = 4
		self.tcp_ip = tcp_ip
		self.tcp_port = tcp_port
		self.num_floats = num_floats
		print("Networking thread init for " + self.tcp_ip + ":" + str(self.tcp_port) + ", expecting " + str(self.num_floats) + " floats.")
		self.connected = False
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.tcp_ip, self.tcp_port))
		self.connected = True
		self.data = list()
		self.networkStruct = struct.Struct('f f f f f f f f f f f f f f c c c c')
		self.networkBuffer = ctypes.create_string_buffer(self.networkStruct.size)
		self.currThreshold = list()
		self.currInfo = list()
		self.currRegression = list()
		self.threshDone = False
		self.stopHandled = True
		self.fatigueReady = False
		self.objectStatus = '0'
		
	def run(self):
		while(True):
			self.ReceiveNetworkData()

	def GetData(self):
		return self.data
	
	def IsConnected(self):
		return self.connected
	
	def IsStopNotHandled(self):
		return (self.stopHandled == False)
		
	def SetStopHandled(self, bStop):
		self.stopHandled = bStop
		
	def GetInfo(self):
		return self.currInfo
		
	def HasInfo(self):
		return len(self.currInfo) > 0
		
	def ClearInfo(self):
		self.currInfo = list()
	
	def GetRegression(self):
		return self.currRegression
		
	def HasRegression(self):
		return (self.threshDone == True)
		#return len(self.currRegression) == 32
	
	def ClearRegression(self):
		self.threshDone = False
		self.currRegression = list()
		
	def GetThreshold(self):
		return self.currThreshold

	def HasThreshold(self):
		return len(self.currThreshold) > 0
		
	def ClearThreshold(self):
		self.currThreshold = list()
	
	def SetObjectStatus(self, status):
		self.objectStatus = status
	
	def IsFatigueReady(self):
		return self.fatigueReady
	
	def ClearFatigueReady(self):
		self.fatigueReady = False
		
	def Acknowledge(self, bSendTracking=False):
		#send a single char back to the laptop so we know what state the cave scenario is in
		#send the tracking data as well back to the laptop
		char = self.objectStatus.encode('ascii')
			
		if(bSendTracking == True):
			firstTracker = VRScript.Core.Entity('User0Head')
			m = firstTracker.movable().selfToWorld()
			mTrans = m.getTranslation()
			qRot = m.getQuat()
			secondTracker = VRScript.Core.Entity('User1Head')
			m2 = secondTracker.movable().selfToWorld()
			m2Trans = m2.getTranslation()
			q2Rot = m2.getQuat()
			
			#print(str(self.objectStatus))
			values = (mTrans.x, mTrans.y, mTrans.z, m2Trans.x, m2Trans.y, m2Trans.z, qRot.x, qRot.y, qRot.z, qRot.w, q2Rot.x, q2Rot.y, q2Rot.z, q2Rot.w, char, char, char, char)
			self.networkStruct.pack_into(self.networkBuffer, 0, *values)
			self.s.send(self.networkBuffer)
		else:
			self.s.send(char)

	def ReceiveNetworkData(self):
		BUFFER_SIZE = 4 * self.num_floats
		#msgStr = msg.decode('utf-8')	#old code to convert a network string to usable python string
		#msgStr = msgStr.rstrip('\0')
		bIsData = False
		buff = self.s.recv(BUFFER_SIZE)
		if not buff: self.connected = False
		self.data = unpack('f'*self.num_floats, buff)
		#if DEBUG: print(self.data)
		#print(self.data)
		if(self.data[0] == 1.0):
			bIsData = True
		if(self.data[0] == 3.0):
			self.currInfo = self.data
		elif(self.data[0] == 4.0):
			self.currThreshold = self.data
		elif(self.data[0] == 2.0):
			self.stopHandled = False
		elif(self.data[0] == 5.0):
			i = 1
			while(i <= 16):
				self.currRegression.append(self.data[i])
				i = i + 1
			#print(str(len(self.currRegression)) + "\n")
		elif(self.data[0] == 6.0):
			self.threshDone = True
		elif(self.data[0] == 7.0):
			self.fatigueReady = True
		self.Acknowledge(bIsData)
		
class RegressionBase():
	def __init__(self, muscleIndex, bLin, bQuad, bPiece):
		self.muscleIdx = muscleIndex
		self.linear = bLin
		self.quadratic = bQuad
		self.piecewise = bPiece
		
	def IsLinear(self):
		return self.linear
		
	def IsQuadratic(self):
		return self.quadratic
	
	def IsPiecewise(self):
		return self.piecewise
		
class RegressionLinear(RegressionBase):
	def __init__(self, muscleIndex, slope, yint):
		RegressionBase.__init__(self, muscleIndex, True, False, False)
		self.m = slope
		self.b = yint
	
	def GetSlope(self):
		return self.m
		
	def GetYIntercept(self):
		return self.b
		
class RegressionQuadratic(RegressionBase):
	def __init__(self, muscleIndex, c1, c2, c3):
		RegressionBase.__init__(self, muscleIndex, False, True, False)
		self.a = c1
		self.b = c2
		self.c = c3
		
	def GetA(self):
		return self.a
		
	def GetB(self):
		return self.b
	
	def GetC(self):
		return self.c

class RegressionPiecewise(RegressionBase):
	def __init__(self, muscleIndex, slopeList, yintList):
		RegressionBase.__init__(self, muscleIndex, False, False, True)
		self.ms = slopeList
		self.bs = yintList
		
	def GetNumLines(self):
		return len(self.ms)
		
	def GetSlopes(self):
		return self.ms
	
	def GetYInts(self):
		return self.bs
		
DISPLAY_LABEL = 1
EXERT_DEBUG = 1
HOLD_TIME = 5.0
START_TIME = 5.0
DROP_TIME = 3.0
DEBUG_NETWORK = 0
DEBUG_LIMITS = 1
FATIGUE_START_TIME = 20.0
#class that allows an object to be tracked w/ the 2nd head tracker
class TrackedObject(GenericObject):
	def __init__(self, sName, sMeshName, transform, bVis, bPhysics, physicsShape, interact, recvData = False, tcp_ip = None, tcp_port = None, num_floats = None):
		GenericObject.__init__(self, sName, sMeshName, transform, bVis, bPhysics, physicsShape, interact)
		self.lastDir = VRScript.Math.Vector(0,0,0)
		self.currWeight = 0
		self.currHeight = 0
		self.markIndex = 0
		self.currThreshold = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.currValues = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.currRegression = list()	#we want this to hold one of three types of regression checks - linear, quadratic or piece-wise linear
		self.markNames = ["first_mark", "second_mark", "third_mark"]
		self.longMarkNames = ["first_mark_long", "second_mark_long", "third_mark_long"]
		self.receiveData = recvData
		self.weightLifted = False
		self.weightDropped = False
		self.liftDone = False
		self.soundPlayed = True
		self.fatigueTest = False
		self.fatigueTestReady = False
		self.done = False
		self.blandCAVE = 0
		self.liftTime = 0
		self.startTime = 0
		self.dropTime = 0
		self.fatigueTime = 0
		self.fatigueHoldTime = 0
		self.lastFatigueTime = 0
		self.checkValues = False
		#self.attach(VRScript.Core.Renderable("tracked_three_pound_weight", VRScript.Resources.Mesh("tracked_three_pound_weight", "models\\three_pound_weight.ive")))
		#self.attach(VRScript.Core.Renderable("tracked_five_pound_weight", VRScript.Resources.Mesh("tracked_five_pound_weight", "models\\five_pound_weight.ive")))
		#self.attach(VRScript.Core.Renderable("tracked_ten_pound_weight", VRScript.Resources.Mesh("tracked_ten_pound_weight", "models\\ten_pound_weight.ive")))
		self.attach(VRScript.Core.Renderable("tracked_three_pound_weight", VRScript.Resources.Mesh("tracked_three_pound_weight", "models\\five_pound_weight_blank.ive")))
		self.attach(VRScript.Core.Renderable("tracked_five_pound_weight", VRScript.Resources.Mesh("tracked_five_pound_weight", "models\\five_pound_weight_blank.ive")))
		self.attach(VRScript.Core.Renderable("tracked_ten_pound_weight", VRScript.Resources.Mesh("tracked_ten_pound_weight", "models\\five_pound_weight_blank.ive")))
		#self.attach(VRScript.Core.Renderable("moving_marker", VRScript.Resources.Mesh("moving_marker", "models\\moving_marker.ive")))
		self.attach(VRScript.Core.Renderable("moving_marker_bland", VRScript.Resources.Mesh("moving_marker_bland", "models\\moving_marker.ive")))
		self.renderable("tracked_three_pound_weight").setVisible(False)
		self.renderable("tracked_five_pound_weight").setVisible(False)
		self.renderable("tracked_ten_pound_weight").setVisible(True)
		self.renderable("moving_marker_bland").setVisible(False)
		#special case physical here since we want it in the shape of the weight, not the hand...
		self.attach(VRScript.Core.Physical(self.name, VRScript.Resources.BoundingBox(self.renderable("tracked_ten_pound_weight").getMesh("tracked_ten_pound_weight"))))
		self.soundStart = VRScript.Core.Audible("soundStart", "sounds\\lift_the_weight.wav")
		self.soundRest = VRScript.Core.Audible("soundRest", "sounds\\lower_the_weight.wav")
		self.soundHold = VRScript.Core.Audible("soundHold", "sounds\\hold_for_five_seconds.wav")
		self.soundEnd = VRScript.Core.Audible("soundEnd", "sounds\\end_of_trial.wav")
		#self.soundCollide = VRScript.Core.Audible("soundCollide", "sounds\\clong_2 1.wav")
		audioProp = self.soundStart.getAudioProperties()
		audioProp.loop = False
		self.soundStart.setAudioProperties(audioProp)
		audioProp = self.soundRest.getAudioProperties()
		audioProp.loop = False
		self.soundRest.setAudioProperties(audioProp)
		audioProp = self.soundHold.getAudioProperties()
		audioProp.loop = False
		self.soundHold.setAudioProperties(audioProp)
		audioProp = self.soundEnd.getAudioProperties()
		audioProp.loop = False
		self.soundEnd.setAudioProperties(audioProp)
		#audioProp = self.soundCollide.getAudioProperties()
		#audioProp.loop = False
		#self.soundCollide.setAudioProperties(audioProp)
		#self.attach(self.soundCollide)
		self.attach(self.soundStart)
		self.attach(self.soundRest)
		self.attach(self.soundHold)
		self.attach(self.soundEnd)
		self.enduranceSoundPlayed = False
		self.holdPlayed = False
		self.count = 0
		self.testCount = 1000
		#self.movingMarkerStartPos = VRScript.Math.Vector(-4.67907427782332,-5.38940976314303,0.721681785835383)
		self.blandMarkerStartPos = VRScript.Math.Vector(-4.47907427782332,-5.38940976314303,0.721681785835383)
		self.movingMarkerStartPos = VRScript.Math.Vector(-3.51863678943039,-5.38940976314302,0.711681785835383)
		#debug...
		self.frameCount = 0
		
		if(self.receiveData):
			self.data = list()
			self.networkThread = NetworkThread(tcp_ip, tcp_port, num_floats)
			self.networkThread.start()

	def SetToStart(self):
		self.physical(self.name).setCollisionType(VRScript.Core.CollisionType.Static)
		startPos = VRScript.Math.Matrix()
		if(self.blandCAVE == 0):
			startPos.setTranslation(self.vStartPos)
		else:
			startPos.setTranslation(self.movingMarkerStartPos)
		self.movable().setPose(startPos)
		if(self.done == False):
			if(self.soundPlayed):
				self.networkThread.SetObjectStatus('1')
			elif(self.done == False):
				self.networkThread.SetObjectStatus('0')
			
	def SetToTracker(self, onGround = False):
		#self.physical(self.name).setCollisionType(VRScript.Core.CollisionType.Kinematic)
		#secondTracker = VRScript.Core.Entity('User0Hand')
		secondTracker = VRScript.Core.Entity('User1Head')
		m = secondTracker.movable().selfToWorld()
		if(self.name == "hand"):
			#rotX = VRScript.Math.Matrix()
			#rotX.postAxisAngle(90.0, VRScript.Math.Vector(1.0,0.0,0.0))
			#rotY = VRScript.Math.Matrix()
			#rotY.postAxisAngle(180.0, VRScript.Math.Vector(0.0, 0.0, 1.0))
			if(self.blandCAVE == 1):
				#mat = VRScript.Math.Matrix()
				v = VRScript.Math.Vector(self.movingMarkerStartPos.x, self.movingMarkerStartPos.y, m.getTranslation().z)
				#mat.setTranslation(v)
				#oldX = self.movingMarkerStartPos.x
				rotZ = VRScript.Math.Matrix()
				#rotZ.postAxisAngle(90.0, VRScript.Math.Vector(0.0, 0.0, 1.0))
				rotZ.setTranslation(v)
				#m = m * rotZ
				#m.setTranslation(v)
				#v = VRScript.Math.Vector(m.getTranslation())
				#v.y = v.y + 0.20	#may not need this now...
				#v.x = oldX
				#m.setTranslation(v)
				self.movable().setPose(rotZ)
			else:
				rotZ = VRScript.Math.Matrix()
				rotZ.postAxisAngle(90.0, VRScript.Math.Vector(0.0, 0.0, 1.0))
				m = m * rotZ
				v = VRScript.Math.Vector(m.getTranslation())
				v.y = v.y + 0.02
				v.z = v.z + 0.02
				m.setTranslation(v)
				#m = m * rotY
				self.movable().setPose(m)
		else:
			v = VRScript.Math.Vector(m.getTranslation())
			v.y = v.y - 0.1
			#v.y = v.y + 0.2
			v.x = v.x - 0.2
			if(onGround == True):
				v.z = 0.0
			m.setTranslation(v)
			self.movable().setPose(m)
		#self.physical(self.name).setCollisionType(VRScript.Core.CollisionType.Dynamic)
		#self.bGrabbed = True
		#print("set to tracker")
		
	def OnUpdate(self, cbInfo):
		#self.count = self.count + 1
		#if(self.count > self.testCount):
		#	self.BlandCAVE(True)
		#match the object's transform with the 2nd head tracker's transform..
		if self.receiveData:

			if self.networkThread.IsConnected():
			
				self.data = self.networkThread.GetData()
				bNewData = False
				bInactive = False
				bNewInfo = self.networkThread.HasInfo()
				bNewThreshold = self.networkThread.HasThreshold()
				bNewStop = self.networkThread.IsStopNotHandled()
				bNewRegression = self.networkThread.HasRegression()
				bFatigueReady = self.networkThread.IsFatigueReady()
				self.frameCount = self.frameCount + 1
				
				if(len(self.data) > 0):
					msgStr = self.data[0]
					if(msgStr == 1.0):
						bNewData = True
					elif(msgStr == 0.0):
						bInactive = True

				if bNewData:
					i = 1
					while i <= 16:
						self.currValues[i-1] = self.data[i]
						if(DEBUG_NETWORK):
							if(i < 5):
								print(str(self.currValues[i-1]) + " ")
						i = i+1
					
					if(DEBUG_NETWORK):
						print("\n")
						print("Frame count: " + str(self.frameCount) + "\n")
						
					if(self.soundPlayed == False):
						if((cbInfo.frameTime - self.startTime) > START_TIME):
							if(self.fatigueTest == False):
								#print("playing sound!\n")
								self.audible("soundStart").play()
							self.soundPlayed = True
							self.networkThread.SetObjectStatus('1')
					#else:
					#	self.networkThread.SetObjectStatus('0')
						
					if(self.weightDropped == True):
						strDropped = "Dropped: "
						strDropped = strDropped + str(int(DROP_TIME) - int(cbInfo.frameTime - self.dropTime))
						self.DisplayLabel(strDropped)
						if((cbInfo.frameTime - self.dropTime) > DROP_TIME):
							self.weightDropped = False
							self.weightLifted = False
							self.SetToStart()
							
				if bNewInfo:
					print("new info")
					info = self.networkThread.GetInfo()
					self.currWeight = info[1]
					self.currHeight = info[2]
					self.markIndex = int(info[3])-1
					print(str(self.markIndex) + "\n")
					self.fatigueTime = int(info[4])
					wasBland = (self.blandCAVE == 1)
					self.blandCAVE = int(info[5])
					if(wasBland and self.blandCAVE == 0 ):
						self.BlandCAVE(False)
					elif(wasBland == False and self.blandCAVE == 1):
						self.BlandCAVE(True)
						
					if(self.fatigueTime != 0):
						print("playing fatigue sound!\n")
						self.fatigueTest = True
						self.audible("soundStart").play()
						#print("fatigue test active")
						#print("fatigue time: " + str(self.fatigueTime))
						
					#set weight so it's back on the table.
					self.SetToStart()
					
					#switch which weight is being rendered...
					if(self.blandCAVE == 0):
						if(self.currWeight == 10):
							self.renderable("hand").setVisible(False)
							self.renderable("tracked_five_pound_weight").setVisible(False)
							self.renderable("tracked_three_pound_weight").setVisible(False)
							self.renderable("tracked_ten_pound_weight").setVisible(True)
						elif(self.currWeight == 5):
							self.renderable("hand").setVisible(False)
							self.renderable("tracked_ten_pound_weight").setVisible(False)
							self.renderable("tracked_three_pound_weight").setVisible(False)
							self.renderable("tracked_five_pound_weight").setVisible(True)
						elif(self.currWeight == 3):
							self.renderable("hand").setVisible(False)
							self.renderable("tracked_three_pound_weight").setVisible(True)
							self.renderable("tracked_five_pound_weight").setVisible(False)
							self.renderable("tracked_ten_pound_weight").setVisible(False)
						
					if(self.blandCAVE == 0):
						VRScript.Core.Entity(self.markNames[self.markIndex]).renderable(self.markNames[self.markIndex]).setVisible(True)
						VRScript.Core.Entity(self.markNames[(self.markIndex+1) % 3]).renderable(self.markNames[(self.markIndex+1) % 3]).setVisible(False)
						VRScript.Core.Entity(self.markNames[(self.markIndex+2) % 3]).renderable(self.markNames[(self.markIndex+2) % 3]).setVisible(False)
					else:
						VRScript.Core.Entity(self.longMarkNames[self.markIndex]).renderable(self.longMarkNames[self.markIndex]).setVisible(True)
						VRScript.Core.Entity(self.longMarkNames[(self.markIndex+1) % 3]).renderable(self.longMarkNames[(self.markIndex+1) % 3]).setVisible(False)
						VRScript.Core.Entity(self.longMarkNames[(self.markIndex+2) % 3]).renderable(self.longMarkNames[(self.markIndex+2) % 3]).setVisible(False)
						
					#play sound after  5 seconds...
					self.startTime = cbInfo.frameTime
					self.soundPlayed = False
					#print("grabbed start time\n")
					self.networkThread.SetObjectStatus('0')
					self.weightLifted = False
					self.weightDropped = False
					self.liftDone = False
					self.holdPlayed=False
					self.fatigueTest = False
					if(self.fatigueTime != 0):
						self.fatigueTest = True
					self.fatigueTestReady = False
					self.done = False
					self.checkValues = True
					self.networkThread.ClearInfo()
					
				if bNewThreshold:
					print("new threshold")
					#todo - probably a much easier way of passing the values to the array here..
					thresh = self.networkThread.GetThreshold()
					i = 1
					while i <= 16:
						self.currThreshold[i-1] = thresh[i]
						#print(str(self.currThreshold[i-1]) + "\n")
						i = i+1
					self.networkThread.ClearThreshold()
					
				if bNewRegression:
					print("new regression")
					self.currRegression = list()
					reg = self.networkThread.GetRegression()
					i = 0
					mIndex = 0
					while i < len(reg):
						if(reg[i] == 1.0):
							print("muscle " + str(mIndex) + " is linear!\n")
							print("m: " + str(reg[i+1]) + " b: " + str(reg[i+2]))
							#linear
							self.currRegression.append(RegressionLinear(mIndex, reg[i+1], reg[i+2]))
							i += 3
							mIndex = mIndex + 1
						elif(reg[i] == 2.0):
							print("muscle " + str(mIndex) + " is quadratic!\n")
							print("a: " + str(reg[i+1]) + " b: " + str(reg[i+2]) + " c: " + str(reg[i+3]))
							self.currRegression.append(RegressionQuadratic(mIndex, reg[i+1], reg[i+2], reg[i+3]))
							mIndex = mIndex + 1
							i += 4
						elif(reg[i] == 3.0):
							print("muscle " + str(mIndex) + " is piecewise!\n")
							#todo - make it so more muscles can work automatically here..
							self.currRegression.append(RegressionPiecewise(mIndex, [reg[i+1], reg[i+2], reg[i+3]],[reg[i+4], reg[i+5], reg[i+6]]))
							mIndex = mIndex + 1
							i += 7
						else:
							i = i + 1	#this is the tail end of the regression info so just ignore it.. since it'll be all zero
					self.networkThread.ClearRegression()
				if bNewStop:
					print("stopping")
					self.renderable("tracked_three_pound_weight").setVisible(False)
					self.renderable("tracked_five_pound_weight").setVisible(False)
					self.renderable("tracked_ten_pound_weight").setVisible(False)
					if(self.blandCAVE == 0):
						VRScript.Core.Entity("first_mark").renderable("first_mark").setVisible(False)
						VRScript.Core.Entity("second_mark").renderable("second_mark").setVisible(False)
						VRScript.Core.Entity("third_mark").renderable("third_mark").setVisible(False)
					else:
						VRScript.Core.Entity("first_mark_long").renderable("first_mark_long").setVisible(False)
						VRScript.Core.Entity("second_mark_long").renderable("second_mark_long").setVisible(False)
						VRScript.Core.Entity("third_mark_long").renderable("third_mark_long").setVisible(False)
					
					self.SetToStart()
					self.startTime = cbInfo.frameTime
					self.liftTime = 0
					self.dropTime = 0
					self.soundPlayed = True
					self.weightLifted = False
					self.weightDropped = False
					self.liftDone = False
					self.fatigueTest = False
					self.fatigueTestReady = False
					self.done = False
					self.checkValues = False
					self.networkThread.SetObjectStatus('0')
					self.networkThread.SetStopHandled(True)
				
				if bFatigueReady:
					self.fatigueTestReady = True
					self.networkThread.ClearFatigueReady()
					
				if bInactive: 
					return
				
				#self.SetToTracker()
				#self.CheckLimits(True)
				#only set to tracker if we exceed thresholds
				#check that the user is fairly close to intersecting with the weight
				if(self.done == False and self.checkValues):
					if(self.weightLifted == False and self.weightDropped == False):
						secondTracker = VRScript.Core.Entity('User1Head')
						m = secondTracker.movable().selfToWorld()
						pos = m.getTranslation()
						#print("tracker pos:")
						#print(pos.x, pos.y, pos.z)
						#for dev lab issue - we need to transform the vStartPos to world space..
						width = 0.55
						height = 0.25
						depth = 0.25
						entPos = self.vStartPos
						if(self.blandCAVE):
							entPos = self.blandMarkerStartPos
							width = 0.75
							height = 0.25
							depth = 0.25
						#entPos = self.movable().selfToWorld().getTranslation()
						#print("weight pos:")
						#print(entPos.x, entPos.y, entPos.z)
						#check whether pos is within a box surrounding entPos..
						#if it isn't, don't bother checking thresholds..
						if(pos.x < entPos.x+depth and pos.x > entPos.x-depth and pos.y < entPos.y+width and pos.y > entPos.y-width and pos.z < (entPos.z+0.07) and pos.z > (entPos.z-height)):
							if(self.CheckLimits(True)):
								self.SetToTracker()
								self.weightLifted = True
								self.networkThread.SetObjectStatus('2')
								self.weightDropped = False
							else:
								self.weightLifted = False
						else:
							if(self.fatigueTest == False):
								if(self.blandCAVE):
									self.DisplayLabel("Lift Green to Red")
								else:
									self.DisplayLabel("Grasp Weight")
							else:
								self.DisplayLabel("Endurance Test")
					else:
						#don't allow weight to be dropped while fatiguing?
						if(self.weightDropped == False):
							strLift = "Lift\n"
							strLift = strLift + str(self.currValues[0]) + "\n" + str(self.currValues[1]) + "\n" + str(self.currValues[2]) + "\n" + str(self.currValues[3]) + "\n"
							strLift = strLift + "Thresh:\n" + str(self.currThreshold[0]) + "\n" + str(self.currThreshold[1]) + "\n" + str(self.currThreshold[2]) + "\n" + str(self.currThreshold[3])
							self.DisplayLabel(strLift)
							#check that we're still above threshold..
							if(self.CheckLimits(True)):
								self.SetToTracker()
								self.weightLifted = True
								self.networkThread.SetObjectStatus('2')
								self.weightDropped = False
							else:
								#if we had been lifting the weight, but stopped using enough force - make weight fall w/ physics
								#but then we will need to reset it to it's original position on the next go-around..after 3 seconds
								#self.fatigueTest == False
								self.DisplayLabel("Dropped")
								self.weightLifted = False
								self.weightDropped = True
								self.networkThread.SetObjectStatus('3')
								self.dropTime = cbInfo.frameTime
								#print("below threshold")
								if(self.bPhys == True):
									self.physical(self.name).setCollisionType(VRScript.Core.CollisionType.Dynamic)

		#track height here...
		if(self.weightLifted and self.weightDropped==False and self.done == False and self.checkValues):		#added weightDropped=false check here...
			#secondTracker = VRScript.Core.Entity('User0Hand')
			secondTracker = VRScript.Core.Entity('User1Head')
			m = secondTracker.movable().selfToWorld()
			#need to check whether the weight is at/above height from it's starting point...
			weightPos = m.getTranslation()
			if(self.liftDone == False):
				strLift = "Lift\n"
				strLift = strLift + str(weightPos.z) + "\n"
				strLift = strLift + "Target Height:\n" + str(self.currHeight) + "\n"
				self.DisplayLabel(strLift)
				if(weightPos.z > self.currHeight):
					if(self.liftTime == 0):
						self.liftTime = cbInfo.frameTime
					
					if(self.fatigueTest):
						if(self.fatigueTestReady):
							if(self.fatigueHoldTime > self.fatigueTime):
								self.DisplayLabel("Rest")
								self.liftDone = True
								self.networkThread.SetObjectStatus('4')
								self.soundRest.play()
								#self.weightLifted = False
								#self.weightDropped = False
								#self.SetToStart()
								self.startTime = 0
								self.liftTime = 0
								self.done = True
							else:
								self.fatigueHoldTime = self.fatigueHoldTime + ( cbInfo.frameTime - self.lastFatigueTime )
								strHold = "Endurance: "
								strHold = strHold + (str(self.fatigueTime - int(self.fatigueHoldTime)))
								self.DisplayLabel(strHold)
						else:
							strHold = "Endurance Ready"
							self.DisplayLabel(strHold)
							if(self.enduranceSoundPlayed == False):
								self.audible("soundStart").play()
								self.enduranceSoundPlayed = True
					else:
						holdTime = HOLD_TIME
						#need to stop timer for regular test as well??
						if((cbInfo.frameTime - self.liftTime) > holdTime):
							self.DisplayLabel("Rest")
							self.liftDone = True
							self.networkThread.SetObjectStatus('4')
							self.soundRest.play()
							#self.weightLifted = False
							#self.weightDropped = False
							#self.SetToStart()
							self.startTime = 0
							self.liftTime = 0
						else:
							strHold = "Hold: "
							strHold = strHold + (str(HOLD_TIME - int(cbInfo.frameTime-self.liftTime)))
							self.DisplayLabel(strHold)
							if(self.holdPlayed==False):
								self.soundHold.play()
								self.holdPlayed=True
				else:
					#set lift status back to 2
					self.networkThread.SetObjectStatus('2')
			else:
				strLift = "Lower\n"
				strLift = strLift + str(weightPos.z) + "\n"
				strLift = strLift + "Target Height:\n" + str(self.vStartPos.z+0.05) + "\n"
				self.DisplayLabel(strLift)
				if(weightPos.z <= (self.vStartPos.z+0.05)):
					self.weightLifted = False
					self.weightDropped = False
					self.SetToStart()
					self.done = True
					self.soundEnd.play()
					self.networkThread.SetObjectStatus('5')
		else:
			self.liftTime = 0
			if(self.done):
				strDone = "Done!"
				self.DisplayLabel(strDone)
				self.weightLifted = False
			#vCurrDir = VRScript.Math.Vector(m.getAxisAngle())
			#angleBetween = math.degrees(math.acos(vCurrDir.dot(VRScript.Math.Vector(0.0, 0.0, -1.0))))
			#if(angleBetween > self.currAngle):
			#	print("lifted past angle!")
			#self.lastDir = vCurrDir
		self.lastFatigueTime = cbInfo.frameTime
		
	def CheckLimits(self, checkRegression=False):
		#this function handles whether the user is still exerting enough force to hold the weight
		if(checkRegression):
			#regression line slope / intercept will be transfered across and and exist in self.currRegression..
			#based on current height, check what we need our thresholds to be then see if currvalues are above those...
			#if all 4 are above, we're lifting, else we've dropped!
			#also - should we be offsetting this by the height of the table?
			#also - need to convert back to inches when evaluating in the regression equation..
			#emg(x) = (height(y)-yintercept)/slope
			secondTracker = VRScript.Core.Entity('User1Head')
			m = secondTracker.movable().selfToWorld()
			h = m.getTranslation().z * 39.3701
			strLift = "Exert\n"
			
			#if EXERT_DEBUG:
			#	strLift = strLift + str(self.currValues[0]) + "\n" + str(self.currValues[1]) + "\n" + str(self.currValues[2]) + "\n" + str(self.currValues[3]) + "\n"
			#	strLift = strLift + "Thresh:\n" + str(self.currThreshold[0]) + "\n" + str(self.currThreshold[1]) + "\n" + str(self.currThreshold[2]) + "\n" + str(self.currThreshold[3]) + "\n"
			
			aboveLimits = True
			i = 0
			#print(str(len(self.currRegression)))
			while i < len(self.currRegression):
				
				if(self.currRegression[i].IsLinear()):
					#print("checking linear regression for muscle " + str(i) + "\n")
					emgVal = self.currRegression[i].GetSlope() * h + self.currRegression[i].GetYIntercept()
					strLift = strLift + str(self.currValues[i]) + "\n"
					strLift = strLift + "Thresh: " + str(emgVal) + "\n"
					if(self.currValues[i] < emgVal):
						aboveLimits = False
						if(DEBUG_LIMITS):
							print("muscle " + str(i) + " failed threshold at height: " + str(h) + " Emg Val: " + str(self.currValues[i]) + " Threshold: " + str(emgVal))
						#break
				elif(self.currRegression[i].IsQuadratic()):
					#print("checking quadratic regression for muscle " + str(i) + "\n")
					a = self.currRegression[i].GetA()
					b = self.currRegression[i].GetB()
					c = self.currRegression[i].GetC()
					emgVal = a * h * h + b * h + c
					strLift = strLift + str(self.currValues[i]) + "\n"
					strLift = strLift + "Thresh: " + str(emgVal) + "\n"
					if(self.currValues[i] < emgVal):
						aboveLimits = False
						if(DEBUG_LIMITS):
							print("muscle " + str(i) + " failed threshold at height: " + str(h) + " Emg Val: " + str(self.currValues[i]) + " Threshold: " + str(emgVal))
						#break
				elif(self.currRegression[i].IsPiecewise()):
					#print("checking piecewise regression for muscle " + str(i) + "\n")
					m = self.currRegression[i].GetSlopes()
					b = self.currRegression[i].GetYInts()
					emgVal = 0
					if(h > 29 and h < 35):
						emgVal = m[0] * h + b[0]
					elif(h >= 35 and h < 42):
						emgVal = m[1] * h + b[1]
					elif(h >= 42 and h <= 51):
						emgVal = m[2] * h + b[2]
					
					if(emgVal != 0):
						strLift = strLift + str(self.currValues[i]) + "\n"
						strLift = strLift + "Thresh: " + str(emgVal) + "\n"
						
					if(self.currValues[i] < emgVal):
						aboveLimits = False
						#print("muscle " + str(i) + " failed threshold")
						#break
				i = i+1
			
			self.DisplayLabel(strLift)
			
			return aboveLimits
		else:
			aboveLimits = True
			i = 0
			while i < 16:
				if(self.currValues[i] < self.currThreshold[i]):
					aboveLimits = False
					print("muscle " + str(i) + " failed threshold")
					break
				i = i+1
			return aboveLimits
	
	def DisplayLabel(self, str):
		if DISPLAY_LABEL:
			label = VRScript.Core.Entity('weightLabel')
			f = label.fonttext("weight_text")
			f.setText(str)
	
	def BlandCAVE(self, bOn):
		toggleNames = ["yoga mat", "yoga mat_1", "weight_scenario_1", "Recumbent Exercise Bike1", "gym_window", "stray_geometry", "hand", "table", "marker_stick1"]
		toggleOnNames = ["marker_stick_bland", "table_bland"]
		
		i = 0
		while(i < len(toggleNames)):
			#print(toggleNames[i])
			VRScript.Core.Entity(toggleNames[i]).renderable(toggleNames[i]).setVisible(bOn==False)
			i = i + 1
		
		i=0
		while(i < len(toggleOnNames)):
			VRScript.Core.Entity(toggleOnNames[i]).renderable(toggleOnNames[i]).setVisible(bOn==True)
			i = i + 1
			
		self.blandMode = bOn
		#VRScript.Core.Entity("moving_marker").renderable("moving_marker").setVisible(bOn)
		#VRScript.Core.Entity("background").renderable("background").setVisible(bOn)
		self.renderable("moving_marker_bland").setVisible(bOn)
		self.renderable("tracked_three_pound_weight").setVisible(False)
		self.renderable("tracked_five_pound_weight").setVisible(False)
		self.renderable("tracked_ten_pound_weight").setVisible(False)
		
	#def OnButtonPress(self, cbInfo, btInfo, user):
	#	self.SetToTracker()
		
	#def OnCollision(self, cbInfo, intInfo):
		#if self.bPhys:
			#if self.getName() == "hand":
				#self.soundCollide.play()
				#print("collided")
				#self.bGrabbed = False
	#			self.SetToTracker()
				#intInfo.otherComponent.applyImpulse(VRScript.Math.Vector(0.0, 0.0, 1.0), VRScript.Math.Vector(0, 0, 0))
	#		if intInfo.otherEntity.getName() == "stray_geometry" or intInfo.otherEntity.getName() == "ground":
				#print("collided")
	#			self.SetToTracker()
	#			self.SetToStart()
	#		else:
	#			intInfo.selfComponent.applyImpulse(VRScript.Math.Vector(0.0, 5.0, 5.0), VRScript.Math.Vector(0, 0, 0))
				#self.bGrabbed = False
				#intInfo.selfComponent.applyImpulse(VRScript.Math.Vector(0.0, 0.0, 1.0), VRScript.Math.Vector(0, 0, 0))
				
class LELReceiver(VRScript.Core.Behavior):
    
    def __init__(self,entity=None, tcp_ip = None, tcp_port = None, num_floats = None):
        if tcp_ip is None:         tcp_ip = '127.0.0.1'
        if tcp_port is None:     tcp_port = 19950
        if num_floats is None: num_floats = 4
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.num_floats = num_floats
        
        print("LELReceiver init for " + self.tcp_ip + ":" + str(self.tcp_port) + ", expecting " + str(self.num_floats) + " floats.")
        VRScript.Core.Behavior.__init__(self,entity)

        self.connected = False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.tcp_ip, self.tcp_port))
        # I think if it errors it won't get to this line?
        self.connected = True
        self.data = list()

    def OnUpdate(self, info):
        BUFFER_SIZE = 4 * self.num_floats
        if self.connected:
            buff = self.s.recv(BUFFER_SIZE)
            if not buff: self.connected = False
            self.data = unpack('f'*self.num_floats, buff)
            if DEBUG: print(self.data)
            # Acknowledge
            self.s.send('1'.encode('ascii'))

    def getData(self):
        return self.data