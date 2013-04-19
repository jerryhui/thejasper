import VRScript
import math
from math import *
from Skeleton import Skeleton, Joint
import sys
#import StringIO

DEBUG = 0

######################### Generic Scenario Class #################################
class LELScenario:

	def __init__(self):
		self.active_objects = []
		self.static_objects = []
		self.debugCount = 0
		self.skeleton = 0
		self.rotating = 0
		self.rotationCenter = VRScript.Math.Vector(0.0, 0.0, 0.0)
		self.scaling = 0
		self.moving = 0
		self.scaleStartDistance = 0
		self.gizmo = 0

	def create_billboard(self, sName, position, follow=True):
		new_entity = Billboard(sName, position, follow)
		self.static_objects.append(new_entity)
		return new_entity
	
	def create_entity(self, sName, sMeshName, position, vis, physics, physicsShape, interact, physicsType="Static", scale=[1.0, 1.0, 1.0], rot=[0.0, 0.0, 0.0, 0.0]):
		new_entity = GenericObject(sName, sMeshName, position, vis, physics, physicsShape, interact, physicsType)
		self.static_objects.append(new_entity)
		new_entity.parentScene = self
		return new_entity
		
	def create_primitive(self, sName, sMeshName, position, vis, physics, physicsShape, interact, color=VRScript.Core.Color(1,1,1,1), scale=[1.0, 1.0, 1.0], rot=[0.0, 0.0, 0.0, 0.0]):
		new_primitive = GenericObject(sName, sMeshName, position, vis, physics, physicsShape, interact)
		new_primitive.isPrimitive = True
		print("creating primitive")
		new_primitive.SetMaterialProperties(VRScript.Core.MaterialProperties(color,color,color,color,1.0,1.0,1,False))
		self.static_objects.append(new_primitive)
		new_primitive.parentScene = self
		return new_primitive
		
	def create_gizmo(self):
		self.gizmo = GenericObject("gizmo", "models\\gizmo.ive", [0,0,0], True, False, "None", False)
		#scale it down a little
		scaleDown = VRScript.Math.Matrix()
		scaleDown.makeScale(VRScript.Math.Vector(0.5, 0.5, 0.5))
		self.gizmo.movable().setPose(scaleDown)
		
	def create_ground_plane(self):
		ground_plane = GenericObject("ground", "models\\ground_plane.osg", [0,0,0], True, True, "Plane", False, "Static")
		self.static_objects.append(ground_plane)
		self.set_physics_properties("ground", [0, .9, 1, 1, .5])
		#ground_plane = VRScript.Core.Entity("ground", "models\\ground_plane.osg")
		#ground_plane.attach(VRScript.Core.Physical("p_floor", VRScript.Resources.ConvexMesh(ground_plane.renderable('').getMesh(''))))
		#ground_plane.physical('').setPhysicsProperties(VRScript.Core.PhysicsProperties(0,.9,1,1,.5))
		#VRScript.Core.Entity('e_ground').attach(VRScript.Core.Physical('p_ground',VRScript.Resources.Plane()))
	
	def create_physics_spring(self, sName, sMeshName, position, vis, physics, physicsShape, interact, mass=0.1, tension=10.0, damping=0.5, length=0.1, second_tracker=False):
		new_entity = PhysicsSpring(sName, sMeshName, position, vis, physics, physicsShape, interact, mass, tension, damping, length, second_tracker)
		
	def create_skeleton(self, sName, recvData=False, tcp_ip = None, tcp_port = None, num_floats = None):
		new_skel = Skeleton(sName, recvData, tcp_ip, tcp_port, num_floats)
		self.skeleton = new_skel
		return new_skel
		
	def create_tracked_entity(self, sName, sMeshName, transform, vis, physics, physicsShape, interact, recvData=False, tcp_ip = None, tcp_port = None, num_floats = None):
		new_entity = TrackedObject(sName, sMeshName, transform, vis, physics, physicsShape, interact, recvData, tcp_ip, tcp_port, num_floats)
		self.active_objects.append(new_entity)
		return new_entity

	def create_wand(self, sName, sMeshName):
		hand = WandObject(sName, sMeshName)
		#"models\\hand.ive"
	
	def clear_selection(self):	
		for obj in self.static_objects:
			if(len(obj.physicals()) > 0):
				if(obj.physical(obj.getName()) != None):
					obj.physical(obj.getName()).enableDebugVisual(False)
	
	def delete_selection(self):
		for obj in self.static_objects:
			if(obj.IsSelected()):
				obj.renderable('').setVisible(False)
				obj.physical(obj.getName()).enableDebugVisual(False)
				obj.deleted = True
	
	def duplicate_selection(self):
		for obj in self.static_objects:
			if(obj.IsSelected()):
				k = 0
				
	def grab_selection(self, center, cbInfo):
		#bring combination of objects to center of shoulders...
		#find total bounding box center of all selected objects..
		print("grabbing selection")
		minTotal = [9999999,9999999,9999999]
		maxTotal = [-9999999,-9999999,-9999999]
		for obj in self.static_objects:
			if(obj.IsSelected()):
				c = VRScript.Math.Point(obj.bb.center.x, obj.bb.center.y, obj.bb.center.z)
				c = c.transform(obj.movable().getPose())
				hw = VRScript.Math.Vector(obj.bb.halfWidth.x, obj.bb.halfWidth.y, obj.bb.halfWidth.z)
				hw = hw.transform(obj.movable().getPose())
				minPt = [c.x-hw.x, c.y-hw.y, c.z-hw.z]
				maxPt = [c.x+hw.x, c.y+hw.y, c.z+hw.z]
				for i in range(0,3):
					if(minPt[i] < minTotal[i]):
						minTotal[i] = minPt[i]
					if(maxPt[i] > maxTotal[i]):
						maxTotal[i] = maxPt[i]
				break #!!!!FOR NOW - JUST ALLOW ONE OBJECT TO BE GRABBED AT ONCE
		#calculate vector from total bounds center to shoulder center
		boundsCenter = VRScript.Math.Vector((maxTotal[0]+minTotal[0]) * 0.5, (maxTotal[1]+minTotal[1]) * 0.5, (maxTotal[2]+minTotal[2]) * 0.5)
		vToCenter = center-boundsCenter
		#use this same vector to translate each object..
		for obj in self.static_objects:
			if(obj.IsSelected()):
				obj.StoreReturnTransform()
				obj.physical(obj.getName()).setCollisionType(VRScript.Core.CollisionType.Kinematic)
				m = VRScript.Math.Matrix(obj.movable().selfToWorld())
				v = VRScript.Math.Vector(m.getTranslation())
				v = v + vToCenter
				m.setTranslation(v)
				obj.movable().setPose(m)
				obj.bGrabbed = True
				break #!!!!FOR NOW - JUST ALLOW ONE OBJECT TO BE GRABBED AT ONCE
					
	def release_selection(self, cbInfo):
		print("Releasing selection")
		for obj in self.static_objects:
			if(obj.IsGrabbed()):
				obj.bGrabbed = False
				obj.physical(obj.getName()).setCollisionType(VRScript.Core.CollisionType.Dynamic)
				
	def return_selection(self, cbInfo):
		print("Returning objects")
		for obj in self.static_objects:
			if(obj.IsGrabbed()):
				obj.bGrabbed = False
				m = obj.movable().getPose()
				m.setTranslation(obj.initialPose.getTranslation())
				obj.movable().setPose(m)
				obj.physical(obj.getName()).setCollisionType(VRScript.Core.CollisionType.Dynamic)

	def stop_movement(self, cbInfo):
		for obj in self.static_objects:
			if(obj.IsSelected()):
				m = obj.movable().getPose()
				obj.initialPose = m
				obj.physical(obj.name).setCollisionType(VRScript.Core.CollisionType.Dynamic)
				
	def ray_cast_select(self, start, dir, bSel, keep, cbInfo):
		maxDist = 99999999.0
		hitIndex = -1
		count = 0
		#b = BoxDebugPhysics(VRScript.Math.Point(0,0,0), VRScript.Math.Vector(2,2,2), start, dir, "tester_" + str(self.debugCount))
		#b.OnInit(None)
		#self.debugCount = self.debugCount + 1
		
		for obj in self.static_objects:
			if(obj.bGrabbed == False):
				#test the ray intersection with the colliders of the object...(bounding box assumption for now)
				if(len(obj.physicals()) > 0):
					if(obj.bb != None):	#todo: allow general intersection testing w/ the other shapes as well as boxes..
						#perform box ray intersection..
						dist = obj.RayIntersect(start, dir)
						if(dist > 0 and dist < maxDist):
							#print(dist)
							maxDist = dist
							hitIndex = count
					
			count = count + 1
		
		if(keep == False and self.moving == 0):
			self.clear_selection()
				
		#print(hitIndex)
		if(hitIndex != -1):
			sName = self.static_objects[hitIndex].getName()
			self.static_objects[hitIndex].physical(sName).enableDebugVisual(True)
			hitPoint = start + (dir * maxDist)
			self.gizmo.renderable(self.gizmo.name).setVisible(True)
			m = self.gizmo.movable().getPose()
			m.setTranslation(hitPoint)
			self.gizmo.movable().setPose(m)
		else:
			#if nothing hit, make sure selection highlight is off
			#self.clear_selection()	#TEMP
			#check for where the ray intersects the ground plane..
			#test whether ray and ground plane are parallel..
			up = VRScript.Math.Vector(0,0,1)
			dirDotUp = up.dot(dir)
			if(dirDotUp == 0):
				self.gizmo.renderable(self.gizmo.name).setVisible(False)
			else:
				#plane intersection
				s = up.dot(-start) / (up.dot(dir))
				if(s >= 0.0):
					#print(s)
					self.gizmo.renderable(self.gizmo.name).setVisible(True)
					hitPoint = start + (dir * s)
					m = self.gizmo.movable().getPose()
					m.setTranslation(hitPoint + VRScript.Math.Vector(0,0,0.1))
					self.gizmo.movable().setPose(m)
	
	def save_scene(self, sName):
		#todo - save out the scene to a python file...that we can reload..using our create_entity / primitive syntax.. 
		f = open("V:\\test_scenes\\"+sName, 'w+')
		#f.write('vac = VoiceActionController()')
		#f.write('vac.scene.create_entity("blank_ground_plane", "models\\blank_ground_plane.ive", [0,0,0], True, True, "Concave", False)')
		for obj in self.static_objects:
			m = obj.movable().selfToWorld()
			pos = m.getTranslation()
			scale = m.getScale()
			vAxis = m.getAxisAngle()
			#actually we don't necessarily want to write it out like this?
			#they could instead be in json type format that we then read back in in here..
			if(obj.isPrimitive):
				#for now just output material property color as ambientColor, eventually we can fancy it up
				f.write('create_primitive(\"' + obj.name + '\", \"' + obj.meshName + '\", [' + str(pos.x) + ', ' + str(pos.y) + ', ' + str(pos.z) + '], True, True, \"' + obj.physShape + '\", True, VRScript.Core.Color(' + str(obj.matProp.ambientColor.r) + ', ' + str(obj.matProp.ambientColor.g) + ', ' + str(obj.matProp.ambientColor.b) + '), [' + str(scale.x) + ', ' + str(scale.y) + ', ' + str(scale.z) + '], [' + str(vAxis.w) + ', ' + str(vAxis.x) + ', ' + str(vAxis.y) + ', ' + str(vAxis.z) + '])\n')
			else:
				if not "ground" in obj.name:
					f.write('create_entity(\"' + obj.name + '\", \"' + obj.meshName + '\", [' + str(pos.x) + ', ' + str(pos.y) + ', ' + str(pos.z) + '], True, True, \"' + obj.physShape + '\", True, [' + str(scale.x) + ', ' + str(scale.y) + ', ' + str(scale.z) + '], [' + str(vAxis.w) + ', ' + str(vAxis.x) + ', ' + str(vAxis.y) + ', ' + str(vAxis.z) + '])\n')
			
		f.close()
	
	def load_scene(self, sName):
		print("loading scene %s" % sName)
		f = open("V:\\test_scenes\\"+sName, 'r')
		#codeOut = StringIO.StringIO()
		#codeErr = StringIO.StringIO()
		#sys.stdout = codeOut
		#sys.stderr = codeErr
		
		for line in f:
			exec(line)
			#assign some default phys properties to the previously added object to static object list then call OnInit
			newModel = self.static_objects[len(self.static_objects)-1]
			print(newModel.name)
			newModel.SetPhysProperties([3.0, 0.25, 0.9, 1, 0.5])
			newModel.OnInit(None)
			#todo - might have to call OnInit(None) here..?
		#sys.stdout = sys.__stdout__
		#sys.stderr = sys.__stderr__
		
		#s = codeErr.getvalue()
		#print("error:\n%s\n" % s)
		#s = codeOut.getvalue()
		#print("output:\n%s\n" % s)
		
		#codeOut.close()
		#codeErr.close()
		
	def set_animation_properties(self, sName, vAxis, vValues, animType):
		for obj in self.static_objects:
			if(obj.name == sName):
				obj.SetAnimationProperties(vAxis, vValues, animType)
				break
			
	def set_physics_properties(self, sName,  vValues):
		for obj in self.static_objects:
			if(obj.name == sName):
				obj.SetPhysProperties(vValues)
				break
		for obj in self.active_objects:
			if(obj.name == sName):
				obj.SetPhysProperties(vValues)
				break
				
	def store_gizmo_offset(self, vGizmo):
		for obj in self.static_objects:
			if(obj.IsSelected()):
				obj.vCurrPos = obj.movable().selfToWorld().getTranslation() - vGizmo
					
	def enable_physics_debug(self, on):
		for obj in self.static_objects:
			if(obj.bPhys):
				obj.physical(obj.name).enableDebugVisual(on)
		for obj in self.active_objects:
			if(obj.bPhys):
				obj.physical(obj.name).enableDebugVisual(on)
	
	def	find_object(self, objName):
		for obj in self.static_objects:
			if(obj.name == objName):
				return obj
				
