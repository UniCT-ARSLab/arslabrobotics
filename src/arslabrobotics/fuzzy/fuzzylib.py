#
#
#

__all__ = [
    "FuzzySet",
    "Triangle",
    "Down",
    "Up",
    "Variable",
    "FuzzyEngine"
    ]

from arslabrobotics.fuzzy.fuzzyplot import *

class FuzzySet:

    def __init__(self, name, low, high):
        self._low = low
        self._high = high
        self._name = name

    def __repr__(self):
        return str(self._name)

    def name(self):
        return self._name

    def get_limits(self):
        return (self._low, self._high)


class Triangle(FuzzySet):

    def __init__(self, name, low, high, mid = None):
        super().__init__(name, low, high)
        if mid is None:
            self._mid = (self._low + self._high) / 2
        else:
            self._mid = mid

    def fuzzify(self, var):
        if (var > self._high) or (var < self._low):
            return 0.0
        if var == self._mid:
            return 1.0
        if var < self._mid:
            return (var - self._low) / (self._mid - self._low)
        else:
            return (self._high - var) / (self._high - self._mid)


class Down(FuzzySet):

    def __init__(self, name, low, high):
        super().__init__(name, low, high)

    def fuzzify(self, var):
        if var > self._high:
            return 0.0
        if var < self._low:
            return 1.0
        else:
            return 1.0 - (var - self._low) / (self._high - self._low)


class Up(FuzzySet):

    def __init__(self, name, low, high):
        super().__init__(name, low, high)

    def fuzzify(self, var):
        if var > self._high:
            return 1.0
        if var < self._low:
            return 0.0
        else:
            return (var - self._low) / (self._high - self._low)




class FuzzyRule:

    AND = 0
    OR  = 1
    NOT = 2

    def __init__(self, lhs, rhs, typ = AND):
        self._lhs = lhs # [ BoundedVariable ]
        self._rhs = rhs
        self._type = typ
        #print("FuzzyRule:", lhs, rhs)

    def eval(self, debug = False):
        values = [ ]
        for bounded_var in self._lhs:
            values.append(bounded_var.get())
        #print(values)
        ret_val = None
        match self._type:
            case self.AND:
                ret_val = min(values)
            case self.OR:
                ret_val = max(values)
        if debug:
            print("RULE:", end='')
            for v in self._lhs:
                print(v,' ', end='')
            print(">>", self._rhs.fuzzyset().name(), ret_val)
        return ret_val

    def lhs(self):
        return self._lhs

    def rhs(self):
        return self._rhs

    def __and__(self, term):
        self._lhs.append(term)
        return self

    def __rshift__(self, var):
        self._rhs = var
        return self


class BoundedVariable:

    def __init__(self, v, s):
        #print("BoundedVariable", v, s)
        self._variable = v
        self._fuzzyset = s

    def __repr__(self):
        return "%s(%f, %f)" % (self._fuzzyset.name(), \
                               self._variable.get(),
                               self.get())

    def fuzzyset(self):
        return self._fuzzyset

    def variable(self):
        return self._variable

    def eval(self, v):
        self._variable.set(v)
        return self.get()

    def get(self):
        return self._fuzzyset.fuzzify(self._variable.get())

    def __and__(self, term):
        return FuzzyRule([ self, term ], None, FuzzyRule.AND)

    def __rshift__(self, var):
        return FuzzyRule([ self ], var)


class Variable:

    def __init__(self, val = None, name = None):
        self._value = val
        self._name = name

    def __repr__(self):
        if self._name is None:
            return f"V: 0x{id(self):08x}({self._value})"
        else:
            return f"V: {self._name}({self._value})"

    def set(self, v):
        self._value = v

    def get(self):
        return self._value

    def __call__(self, fuzzyset):
        return BoundedVariable(self, fuzzyset)


