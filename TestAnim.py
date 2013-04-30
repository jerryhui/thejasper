import VRScript
import Animation

ghost=Animation.AnimationObject("Ghost")
ghost.LoadAnimation("Ghosts\\005-03end.fbx",[90,0,0],VRScript.Math.Vector(1,1,1))
ghost.Play(VRScript.Core.PlayMode.Loop)