#generic class for an object, for when we need to add behavior
class GenericObject(VRScript.Core.Behavior):
	def __init__(self, sName, sMeshName, position, bVis, bPhysics, physicsShape, interact, physicsType):
		VRScript.Core.Behavior.__init__(self, sName)
		#todo - cleanup these property names
		self.name = sName
		self.meshName = sMeshName
		self.vStartPos = VRScript.Math.Vector(position[0], position[1], position[2])
		self.vCurrPos = VRScript.Math.Vector(position[0], position[1], position[2])	#used during animation and also as a gizmo offset
		self.bVisible = bVis
		self.bPhys = bPhysics
		self.physShape = physicsShape
		self.physType = physicsType
		self.bInteract = interact
		self.bAnimating = False
		self.bScripted = False
		self.lastScale = 0
		self.initialPose = VRScript.Math.Matrix()
		self.animType = 0	#0 = trans, 1 = rot, 2 = scale
		self.vAxis = VRScript.Math.Vector(1,0,0)
		self.animationValues = []
		self.lastTime = 0
		self.lastAngle = 0
		self.lastScale = 0.0		#accumulated scale towards current value
		self.physicsValues = []#[3.0, 0.25, 0.9, 1, 0.5]
		self.bb = None				#bounding box created on start
		self.boundingSphere = None	#bounding sphere created on start
		self.bDebug = None			#debug bounding box
		self.debugCount = 0
		self.parentScene = 0		#ptr to LEL Scenario
		self.bGrabbed = False		#is this object currently grabbed?	
		self.isPrimitive = False
		self.matProp = 0
		self.deleted = False
		self.lastRotation = VRScript.Math.Vector(0,0,1)
		self.isFaucetHandle = False
		self.waterName = None
		self.waterOn = False
		self.isDoor = False
		self.isDoorOpen = False
		self.isFactory = False
		self.factoryID = 0
		self.isCardObject = False
		self.cardMeshString = None
		self.cardMeshStringOrder = None
		self.isCard = False
		self.isCardAttached = False
		self.cardParent = None
		self.parentItem = None
		self.placeholderName = None
		self.hitTime = 0		#this is a timer to turn the object static after it has collided with something
		
	def GetLocalBoundsCenter(self):
		c = VRScript.Math.Point(self.bb.center.x, self.bb.center.y, self.bb.center.z)
		hw = VRScript.Math.Vector(self.bb.halfWidth.x, self.bb.halfWidth.y, self.bb.halfWidth.z)
		minTotal = [c.x-hw.x, c.y-hw.y, c.z-hw.z]
		maxTotal = [c.x+hw.x, c.y+hw.y, c.z+hw.z]
		#calculate vector from total bounds center to shoulder center
		boundsCenter = VRScript.Math.Vector((maxTotal[0]+minTotal[0]) * 0.5, (maxTotal[1]+minTotal[1]) * 0.5, (maxTotal[2]+minTotal[2]) * 0.5)
		return boundsCenter
		
	def GetWorldBoundsCenter(self):
		c = VRScript.Math.Point(self.bb.center.x, self.bb.center.y, self.bb.center.z)
		c = c.transform(self.movable().getPose())
		hw = VRScript.Math.Vector(self.bb.halfWidth.x, self.bb.halfWidth.y, self.bb.halfWidth.z)
		hw = hw.transform(self.movable().getPose())
		minTotal = [c.x-hw.x, c.y-hw.y, c.z-hw.z]
		maxTotal = [c.x+hw.x, c.y+hw.y, c.z+hw.z]
		#calculate vector from total bounds center to shoulder center
		boundsCenter = VRScript.Math.Vector((maxTotal[0]+minTotal[0]) * 0.5, (maxTotal[1]+minTotal[1]) * 0.5, (maxTotal[2]+minTotal[2]) * 0.5)
		return boundsCenter
		
	def HasBoundingShape(self):
		return ((len(self.physicals()) > 0) and self.boundingSphere is not None or self.bb is not None)
		
	def IsGrabbed(self):
		return (self.HasBoundingShape() and self.bGrabbed == True and self.deleted == False)
		
	def IsSelected(self):
		return (self.HasBoundingShape() and self.physical(self.name).debugVisualEnabled() and self.deleted == False)
		
	def SetAnimationProperties(self, axis, values, type):
		self.vAxis = VRScript.Math.Vector(axis[0], axis[1], axis[2])
		self.bScripted = True
		self.animType = type
		self.animationValues.extend(values)
		if(self.animType == 1):
			self.valueIndex = 1
		else:
			self.valueIndex = 0
	
	def SetCard(self, bYes):
		self.isCard = bYes
		
	#for kanban
	def SetCardObject(self, bYes, cardMesh, cardMeshOrder):
		self.isCardObject = bYes
		self.cardMeshString = cardMesh
		self.cardMeshStringOrder = cardMeshOrder
	
	#for playing door sound effect
	def SetDoor(self, bYes):
		self.isDoor = bYes
	
	#for kanban
	def SetFactory(self, bYes):
		self.isFactory = bYes
	
	#for playing faucet sound effect
	def SetFaucetHandle(self, bYes, strFaucetName):
		self.isFaucetHandle = bYes
		self.waterName = strFaucetName
		self.bScripted = True
		
	def SetMaterialProperties(self, mat):
		self.matProp = mat
	
	def SetParentScene(self, scene):
		self.parentScene = scene
		
	def SetParent(self, parentName):
		self.parentItem = parentName
	
	def SetPlaceHolderName(self, n):
		self.placeholderName = n
		
	def SetPhysProperties(self, values):
		if(self.bPhys):
			self.physicsValues.extend(values)
	
	def SpawnCard(self, bOnOrder):
		if(self.isCardObject and self.parentScene != None):
			newName = self.name + "_card_" + str(self.factoryID)
			self.factoryID = self.factoryID + 1
			v = self.movable().getPose().getTranslation()
			if(bOnOrder):
				newCard = self.parentScene.create_entity(newName, self.cardMeshString, [v.x, v.y, v.z], True, True, "Box", True, "Kinematic")
				newCard.SetCard(True)
			else:
				newCard = self.parentScene.create_entity(newName, self.cardMeshStringOrder, [v.x, v.y, v.z], True, True, "Box", True, "Kinematic")
				newCard.SetCard(True)
				
			newCard.OnInit(None)
			
	#for kanban - spawns the same object at it's original location after it's done being moved
	def Spawn(self):
		#create a new instance of this object...
		if(self.isFactory and self.parentScene != None):
			newName = self.name + "_" + str(self.factoryID)
			newEnt = self.parentScene.create_entity(newName, self.meshName, [self.vStartPos.x, self.vStartPos.y, self.vStartPos.z], True, True, self.physShape, True, "Static")
			self.parentScene.set_physics_properties(newName, [1.0, 0.25, 0.9, 1, 0.5])
			self.SetFactory(False)
			newEnt.SetFactory(True)
			newEnt.SetParentScene(self.parentScene)
			newEnt.OnInit(None)
			
			if(self.name.find('purple') != -1):
				newPlaceholderName = "placeholder_purple_"+newName
				newPlaceholder = self.parentScene.create_entity(newPlaceholderName, "models\\placeholder_purple_right.ive", [-9.24425168232305,-3.80668043305094,0.341800719102794], False, True, "Box", False, "Static")
				self.parentScene.set_physics_properties(newPlaceholderName, [1.0, 0.25, 0.9, 1, 0.5])
				newPlaceholder.SetParent(newName)
				newPlaceholder.OnInit(None)
			else:
				newPlaceholderName = "placeholder_red_"+newName
				newPlaceholder = self.parentScene.create_entity(newPlaceholderName, "models\\placeholder_red_right.ive", [-9.2223533848255,-3.51940847947684,0.200355804312182], False, True, "Box", False, "Static")
				self.parentScene.set_physics_properties(newPlaceholderName, [1.0, 0.25, 0.9, 1, 0.5])
				newPlaceholder.SetParent(newName)
				newPlaceholder.OnInit(None)
				
			newEnt.SetPlaceHolderName(newPlaceholderName)
			self.factoryID = self.factoryID + 1
			
	def StoreReturnTransform(self):
		self.initialPose = self.movable().getPose()
		
	def RayIntersect(self, start, dir):
		#TODO - other shapes
		hitDist = -1
		origin = [start.x, start.y, start.z]
		vDir = [dir.x, dir.y, dir.z]
		if(self.physShape == "Box"):
			#ray aabb intersection test is done here..
			#this is based on "Woo's Method"
			inside = True
			quadrant = [0,0,0]
			maxT = [0.0, 0.0, 0.0]
			candidatePlane = [0.0, 0.0, 0.0]
			hitPoint = [0.0, 0.0, 0.0]
			RIGHT = 0 
			LEFT = 1
			MIDDLE = 2
			NUM_DIM = 3
			
			#if we don't make a new vector here and transform the center directly, it saves that to the center, so the center then moves..
			c = VRScript.Math.Point(self.bb.center.x, self.bb.center.y, self.bb.center.z)
			c = c.transform(self.movable().getPose())
			hw = VRScript.Math.Vector(self.bb.halfWidth.x, self.bb.halfWidth.y, self.bb.halfWidth.z)
			hw = hw.transform(self.movable().getPose())
			#print(c.x, c.y, c.z)
			#print(hw.x, hw.y, hw.z)

			#box = BoxDebug(c, hw, self.getName()+"_boxDebug" + str(self.debugCount))
			#box.OnInit(None)
			#self.debugCount = self.debugCount + 1
			
			# if(self.bDebug == None):
				# self.bDebug = BoxDebug(c, hw, self.getName()+"_boxDebug")
				# self.bDebug.OnInit(None)
			
			minPt = [c.x-hw.x, c.y-hw.y, c.z-hw.z]
			maxPt = [c.x+hw.x, c.y+hw.y, c.z+hw.z]
			# print("min:")
			# print(minPt[0], minPt[1], minPt[2])
			# print("max:")
			# print(maxPt[0], maxPt[1], maxPt[2])
			
			for i in range(0,NUM_DIM):
				if(origin[i] < minPt[i]):
					quadrant[i] = LEFT
					candidatePlane[i]=minPt[i]
					inside = False
				elif(origin[i] > maxPt[i]):
					quadrant[i] = RIGHT
					candidatePlane[i]=maxPt[i]
					inside = False
				else:
					quadrant[i] = MIDDLE
			
			if(inside):
				#ray is inside of the bounding box
				hitDist = 0
				#print("ray inside")
				return hitDist
			
			for i in range(0, NUM_DIM):
				if(quadrant[i] != MIDDLE and vDir[i] != 0):
					maxT[i] = (candidatePlane[i]-origin[i])/vDir[i]
				else:
					maxT[i] = -1
			
			whichPlane = 0
			for i in range(1, NUM_DIM):
				if(maxT[whichPlane] < maxT[i]):
					whichPlane = i
			
			if maxT[whichPlane] < 0:
				#print("no max T")
				return hitDist
			
			for i in range(0, NUM_DIM):
				if(whichPlane != i):
					hitPoint[i] = origin[i] + (maxT[whichPlane] * vDir[i])
					if(hitPoint[i] < minPt[i] or hitPoint[i] > maxPt[i]):
						#print("false here")
						return hitDist
				else:
					hitPoint[i] = candidatePlane[i]
			
			#print("reached below")
			#calculate distance from hitPoint to origin...
			vToHitPoint = VRScript.Math.Vector(hitPoint[0]-origin[0], hitPoint[1]-origin[1], hitPoint[2]-origin[2])
			hitDist = vToHitPoint.length()
			return hitDist
		elif(self.physShape == "Sphere"):
			c = self.boundingSphere.center
			l = c - start
			s = l.dot(dir)
			l2 = l * l
			r2 = self.boundingSphere.radius * self.boundingSphere.radius
			if(s < 0 and l2 > r2):
				return -1
			m2 = l2-(s*s)
			if(m2 > r2):
				return -1
			q = math.sqrt(r2-m2)
			if(l2 > r2):
				t = s - q
			else:
				t = s + q
			return t
		return 0
		
	def OnInit(self, cbInfo):
		print(self.name)
		print(self.meshName)
		if(self.meshName == "SPHERE"):
			self.attach(VRScript.Core.Renderable(self.name, VRScript.Resources.Sphere(0.05)))
		elif(self.meshName == "BOX"):
			self.attach(VRScript.Core.Renderable(self.name, VRScript.Resources.Box(VRScript.Math.Vector(0.05, 0.05, 0.05), VRScript.Math.Point(0,0,0))))
		elif(self.meshName == "CYLINDER"):
			self.attach(VRScript.Core.Renderable(self.name, VRScript.Resources.Cylinder(0.02, 0.03)))
		elif(self.meshName == "CAPSULE"):
			self.attach(VRScript.Core.Renderable(self.name, VRScript.Resources.Capsule(0.02, 0.03, VRScript.Resources.Axis.Z, VRScript.Math.Point(0,0,0))))
		elif(self.meshName == "PLANE"):
			self.attach(VRScript.Core.Renderable(self.name, VRScript.Resources.Box(VRScript.Math.Vector(1.0,1.0,0.001), VRScript.Math.Vector(0,0,0))))
		else:
			if(self.meshName == "models\\psSink.osg"):
				scaleMat = VRScript.Math.Matrix().makeScale(VRScript.Math.Vector(0.0254,0.0254,0.0254))
				self.attach(VRScript.Core.Renderable(self.name, VRScript.Resources.Mesh(self.name, self.meshName, scaleMat)))
			else:
				self.attach(VRScript.Core.Renderable(self.name, VRScript.Resources.Mesh(self.name, self.meshName)))
			
		self.renderable(self.name).setVisible(self.bVisible)
		m = VRScript.Math.Matrix()
		m.setTranslation(self.vStartPos)
		self.movable().setPose(m)
		self.initialPose = m
		
		print("Made generic object : " + self.name + "\n")
		if(self.bPhys):
			if(self.physShape == "Concave"):
				self.attach(VRScript.Core.Physical(self.name, VRScript.Resources.ConcaveMesh(self.renderable(self.name).getMesh(self.name))))
			elif(self.physShape == "Convex"):
				self.attach(VRScript.Core.Physical(self.name, VRScript.Resources.ConvexMesh(self.renderable(self.name).getMesh(self.name))))
			elif(self.physShape == "Sphere"):
				self.boundingSphere = VRScript.Resources.BoundingSphere(self.renderable(self.name).getMesh(self.name))
				self.attach(VRScript.Core.Physical(self.name, self.boundingSphere))
			elif(self.physShape == "Box"):
				self.bb = VRScript.Resources.BoundingBox(self.renderable(self.name).getMesh(self.name))
				self.attach(VRScript.Core.Physical(self.name, self.bb))
			elif(self.physShape == "Hull"):
				self.attach(VRScript.Core.Physical(self.name, VRScript.Resources.Hull(self.renderable(self.name).getMesh(self.name))))
			elif(self.physShape == "Cylinder"):
				self.attach(VRScript.Core.Physical(self.name, VRScript.Resources.BoundingCylinder(self.renderable(self.name).getMesh(self.name))))
			elif(self.physShape == "Capsule"):
				self.attach(VRScript.Core.Physical(self.name, VRScript.Resources.BoundingCapsule(self.renderable(self.name).getMesh(self.name))))
			elif(self.physShape == "SimpleHull"):
				self.attach(VRScript.Core.Physical(self.name, VRScript.Resources.SimpleHull(self.renderable(self.name).getMesh(self.name))))
			elif(self.physShape == "Plane"):
				self.attach(VRScript.Core.Physical(self.name, VRScript.Resources.Plane()))
			
		if(self.bPhys):
			if(len(self.physicsValues) == 5):
				self.physical(self.name).setPhysicsProperties(VRScript.Core.PhysicsProperties(self.physicsValues[0], self.physicsValues[1], self.physicsValues[2], self.physicsValues[3], self.physicsValues[4]))
			
			if(self.physType == "Static"):
				self.physical(self.name).setCollisionType(VRScript.Core.CollisionType.Static)
			elif(self.physType == "Dynamic"):
				self.physical(self.name).setCollisionType(VRScript.Core.CollisionType.Dynamic)
			elif(self.physType == "Kinematic"):
				self.physical(self.name).setCollisionType(VRScript.Core.CollisionType.Kinematic)
			
			self.physical(self.name).setConstraints(VRScript.Math.Vector(1, 1, 1),VRScript.Math.Vector(1, 1, 1))
			self.physical(self.name).enableDebugVisual(False)
		
			if(self.isCard or self.name.find("bin") != -1):
				print("setting proximity test")
				self.physical(self.name).setProximity(True)
			
		if(self.bInteract):
			self.attach(VRScript.Core.Interactible(self.name, self.renderable('')))
			self.interactible(self.name).enableGrab((self.bScripted==False))
			self.interactible(self.name).enableSelection(True)

		if(self.matProp != 0):
			self.renderable(self.name).setMaterialProperties(self.matProp)
			
		if(self.isFaucetHandle):
			print("Initializing Faucet Handle")
			self.attach(VRScript.Core.Audible('water', 'faucet_loop.wav'))
			self.audible('water').setAudioProperties(VRScript.Core.AudioProperties(1., 1., True))
        
		if(self.isDoor):
			print("Initializing Door")
			self.attach(VRScript.Core.Audible('door_open', 'door_open.wav'))
			self.attach(VRScript.Core.Audible('door_close', 'door_close.wav'))
			
	def OnBeginMove(self, cbInfo, intInfo):
		if(self.bPhys == True):
			self.physical(self.name).setCollisionType(VRScript.Core.CollisionType.Kinematic)
		
		if(self.isCardAttached):
			self.movable().setParent('World')
			self.isCardAttached = False
			
		return True
    
	def OnEndMove(self, cbInfo, intInfo):
		if(self.isFactory):
			#spawn a new object in the original location where this one started..
			self.Spawn()
			#self.physical(self.name).setCollisionType(VRScript.Core.CollisionType.Static)			
			#return True
			
		if(self.bPhys == True):
			if(self.physType != "Kinematic"):
				self.physical(self.name).setCollisionType(VRScript.Core.CollisionType.Dynamic)
		
		if(self.isCard):
			if(self.cardParent != None):
				print("attaching to bin")
				#m = self.movable().selfToEntity(self.cardParent)
				self.movable().setPose(self.initialPose)
				self.movable().setParent(self.cardParent)
				self.isCardAttached = True
				
		return True
	
	def OnProximity(self, cbInfo, ctInfo):
		if (self.isCard and self.isCardAttached == False):
			if(self.cardParent == None):
				#if card is close to a bin
				if(ctInfo.otherEntity.getName().find("bin") != -1):
					#print("testing card prox: " + str(ctInfo.distance))
					if(ctInfo.distance < .3):
						print("close to bin")
						self.cardParent = ctInfo.otherEntity.getName()	#this grabs the parent bin name
						ent = self.parentScene.find_object(ctInfo.otherEntity.getName())
						if(ent.placeholderName != None):
							print("placeholder: " + ent.placeholderName)
						self.initialPose = VRScript.Core.Entity(ent.placeholderName).movable().selfToEntity(self.cardParent)#getPose()
			else:
				if(self.cardParent == ctInfo.otherEntity.getName()):
					if(ctInfo.distance > .3):	#if proximity to the previously attached object is farther
						self.cardParent = None
		
	def OnResetMove(self, cbInfo, user):
		return self.OnEndMove(self, cbInfo, user)
		
	def OnButtonPress(self, cbInfo, btInfo, user):
		if self.isCardObject and self.parentScene != None:
			if btInfo.button == 3:
				print("Spawning card...")
				self.SpawnCard(True)
			elif btInfo.button == 1:
				self.SpawnCard(False)
			
		if self.bScripted:
			#handle some specific scripting first..
			if self.isFaucetHandle:
				if btInfo.button == 0:
					mat = self.movable().getPose()
					v = mat.getTranslation() # Get position
					if self.waterOn == False:# and VRScript.Core.Entity(self.waterName).renderable(self.waterName).isVisible() == False:
						q = VRScript.Math.Quat(0, 0, sin(pi/6), cos(pi/6) )
						self.audible('water').play()
						self.waterOn = True
						VRScript.Core.Entity(self.waterName).renderable(self.waterName).show()
						print("Turning on water...")
					# if faucet is on, turn to the left
					elif self.waterOn == True:
						q = VRScript.Math.Quat(0, 0, sin(5 * pi/6), cos(5 * pi/6) )
						self.waterOn = False
						self.audible('water').stop()
						VRScript.Core.Entity(self.waterName).renderable(self.waterName).hide()
						#self.water.renderable('').setVisible(False)
						print("Turning off water...")
					
					mat.setTranslation(VRScript.Math.Vector(0,0,0)) # Remove position
					mat.postQuat(q) # Rotate
					mat.setTranslation(v) # Put position back in
					self.movable().setPose(mat)
			else:
				if btInfo.button == 0 and self.bAnimating == False:
					#print("Hit Object!\n")
					self.bAnimating = True
					self.lastTime = cbInfo.currentTime
					if self.isDoor:
						if self.isDoorOpen:
							self.audible('door_close').play()
						elif self.isDoorOpen == False:
							self.audible('door_open').play()
		
	def OnCollision(self, cbInfo, intInfo):
		#kanban special case
		if self.getName().find("bin") != -1 or self.isCardObject:
			#we want to turn a bin static after it hits the ground..
			if(self.hitTime == 0):
				self.hitTime = cbInfo.currentTime
				print(str(self.hitTime))
			#self.physical(self.name).setCollisionType(VRScript.Core.CollisionType.Static)			
		# if self.bGrabbed == False:
			# if self.bPhys:
				# if self.getName() == "stray_geometry" or self.getName() == "ground":
					# intInfo.otherComponent.applyImpulse(VRScript.Math.Vector(0.0, 0.0, 0.1), VRScript.Math.Vector(0, 0, 0))
				# elif intInfo.otherEntity.getName() == "stray_geometry" or intInfo.otherEntity.getName() == "ground":
					# intInfo.selfComponent.applyImpulse(VRScript.Math.Vector(0.0, 0.0, 0.1), VRScript.Math.Vector(0, 0, 0))
				
	def OnUpdate(self, cbInfo):
		if(self.hitTime != 0):
			if(cbInfo.currentTime - self.hitTime > 0.5):
				print("Reset to static")
				self.physical(self.name).setCollisionType(VRScript.Core.CollisionType.Static)
				self.hitTime = 0
				
		#general parenting attempt here.. what if the parent isn't loaded yet?  might have to do it on first loop
		if(self.parentItem != None):
			print("\nSetting parent to: " + self.parentItem + "\n")
			mp = self.movable().selfToEntity(self.parentItem)
			#mp = self.movable().entityToSelf(self.parentItem)
			self.initialPose = mp
			self.movable().setPose(mp)
			self.movable().setParent(self.parentItem)
			self.parentItem = None
		
		if self.IsGrabbed() == True:
			if(self.parentScene.rotating):
				#rotation
				m = self.movable().getPose()
				oldTrans = m.getTranslation()
				#when we are close, let's adapt a new-style "trackball" type rotation..
				vHandRight = self.parentScene.skeleton.GetJointPosition(11)
				vToHand = vHandRight - self.parentScene.rotationCenter
				vToHand = vToHand.normalize()			
				
				#determine "radius" of the object
				#handle different physics shapes
				rad = 0
				if(self.bb != None):
					rad = self.bb.halfWidth.x	#for now just use x - eventually we will calculate this to the corner..
				elif(self.boundingSphere != None):
					rad = self.boundingSphere.radius
				
				#vToHand = vToHand * rad	#make the vector the length of the radius of the sphere..
				#vToHand.normalize()
				#lastRotation and current vToHand form a plane through the object's center..
				#the normal of this plane is our rotation axis...
				#we can get the normal of the plane by cross product of the two vectors..
				rotationAxis = vToHand.cross(self.lastRotation)
				rotationAxis = rotationAxis.normalize()
				#print(rotationAxis.x, rotationAxis.y, rotationAxis.z)
				#calculate rotation angle..
				rotationAngle = -math.acos(vToHand.dot(self.lastRotation))
				#print(rotationAngle)
				qw = math.cos(rotationAngle/2)
				qsin = math.sin(rotationAngle/2)
				quatRot = VRScript.Math.Quat(qsin * rotationAxis.x, qsin * rotationAxis.y, qsin * rotationAxis.z, qw)
				quatRot = quatRot.normalize()
				mQuat = m.getQuat()
				mQuat = quatRot * mQuat# * quatRot	#do the latter for local rotation..
				m = m.makeQuat(mQuat)
				m.setTranslation(oldTrans)
				self.movable().setPose(m)
				
				self.lastRotation = vToHand
			elif(self.parentScene.scaling):
				#scale
				m = self.movable().getPose()
				vHands = self.parentScene.skeleton.GetHandCenter()
				#m.setTranslation(vHands-self.GetLocalBoundsCenter())
				#hw = self.bb.halfWidth
				#print(hw.x)
				#currLen = hw.x * 2
				dist = self.parentScene.skeleton.GetHandDistance()
				#TODO - uniform vs. not uniform...
				matScale = VRScript.Math.Matrix().makeScale(VRScript.Math.Vector(1.0 + ((dist / self.parentScene.scaleStartDistance)-1.0), 1.0 + ((dist / self.parentScene.scaleStartDistance)-1.0), 1.0 + ((dist / self.parentScene.scaleStartDistance)-1.0)))
				mat = self.initialPose * matScale
				mat.setTranslation(vHands-self.GetLocalBoundsCenter())
				#mat = m * matScale
				self.movable().setPose(mat)
			elif(self.parentScene.moving):
				#print(self.getName())
				#v = VRScript.Core.Entity('User0Hand').movable().selfToWorld().getTranslation()
				#print(v.x, v.y, v.z)
				#translation
				m = self.movable().selfToWorld()
				vHands = self.parentScene.skeleton.GetHandCenter()
				#print(vHands.x, vHands.y, vHands.z)
				b = self.GetLocalBoundsCenter()
				#print(b.x, b.y, b.z)
				m.setTranslation(vHands-b)
				self.movable().setPose(m)
		elif(self.IsSelected() and self.bGrabbed == False):
			#perform non-grabbed manipulations here..
			if(self.parentScene != 0):
				if(self.parentScene.rotating):
					#rotation
					m = self.movable().getPose()
					#form an coordinate frame based on the skeleton..
					#we want to use the frame when we first say "rotate"
					#matRot = VRScript.Math.Matrix()
					#need to use last pos somehow unless we do it all absolute..
					#vHandRight = self.parentScene.skeleton.GetJointPosition(11)
					#show a "rotation circle" gizmo
					#calculate a vector from the center of the object to hand..
					#vObj = m.getTranslation()
					#vToHand = vHandRight - vObj
					#vToHand = vToHand.normalize()
					#angle = math.degrees(math.acos(vToHand.dot(self.parentScene.rightRotationAxis)))
					#matRot.postAxisAngle(angle, self.parentScene.rotationAxis)
					#matRot.setTranslation(vObj)
					#self.movable().setPose(matRot)
					#then use hands to define angle amount...
				elif(self.parentScene.scaling):
					#scale
					m = self.movable().getPose()
					#vHands = self.parentScene.skeleton.GetHandCenter()
					#dist = self.parentScene.skeleton.GetHandDistance()
					#TODO - uniform vs. not uniform...
					#matScale = VRScript.Math.Matrix().makeScale(VRScript.Math.Vector(1.0 + ((dist / self.parentScene.scaleStartDistance)-1.0), 1.0 + ((dist / self.parentScene.scaleStartDistance)-1.0), 1.0 + ((dist / self.parentScene.scaleStartDistance)-1.0)))
					#mat = self.initialPose * matScale
					#mat.setTranslation(vHands-self.GetLocalBoundsCenter())
					#self.movable().setPose(mat)
				elif(self.parentScene.moving):
					#translation - this case should move the current selection relative to it's offset from the cursor upon when "MOVE" is said
					#print("test")
					m = self.movable().getPose()
					vGizmo = self.parentScene.gizmo.movable().getPose().getTranslation()
					vPos = vGizmo + self.vCurrPos
					m.setTranslation(vPos)
					self.movable().setPose(m)

		#construct matrix to our location
		if self.bAnimating:
		#if self.bScripted:
			#todo - speed controlled by delta value..
			if(self.animType == 0):
				delta = 0.001#(cbInfo.frameTime - self.lastTime) * 0.1
				vSpot = VRScript.Math.Vector(self.movable().getPose().getTranslation())
				#print(str(vSpot.x) + " " + str(vSpot.y) + " " + str(vSpot.z) + "\n")
				vEndSpot = self.vStartPos + VRScript.Math.Vector(self.vAxis * self.animationValues[self.valueIndex])
				#print(str(vEndSpot.x) + " " + str(vEndSpot.y) + " " + str(vEndSpot.z) + "\n")
				vToEnd = VRScript.Math.Vector(vEndSpot - self.vCurrPos)
				vToEnd.normalize()
				vSpot = vSpot + vToEnd * delta;
				#print(str((vSpot-vEndSpot).length()) + "\n")
				if((vSpot-vEndSpot).length() <= 0.005):
					self.bAnimating = False
					self.valueIndex = self.valueIndex + 1
					self.valueIndex = self.valueIndex % len(self.animationValues)
					#reset start position for new value to move to
					self.vCurrPos = vSpot
					
				self.movable().setPose(VRScript.Math.Matrix().setTranslation(vSpot))
				self.lastTime = cbInfo.frameTime
				# if self._open: # closing
					# self.movable().setPose(mat.postAxisAngle(-85.*(1.-alpha), self.vAxis))
				# else: # opening
					# self.movable().setPose(mat.postAxisAngle(-85.*(   alpha), self.vAxis))
			elif(self.animType == 1):
				delta = 0.3
				fDiff = self.animationValues[self.valueIndex] - self.lastAngle
				
				if(fDiff < 0.0):
					delta = -0.3
					
				if(fDiff == 0.0):
					self.lastAngle = 0.3
					
				fDiffAbs = math.fabs(fDiff)
				#print(fDiffAbs)
				if(fDiffAbs < 0.35):
					self.bAnimating = False
					self.valueIndex = self.valueIndex + 1
					self.valueIndex = self.valueIndex % len(self.animationValues)
					
				oldMat = self.movable().getPose()
				mat = VRScript.Math.Matrix()
				mat.setTranslation(oldMat.getTranslation())
				mat.postAxisAngle(self.lastAngle, self.vAxis)
				self.movable().setPose(mat)
				self.lastAngle = self.lastAngle + delta
			elif(self.animType == 2):
				speed = 30	#speed of movement.. (lower = faster)
				#calculate our delta based on the scale target and initial last scale (1.0)
				#scaling..
				nextIndex = self.valueIndex + 1
				nextIndex = nextIndex % len(self.animationValues)
				fScaleTarget = self.animationValues[nextIndex] / self.animationValues[self.valueIndex]
				fScaleDiff = fScaleTarget - 1.0
				
				delta = fScaleDiff / speed
				#print(delta)
				#print("Scale Diff: " + str(fScaleDiff))
				currScaleTarget = self.lastScale + delta
				#print("Curr scale target:" + str(currScaleTarget))
				#print("Last scale: " + str(self.lastScale))
				fDiff = math.fabs(fScaleDiff) - math.fabs(self.lastScale)
				if(fDiff < math.fabs(delta)):
					self.bAnimating = False
					self.valueIndex = self.valueIndex + 1
					self.valueIndex = self.valueIndex % len(self.animationValues)
					self.initialPose = self.movable().getPose()
					self.lastScale = 0.0
				else:	
					matScale = VRScript.Math.Matrix().makeScale(VRScript.Math.Vector(1.0 + (self.vAxis.x * currScaleTarget), 1.0 + (self.vAxis.y * currScaleTarget), 1.0 + (self.vAxis.z * currScaleTarget)))
					mat = self.initialPose * matScale
					self.movable().setPose(mat)
					self.lastScale = currScaleTarget

