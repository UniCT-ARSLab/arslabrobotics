extends Button

func _pressed() -> void:
	DDS.publish("start", DDS.DDS_TYPE_INT, 1)
