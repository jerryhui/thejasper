from JasperEngine import *
from Paranormal import ParanormalState

# The Jasper - A Haunted House for CAVE
# Modeling: Jerry Chen, Natalie Flunker, Hasti Mirkia
# Program: Jerry Hui
#
# Created for DS501, Spring 2013
		
#-------------------------- MAIN PROGRAM --------------------------------------
theJasper = HauntedHouseEngine()

houseCoord = [-12.7, 2.25, 0]
landscapeCoord = [-12.7, 2.25, 0]
# landscapeCoord = [-12.7, 2.25, -0.53]

# ----- House
# Baked models
theJasper.create_entity("fullHouse", "Models\\final.ive", houseCoord, True, False, "Concave", False, "Static")
theJasper.create_entity("landscape", "Models\\landscape.ive", landscapeCoord, True, True, "Concave", False, "Static")
theJasper.create_entity("houseShell", "Models\\houseShell.ive", landscapeCoord, True, False, "Concave", False, "Static")
# simple model for physics
housePhysics = theJasper.create_entity("simpleHouse", "Models\\finalBlock.ive", houseCoord, False, True, "Concave", False, "Static")
theJasper.set_physics_properties("simpleHouse", [200.0, .999, 0.9, 1, 0.5])

# ----- Ghosts, monsters, skeletons
# theJasper.AddParanormal(Paranormal.Paranormal("skeletonOnBikeInBR2", "skeletonbike.ive", [-3.821926779942078,-0.02519086368957,4.73999994634175], "LOOK"))
# theJasper.AddParanormal(Paranormal.Ghost("ghostInBedroom1", "CindyTheGhost.ive", [-1.2927387500326,8.09640865143285,4.7399999463417], "LOOK"))
# theJasper.AddParanormal(Paranormal.Ghost("ghostInBR3", "BuffGhost.ive", [-5.019329190944399,2.959249310276058,4.73999994634174], "LOOK"))
# theJasper.AddParanormal(Paranormal.Ghost("ghostInBR4", "ChandlerTheGhost.ive", [1.845351989480601,3.57564352203617,4.73999994634175], "LOOK"))
# theJasper.AddParanormal(Paranormal.Ghost("restaurantGhost", "DevilGhost.ive", [-11.926308249188269,10.63719549574259,0.309999999879134], "LOOK"))
# fireMonster = theJasper.AddParanormal(Paranormal.Paranormal("FireMonster", "firemon-hidden.fbx", [4.831614595697602,14.3279551695073,1.75867120879058], "LOOK", ParanormalState.Discovered))
# fireMonster.SetDiscoveredAnimation("firemon-hidden.fbx",VRScript.Core.PlayMode.Loop,[90,0,0])
# fireMonster.SetDiscoveredSound("AudioFiles\\Fire.wav")
# fireMonster.SetCapturedAnimation("firemon-captured.fbx",VRScript.Core.PlayMode.Loop,[90,0,0])

# ----- Doors, furniture
# MainDoorLeft = theJasper.AddObject(HouseObjects.Door("MainDoorLeft", "Furniture\\lobby-door-left.ive", [-4.795,-0.712,0.125], True, -90))
# MainDoorRight = theJasper.AddObject(HouseObjects.Door("MainDoorRight", "Furniture\\lobby-door-right.ive", [-2.915,-0.712,0.125], True, 90))
# MainDoorLeft.AddSlaveDoor(MainDoorRight)

# theJasper.AddObject(HouseObjects.Door("BR1Door", "Furniture\\brDoor.ive", [-1.950541497481799,11.9752809323588,4.5], True, -90))
# door = theJasper.AddObject(HouseObjects.Door("BR2Door", "Furniture\\brDoor.ive", [-4.858116923442199,7.54166174274206,4.5], True, -90))
# door.SetPreEuler([-180,0,0])
# theJasper.AddObject(HouseObjects.Door("BR3Door", "Furniture\\brDoor.ive", [-1.950541497481799,6.95758311744,4.5], True, -90))
# door = theJasper.AddObject(HouseObjects.Door("BR4Door", "Furniture\\brDoor.ive", [-4.858116923442199,2.563359678464464,4.5], True, -90))
# door.SetPreEuler([-180,0,0])
# theJasper.AddObject(HouseObjects.Door("BR1BathDoor", "Furniture\\brDoor.ive", [-1.341027110955999,8.93479536299549,4.5], True, -90))
# theJasper.AddObject(HouseObjects.Door("BR2BathDoor", "Furniture\\brDoor.ive", [-6.351631299284609,10.59214731198452,4.5], True, -90))
# theJasper.AddObject(HouseObjects.Door("BR3BathDoor", "Furniture\\brDoor.ive", [-1.311631360193999,3.93479542342146,4.5], True, -90))
# theJasper.AddObject(HouseObjects.Door("BR4BathDoor", "Furniture\\brDoor.ive", [-6.391027049925829,5.592147372410491,4.5], True, -90))

doorCoords = [
	[-1.950541497481799,11.9752809323588,4.5],	#BR 1 Door
	[-4.858116923442199,7.54166174274206,4.5],	#BR 2 Door
	[-1.950541497481799,6.95758311744,4.5],		#BR 3 Door
	[-4.858116923442199,2.563359678464464,4.5],	#BR 4 Door
	[-1.341027110955999,8.93479536299549,4.5],	#BR 1 Bathroom Door
	[-6.351631299284609,10.59214731198452,4.5],	#BR 2 Bathroom Door
	[-1.311631360193999,3.93479542342146,4.5],	#BR 3 Bathroom Door
	[-6.391027049925829,5.592147372410491,4.5]	#BR 4 Bathroom Door
]
doorPreangles = [0, -180, 0, -180, 0,0,0,0]
theJasper.Factory("door", doorCoords, doorPreangles)

theJasper.AddObject(HouseObjects.BumpableObj("victorianChair", "Furniture\\chair001.ive",[1.5115688278029,9.07393871938339,5],"ChairKick.wav",[20.0, 0.9, 0.9, 1, 0.5]))
theJasper.AddObject(HouseObjects.BumpableObj("rockingChair", "Furniture\\chair001.ive",[-8.09177704353456,9.02558333223351,5],"ChairKick.wav",[20.0, 0.9, 0.9, 1, 0.5]))
theJasper.AddObject(HouseObjects.BumpableObj("antiqueChest", "Furniture\\chest.ive",[-9.88431257446918,4.293953274490081,5],"ChairKick.wav",[50.0, 0.9, 0.9, 1, 0.5]))

bottleCoords = [
	[-10.25991536527329,8.400711394023599,0.3],
	[-16.01995635091231,9.00775796055716,0.3],
	[-14.43351674990468,13.9358127318157,0.3],
	[-13.98054427526906,3.7847971945648,0.3]
]

theJasper.Factory("bottle", bottleCoords)

# ----- Background music
theJasper.AddMusic("ligeti-lux.wav")
theJasper.AddMusic("ligeti-atmospheres.wav")
# VRScript.Interaction.setJumpPoint(0,VRScript.Math.Matrix().setTranslation(VRScript.Math.Vector(0,0,0)))