class WandObject(VRScript.Core.Behavior):
	def __init__(self, sName, sMeshName, mat=VRScript.Math.Matrix()):
		VRScript.Core.Behavior.__init__(self, sName)
		self.meshName = sMeshName
		self.name = sName
		self.transform = mat
		
	def OnInit(self, cbInfo):
		#hide the traditional wand renderable
		wand = VRScript.Core.Entity('User0Hand')
		wand.renderable('User0Hand').hide()
		m = VRScript.Math.Matrix()
		m.postAxisAngle(90.0, VRScript.Math.Vector(1.0, 0.0, 0.0))
		customWandMesh = VRScript.Core.Renderable(self.name, VRScript.Resources.Mesh(self.name, self.meshName, m))
		wand.attach(customWandMesh)
		customWandMesh.show()
		phys = VRScript.Core.Physical(self.name, VRScript.Resources.BoundingBox(customWandMesh.getMesh()))
		phys.setPhysicsProperties(VRScript.Core.PhysicsProperties(15, 0.4, 0.3, 0.3, 0.5))
		phys.setCollisionType(VRScript.Core.CollisionType.Kinematic)
		phys.enableDebugVisual(True)
		wand.attach(phys)
		
	def OnUpdate(self, cbInfo):
		#read controller state
		controller = VRScript.Util.getControllerState()
		# wand = VRScript.Core.Entity('User0Hand')
		# m = wand.movable().selfToWorld()
		# vTrans = VRScript.Math.Vector(m.getTranslation())
		# print(str(vTrans.x))
		# print(str(vTrans.y))
		# print(str(vTrans.z))

