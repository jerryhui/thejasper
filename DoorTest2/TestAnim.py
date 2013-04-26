import VRScript
import Animation

ghost=Animation.AnimationObject("Ghost")
ghost.LoadAnimation("003-02.fbx",VRScript.Math.Vector(1,1,1),0,VRScript.Math.Vector(1,0,0))
ghost.Play(VRScript.Core.PlayMode.Loop)