#
#
#
import arslabrobotics as ar

_instance = None

def create():
    dds = ar.dds.DDS()
    dds.start()
    global _instance
    _instance = dds

def publish(name,term):
    global _instance
    _instance.publish(name, term, ar.dds.DDS_TYPE_JSON)

def dbg(p):
    print(p)

