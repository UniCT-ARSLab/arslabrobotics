#
#
#

import arslabrobotics as ar

if __name__ == "__main__":
    cold = ar.fuzzy.Down(0, 15, "Cold")
    medium = ar.fuzzy.Triangle(10, 30, "Medium")
    hot = ar.fuzzy.Up(25, 40, "Hot")

    slow = ar.fuzzy.Down(0, 30)
    med = ar.fuzzy.Triangle(20, 80)
    fast = ar.fuzzy.Up(70, 100)

    #plot_fuzzysets([slow, med, fast])

    t = input("Enter temperature: ")

    ar.fuzzy.plot_fuzzysets([cold, medium, hot])

    temperature = ar.fuzzy.Variable(float(t))

    fan = ar.fuzzy.Variable()

    r1 = temperature(hot) >> fan(fast)
    r2 = temperature(medium) >> fan(med)
    r3 = temperature(cold) >> fan(slow)

    print("FAN FAST:", r1.eval())
    print("FAN MEDIUM:", r2.eval())
    print("FAN SLOW:", r3.eval())

    e = ar.fuzzy.FuzzyEngine()
    e.plot = True
    e.execute(r1,r2,r3)
    print("fan speed:", e.get(fan))


