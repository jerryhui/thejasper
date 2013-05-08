The Jasper - A Haunted House for CAVE
=====================================
Modeling: Jerry Chen, Natalie Flunker, Hasti Mirkia

Program: Jerry Hui

Created for DS501, Spring 2013

TASK LIST
=========
## MUST DO
- [ ] put in doors and interactive objects
- [ ] *Lurcher* test (adding Physical().zeroMotion())
- [ ] landscape location; might be fixed through rebake in meter

## NICE TO HAVE
- [ ] self-close main doors behind user
- [ ] *Crawler* (creature moves randomly using Physics engine)

## PIPE DREAM
- [ ] Wiimote/Kinect controls
- [ ] *Door* objects opened by physics engine

DEV LOG
=======
## 2013/05/17
- [x] Load baked model for view plus simple model for physics
- [x] *EnvObject* now fades in/out status text
- [x] *BumpableObj* gets kicked when interacting
- [x] *Door* slaves tested
- [x] check physics/model line-up

## 2013/05/06
- [x] *Paranormal* now has a staring option
- [x] *Lurcher* (creature that moves forward) first implementation (not yet tested)
- [x] *Door* extended so that groups of doors (usually double doors) can be opened/closed at the same time
- [x] *ProxTrigger* triggers a set of functions (no param) when user breaches a given distance

## 2013/05/04
- [x] *Paranormal* class now detects User0 and triggers custom event _OnUserProximity()_
- [x] Game stats text distance fix
- [x] *Paranormal* initial states now handled correctly

## 2013/05/03
- [x] Modularizing code to JasperEngine.py
- [x] Game stats text not showing up on DEV wall (fixed; head tracker was on backwards)
- [x] Sound will dim as user goes further away