from JasperEngine import *

# The Jasper - A Haunted House for CAVE
# Modeling: Jerry Chen, Natalie Flunker, Hasti Mirkia
# Program: Jerry Hui
#
# Created for DS501, Spring 2013
		
#-------------------------- MAIN PROGRAM --------------------------------------

theJasper = HauntedHouseEngine()

theJasper.create_entity("FirstFloor", "Models\\FirstFloor\\1f.ive", [-11.965188452524,-8.30300893997043,0.521151788013233], True, False, "Concave", False, "Static")
theJasper.create_entity("stairs", "Models\\stairs.osg", [-1.84537044421864,2.88498266908194,0.549046263677154], False, True, "Concave", False, "Static")
theJasper.create_entity("secFloorBoard", "Models\\secFloorBoard.ive", [-11.8793173885138,-5.34976169646222,4.66189630735589], True, True, "Box", False, "Static")
theJasper.create_ground_plane()

ghostMan = theJasper.AddParanormal(Paranormal.Ghost("ghostMan", "ghostman.ive", [0,0,0], "LOOK"))
# ghostMan = theJasper.AddParanormal(Paranormal.GhostFlyaway("ghostManFlyaway", "ghostman.ive", [-1,-2,0], "LOOK"))

theJasper.AddMusic("lux.wav")
VRScript.Interaction.setJumpPoint(0,VRScript.Math.Matrix().setTranslation(VRScript.Math.Vector(-5,-4,0.52115)))