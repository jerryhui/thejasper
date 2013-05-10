import VRScript
import Animation

ghost=Animation.AnimationObject("Ghost")
ghost.LoadAnimation("Models\\Monsters\\baked\\05-03.fbx",[90,0,0],VRScript.Math.Vector(1,1,1))
ghost.Play(VRScript.Core.PlayMode.Loop)