class FuzzyEngine:

    STEPS = 100.0

    COG = 0
    FOM = 1
    LOM = 2
    MOM = 3

    def __init__(self):
        self.plot = False
        self.mode = self.COG
        self.debug = False

    def use_cog(self):
        self.mode = self.COG

    def use_mom(self):
        self.mode = self.MOM

    def use_fom(self):
        self.mode = self.FOM

    def use_lom(self):
        self.mode = self.LOM

    def _centroid(self, bounded_varset):
        lows = []
        highs = []
        for var, val in bounded_varset:
            (low, high) = var.fuzzyset().get_limits()
            lows.append(low)
            highs.append(high)

        low = min(lows)
        high = max(highs)
        #print(low, high)

        increment = (high - low) / self.STEPS
        value = low
        num = 0.0
        den = 0.0
        if self.plot:
            X = []
            Y = []
        while value <= high:
            #print("Value: ", value)
            max_fuzzy_value = 0.0
            for rhs_var, fuzzy_val in bounded_varset:
                output_fuzzy_val = rhs_var.eval(value)
                if output_fuzzy_val > fuzzy_val:
                    output_fuzzy_val = fuzzy_val
                max_fuzzy_value = max(max_fuzzy_value, output_fuzzy_val)
                #print(rhs_var, fuzzy_val, output_fuzzy_val, max_fuzzy_value)
            if self.plot:
                X.append(value)
                Y.append(max_fuzzy_value)
            num += value * max_fuzzy_value
            den += max_fuzzy_value
            value += increment

        if den == 0:
            output = 0.0
        else:
            output = num / den

        if self.plot:
            plot_set(X, [Y], points = [ (output, 0) ], title = "Output")

        return output


    def _defuzzify(self, bounded_varset):
        lows = []
        highs = []
        for var, val in bounded_varset:
            (low, high) = var.fuzzyset().get_limits()
            lows.append(low)
            highs.append(high)

        low = min(lows)
        high = max(highs)
        #print(low, high)

        increment = (high - low) / self.STEPS
        value = low
        fom = None
        lom = None
        X = []
        Y = []
        while value <= high:
            #print("Value: ", value)
            overall_fuzzy_value = 0.0
            for rhs_var, clipped_fuzzy_val in bounded_varset:
                output_fuzzy_val = rhs_var.eval(value)
                if output_fuzzy_val > clipped_fuzzy_val:
                    output_fuzzy_val = clipped_fuzzy_val
                overall_fuzzy_value = max(overall_fuzzy_value, output_fuzzy_val)
                #print(rhs_var, fuzzy_val, output_fuzzy_val, max_fuzzy_value)
            X.append(value)
            Y.append(overall_fuzzy_value)
            value += increment

        num = 0.0
        den = 0.0
        maximum = max(Y)
        #print("X=",X)
        #print("Y=",Y)
        for i in range(len(X)):
            x = X[i]
            y = Y[i]
            num += x * y
            den += y
            #print(num, " ", den)
            if fom is None:
                if y == maximum:
                    fom = x
                    lom = x
            else:
                if y == maximum:
                    lom = x

        #print("num, den = ", num, " ", den)

        match self.mode:
            case self.COG:
                if den == 0:
                    output = 0.0
                else:
                    output = num / den

            case self.MOM:
                output = (lom + fom) / 2

            case self.LOM:
                output = lom

            case self.FOM:
                output = fom

        if self.plot:
            plot_set(X, [Y], points = [ (output, 0) ], title = "Output")

        return output


    def execute(self, *rule_set):
        varset = { } # { Variable : [ BoundedVariable ] }
        for r in rule_set:
            # the output of the rule
            fuzzy_output_val = r.eval(self.debug)
            # the right hand side (a bounded variable)
            rhs = r.rhs()
            var = rhs.variable()
            fuzzyset = rhs.fuzzyset()
            #print(var, fuzzy_output_val, fuzzyset)
            if var in varset:
                found = False
                # check if the bounded var (name + concept) is already present in the list
                # in this case it is an OR operator
                for i in range(len(varset[var])):
                    couple = varset[var][i]
                    if couple[0].fuzzyset() == fuzzyset:
                        # the concept is already present
                        fuzzy_output_val = max(fuzzy_output_val, couple[1])
                        varset[var][i] = (rhs, fuzzy_output_val)
                        found = True
                        break
                if not(found):
                    varset[var].append( (rhs, fuzzy_output_val) )
            else:
                varset[var] = [ (rhs, fuzzy_output_val) ]
        #print(varset)
        if self.debug:
            print("OUTPUT:")
        self.output_varset = { }
        for v in varset:
            output_value = self._defuzzify(varset[v])
            self.output_varset[v] = output_value
            if self.debug:
                print("  VAR:", v)
                for var, val in varset[v]:
                    print("    ", var.fuzzyset().name(), " ", val)
                print("  VALUE:", output_value)
        #print(self.output_varset)

    def get(self, var):
        return self.output_varset[var]


