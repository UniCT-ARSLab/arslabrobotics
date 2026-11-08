extends Button

@onready var robot: Node3D = $"/root/World/Robot"

func _ready() -> void:
	pressed.connect(on_start)
	
func on_start():
	DDS.publish('start', DDS.DDS_TYPE_INT, 0)
