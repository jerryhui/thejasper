The Jasper - A Haunted House for CAVE
=====================================
Modeling: Jerry Chen, Natalie Flunker, Hasti Mirkia

Program: Jerry Hui

Created for DS501, Spring 2013

DEV LOG

## 2013/05/06
### FINISHED
- [x] *Paranormal* now has a staring option
- [x] *Lurcher* (creature that moves forward) first implementation (not yet tested)
- [x] *Door* extended so that groups of doors (usually double doors) can be opened/closed at the same time

### TO Do
- [ ] *Lurcher* test
- [ ] *Crawler* (creature moves using Physics engine)

## 2013/05/04
### FINISHED
- [x] *Paranormal* class now detects User0 and trigges _OnUserProximity()_
- [x] Game stats text distance fix
- [x] *Paranormal* initial states now handled correctly

### TO DO
- [ ] *Paranormal* rotation

## 2013/05/03
### FINISHED
- [x] Modularizing code to JasperEngine.py
- [x] Game stats text not showing up on DEV wall (fixed; head tracker was on backwards)
- [x] Sound will dim as user goes further away

### PROBLEM
- [ ] _OnProximity()_ with user is on but position is not correct