class BoxDebug(VRScript.Core.Behavior):
	def __init__(self, c, hw, entity=None):
		VRScript.Core.Behavior.__init__(self,entity)
		self.center = c
		self.halfWidth = hw
		
	def OnInit(self, info):
		#print('r_'+self.getName())
		renderable = VRScript.Core.Renderable('r_'+self.getName(),VRScript.Resources.Box(self.halfWidth, self.center))
		matprops = VRScript.Core.MaterialProperties(util.green,util.green,util.white,util.green,1.0,1.0,1,True)
		renderable.setMaterialProperties(matprops)
		renderable.show()
		self.attach(renderable)

class BoxDebugPhysics(BoxDebug):
	def __init__(self, c, hw, start, dir, entity=None):
		BoxDebug.__init__(self, c+start, hw, entity)
		self.s = start
		self.d = dir
		
	def OnInit(self, info):
		BoxDebug.OnInit(self, info)
		physical = VRScript.Core.Physical(self.getName(), VRScript.Resources.Box(self.halfWidth, self.center + self.s))
		#physprops = VRScript.Core.PhysicsProperties(1,0,0,0,0)
		physical.setPhysicsProperties(util.phys_light)
		physical.setCollisionType(VRScript.Core.CollisionType.Dynamic)
		physical.enableDebugVisual(True)
		self.attach(physical)
		physical.applyImpulse(self.d * 10, VRScript.Math.Vector())