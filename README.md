The Jasper - A Haunted House for CAVE
=====================================
Modeling: Jerry Chen, Natalie Flunker, Hasti Mirkia

Program: Jerry Hui

Created for DS501, Spring 2013

TASK LIST
=========
## MUST DO
- [ ] put in ghosts and monsters and stuff
- [ ] doors (and others?) are slightly off

## NICE TO HAVE
- [ ] turn on/off physics for doors?
- [ ] *Crawler* (creature moves randomly using Physics engine)
- [ ] *Lurcher* captured animation

## PIPE DREAM
- [ ] Wiimote/Kinect controls
- [ ] *Door* objects opened by physics engine

DEV LOG
=======
## 2013/05/10
- [x] *Paranormal* with FBX hacked

## 2013/05/09
- [x] Fixed PHYSICS: by HULL on CONCAVE
- [x] Fixed: Collision sound FX needs to stop! Distance damping not working
- [x] provide pre-rotation to objects (doors!)
- [x] add Jerry C's house shell
- [x] REMOVED: Lobby door positions: touching, but now can't walk through
- [x] *Paranormal* add rotation to some monsters
- [x] *Paranormal* staring works correctly!
- [x] Fixed: status text broke
- [x] *Lurcher* and *SkeletonBiker* finished

## 2013/05/08
- [x] landscape location; might be fixed through rebake in meter
- [ ] put in some doors and interactive objects (some problems)

## 2013/05/07
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