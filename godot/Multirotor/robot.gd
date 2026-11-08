extends Node3D

var drone
@onready var label_x: Label = $"../Label_X"
@onready var label_y: Label = $"../Label_Y"
@onready var label_z: Label = $"../Label_Z"
@onready var label_xr: Label = $"../Label_XR"
@onready var label_yr: Label = $"../Label_YR"
@onready var label_zr: Label = $"../Label_ZR"
@onready var label_time: Label = $"../Label_Time"

@onready var started : bool = false

# Called when the node enters the scene tree for the first time.
func _ready():
	#inizializzazione server
	drone = get_node("drone")
	DDS.subscribe("f1")
	DDS.subscribe("f2")
	DDS.subscribe("f3")
	DDS.subscribe("f4")
	DDS.subscribe("time")

func _process(delta: float) -> void:
	var pose = drone.get_pose()
	var vel = drone.get_velocity()
	var pos = pose[0]
	var att = pose[1]
	var lin_vel = vel[0]
	var rot_vel = vel[1]
	
	label_x.text = "X : %.3f" % [pos.z]
	label_y.text = "Y : %.3f" % [pos.x]
	label_z.text = "Z : %.3f" % [pos.y]
	
	label_xr.text = "XR : %.3f" % [rad_to_deg(att.z)]
	label_yr.text = "YR : %.3f" % [rad_to_deg(att.x)]
	label_zr.text = "ZR : %.3f" % [rad_to_deg(att.y)]
	
	var t = DDS.read("time")
	if t != null:
		label_time.text = "T: %.3f" % [t]
	
	# positions
	DDS.publish("X", DDS.DDS_TYPE_FLOAT, pos.z)
	DDS.publish("Y", DDS.DDS_TYPE_FLOAT, pos.x)
	DDS.publish("Z", DDS.DDS_TYPE_FLOAT, pos.y)
	
	# euler angles
	DDS.publish("TX", DDS.DDS_TYPE_FLOAT, att.z)
	DDS.publish("TY", DDS.DDS_TYPE_FLOAT, att.x)
	DDS.publish("TZ", DDS.DDS_TYPE_FLOAT, att.y)
	
	# linear speeds
	DDS.publish("VX", DDS.DDS_TYPE_FLOAT, lin_vel.z)
	DDS.publish("VY", DDS.DDS_TYPE_FLOAT, lin_vel.x)
	DDS.publish("VZ", DDS.DDS_TYPE_FLOAT, lin_vel.y)

	# angular speeds
	DDS.publish("WX", DDS.DDS_TYPE_FLOAT, rot_vel.z)
	DDS.publish("WY", DDS.DDS_TYPE_FLOAT, rot_vel.x)
	DDS.publish("WZ", DDS.DDS_TYPE_FLOAT, rot_vel.y)
	
	DDS.publish("tick", DDS.DDS_TYPE_FLOAT, delta)
	var f1 = DDS.read("f1")
	var f2 = DDS.read("f2")
	var f3 = DDS.read("f3")
	var f4 = DDS.read("f4")
	drone.set_forces(f1,f2,f3,f4)
	#print(pos.z," ", pos.y)
