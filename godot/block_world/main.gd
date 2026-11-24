extends Node3D

@onready var red_box: RigidBody3D = $RedBox
@onready var green_cylinder: RigidBody3D = $GreenCylinder
@onready var blue_cone: RigidBody3D = $BlueCone
@onready var yellow_prism: RigidBody3D = $YellowPrism

var objects = {}

func _ready() -> void:
	DDS.subscribe("command")
	objects["cube"] = red_box
	objects["cone"] = blue_cone
	objects["prism"] = yellow_prism
	objects["cylinder"] = green_cylinder
	
func _process(delta: float) -> void:
	var data = DDS.read("command")
	if typeof(data) != TYPE_ARRAY:
		return
	if data != null:
		print(data)
		var cmd = data[0]
		if cmd == "pick":
			var obj_name = data[1]
			if objects.get(obj_name) != null:
				var obj = objects[obj_name]
				obj.visible = false
		elif cmd == "put":
			var obj_name = data[1]
			var x = data[2]
			var z = data[3]
			if objects.get(obj_name) != null:
				var obj = objects[obj_name]
				obj.global_position.x = x
				obj.global_position.y = z
				obj.global_position.z = 0
				obj.visible = true
		DDS.subscribed_vars["command"] = null
