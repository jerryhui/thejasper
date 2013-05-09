from JasperEngine import *
import time

# The Jasper - A Haunted House for CAVE
# Modeling: Jerry Chen, Natalie Flunker, Hasti Mirkia
# Program: Jerry Hui
#
# Created for DS501, Spring 2013
		
#-------------------------- MAIN PROGRAM --------------------------------------
timestamp_start = time.time()

theJasper = HauntedHouseEngine()

houseCoord = [-12.7, 2.25, 0]
landscapeCoord = [-12.7, 2.25, 0]
# landscapeCoord = [-12.7, 2.25, -0.53]

# ----- House
# Baked models
# theJasper.create_entity("fullHouse", "Models\\final.ive", houseCoord, True, False, "Concave", False, "Static")
theJasper.create_entity("landscape", "Models\\landscape.ive", landscapeCoord, True, True, "Concave", False, "Static")
# simple model for physics
housePhysics = theJasper.create_entity("simpleHouse", "Models\\finalSimplified.ive", houseCoord, True, True, "Concave", False, "Static")
theJasper.set_physics_properties("simpleHouse", [200.0, .999, 0.9, 1, 0.5])

# ----- Ghosts, monsters, skeletons
theJasper.AddParanormal(Paranormal.Paranormal("skeletonOnBike", "skeletonbike.ive", [0.1946421524363,102.529022018229,5.64167194396309], "LOOK"))

# ghostMan = theJasper.AddParanormal(Paranormal.Ghost("ghostMan", "ghostman.ive", [0,0,0], "LOOK"))
# ghostMan = theJasper.AddParanormal(Paranormal.GhostFlyaway("ghostManFlyaway", "ghostman.ive", [-1,-2,0], "LOOK"))

# ----- Doors, furniture
MainDoorLeft = theJasper.AddObject(HouseObjects.Door("MainDoorLeft", "Furniture\\lobby-door-left.ive", [-4.795,-0.712,0.125], True, -90))
MainDoorRight = theJasper.AddObject(HouseObjects.Door("MainDoorRight", "Furniture\\lobby-door-right.ive", [-2.915,-0.712,0.125], True, 90))
MainDoorLeft.AddSlaveDoor(MainDoorRight)

theJasper.AddObject(HouseObjects.Door("BR1Door", "Furniture\\brDoor.ive", [-1.950541497481799,11.9752809323588,4.5], True, -90))
door = theJasper.AddObject(HouseObjects.Door("BR2Door", "Furniture\\brDoor.ive", [-4.858116923442199,7.54166174274206,4.5], True, -90))
door.SetPreEuler([-180,0,0])
theJasper.AddObject(HouseObjects.Door("BR3Door", "Furniture\\brDoor.ive", [-1.950541497481799,6.95758311744,4.5], True, -90))
door = theJasper.AddObject(HouseObjects.Door("BR4Door", "Furniture\\brDoor.ive", [-4.858116923442199,2.563359678464464,4.5], True, -90))
door.SetPreEuler([-180,0,0])
theJasper.AddObject(HouseObjects.Door("BR1BathDoor", "Furniture\\brDoor.ive", [-1.341027110955999,8.93479536299549,4.5], True, -90))
theJasper.AddObject(HouseObjects.Door("BR2BathDoor", "Furniture\\brDoor.ive", [-6.351631299284609,10.59214731198452,4.5], True, -90))
theJasper.AddObject(HouseObjects.Door("BR3BathDoor", "Furniture\\brDoor.ive", [-1.311631360193999,3.93479542342146,4.5], True, -90))
theJasper.AddObject(HouseObjects.Door("BR4BathDoor", "Furniture\\brDoor.ive", [-6.391027049925829,5.592147372410491,4.5], True, -90))

theJasper.AddObject(HouseObjects.BumpableObj("victorianChair", "Furniture\\chair001.ive",[1.5115688278029,9.07393871938339,7.33374701944853],"ChairKick.wav"))
theJasper.AddObject(HouseObjects.BumpableObj("rockingChair", "Furniture\\chair001.ive",[-8.09177704353456,9.02558333223351,5],"ChairKick.wav"))
theJasper.AddObject(HouseObjects.BumpableObj("antiqueChest", "Furniture\\chest.ive",[-9.88431257446918,4.293953274490081,5],"ChairKick.wav"))

theJasper.AddObject(HouseObjects.BumpableObj("bottle1", "Furniture\\bottle.ive",[-10.25991536527329,8.400711394023599,0.3],"GlassCrashing.wav"))
theJasper.AddObject(HouseObjects.BumpableObj("bottle2", "Furniture\\bottle.ive",[-16.01995635091231,9.00775796055716,0.3],"GlassCrashing.wav"))
theJasper.AddObject(HouseObjects.BumpableObj("bottle3", "Furniture\\bottle.ive",[-14.43351674990468,13.9358127318157,0.3],"GlassCrashing.wav"))
theJasper.AddObject(HouseObjects.BumpableObj("bottle4", "Furniture\\bottle.ive",[-13.98054427526906,3.7847971945648,0.3],"GlassCrashing.wav"))

theJasper.AddMusic("ligeti-lux.wav")
theJasper.AddMusic("ligeti-atmospheres.wav")
VRScript.Interaction.setJumpPoint(0,VRScript.Math.Matrix().setTranslation(VRScript.Math.Vector(-5,4,0)))

print("Finished loading The Jasper in {0} seconds.".format(time.time()-timestamp_start))