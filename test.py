import paranormal

casper = paranormal.Ghost("Casper",[0,0,0],"Check")
evilsoup = paranormal.EvilSoup("Cucumber",[1,1,3],"Spill")

print "\nTry kicking"
casper.capture("Kick")

print "\nTry checking"
casper.capture("Check")

print "\nIs Casper a Paranormal?"
print isinstance(casper, paranormal.Paranormal)

print "\nIs Casper a Ghost?"
print isinstance(casper, paranormal.Ghost)

print "\nIs Cucumber a ghost?"
print isinstance(evilsoup, paranormal.Ghost)