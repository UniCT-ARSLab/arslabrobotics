extends Control

@onready var cart_node: Node2D = $cart
@onready var pivot_node: Node2D = $cart/pivot
@onready var telemetry: Label = $telemetry_label
# Called when the node enters the scene tree for the first time.

var t : float = 0
var x: float = 0
var phi: float = 0 

func _ready() -> void:
	DDS.subscribe("position")
	DDS.subscribe("angle")
	cart_node.position.x = 0 


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	t += delta
	#DDS.publish("tick", DDS.DDS_TYPE_FLOAT, delta)
	
	telemetry.text = "t = %.3f seconds\np = %.3f meters\nphi = %.3f deg" % \
		[t, x, rad_to_deg(phi)]
	
	var p = DDS.read("position")
	if p != null:
		#print(v)
		x = p
		#p = p * 1000
		#cart_node.position.x = x0 + (p * pixels_per_meter)
		cart_node.position.x = p * 500
		
	var phi_temp = DDS.read("angle")
	if phi_temp != null:
		phi = phi_temp
		pivot_node.rotation = -phi 
	#var degrees = phi * 180 / 3.14159
	
