import Paranormal

casper = Paranormal.Ghost("Casper",[0,0,0],"Check")
evilsoup = Paranormal.EvilSoup("Cucumber",[1,1,3],"Spill")

print "\nTry kicking"
casper.capture("Kick")

print "\nTry checking"
casper.capture("Check")

print "\nIs Casper a Paranormal?"
print isinstance(casper, Paranormal.Paranormal)

print "\nIs Casper a Ghost?"
print isinstance(casper, Paranormal.Ghost)

print "\nIs Cucumber a ghost?"
print isinstance(evilsoup, Paranormal.Ghost)