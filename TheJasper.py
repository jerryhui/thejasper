from JasperEngine import *

# The Jasper - A Haunted House for CAVE
# Modeling: Jerry Chen, Natalie Flunker, Hasti Mirkia
# Program: Jerry Hui
#
# Created for DS501, Spring 2013
		
#-------------------------- MAIN PROGRAM --------------------------------------

theJasper = HauntedHouseEngine()

theJasper.create_entity("fullHouse", "Models\\bigHouse.ive", [0,0,0], True, True, "Concave", False, "Static")
theJasper.create_ground_plane()

ghostMan = theJasper.AddParanormal(Paranormal.Ghost("ghostMan", "ghostman.ive", [0,0,0], "LOOK"))
ghostMan = theJasper.AddParanormal(Paranormal.GhostFlyaway("ghostManFlyaway", "ghostman.ive", [-1,-2,0], "LOOK"))

theJasper.AddMusic("lux.wav")