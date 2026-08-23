extends Node3D

@onready var joint_1: RigidBody3D = $Base/Joint1

func _ready() -> void:
	DDS.subscribe("torque")
	
func _physics_process(_delta: float) -> void:
	var t = DDS.read("torque")
	if t != null:
		joint_1.apply_torque(Vector3(0,0,t))

func _process(_delta: float) -> void:
	var theta = joint_1.rotation.y + PI/2
	var omega = joint_1.angular_velocity.z
	DDS.publish("angle", DDS.DDS_TYPE_FLOAT, theta)
	DDS.publish("speed", DDS.DDS_TYPE_FLOAT, omega)
