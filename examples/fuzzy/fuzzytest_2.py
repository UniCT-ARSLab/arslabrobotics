#
#
#
import sys

sys.path.insert(0, "../../")

from lib.fuzzy.fuzzylib import *
from lib.fuzzy.fuzzyplot import *

if __name__ == "__main__":
    # temperature
    cold = Down(0, 15, "Cold")
    medium = Triangle(10, 30, "Medium")
    hot = Up(25, 40, "Hot")

    # humidity
    low = Down(0, 70, "Low")
    high = Up(50, 100, "High")

    # fan speed
    slow = Down(0, 30, "Slow")
    med = Triangle(20, 80, "Medium")
    fast = Triangle(70, 95, "Fast")
    very_fast = Up(90, 100, "Very Fast")

    plot_fuzzysets([low, high], title = "Humidity")
    plot_fuzzysets([cold, medium, hot], title = "Temperature")
    plot_fuzzysets([slow, med, fast, very_fast], title = "Fan Speed %")

    temperature = Variable(32)
    humidity = Variable(90)

    fan = Variable()

    r1 = (temperature(hot) & humidity(low) ) >> fan(med)
    r2 = (temperature(hot) & humidity(high) ) >> fan(very_fast)
    r3 = (temperature(medium) & humidity(low) ) >> fan(med)
    r4 = (temperature(medium) & humidity(high) ) >> fan(fast)
    r5 = temperature(cold) >> fan(slow)

    print("R1: FAN MEDIUM:", r1.eval())
    print("R2: FAN VERY_FAST:", r2.eval())
    print("R3: FAN MEDIUM:", r3.eval())
    print("R4: FAN FAST:", r4.eval())
    print("R5: FAN SLOW:", r5.eval())

    e = FuzzyEngine()
    e.plot = True
    e.execute(r1,r2,r3,r4,r5)
    print("fan speed:", e.get(fan))


