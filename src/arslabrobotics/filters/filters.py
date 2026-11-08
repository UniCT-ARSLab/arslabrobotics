#
# filters.py
#

import numpy as np
import scipy.signal as sig

from arslabrobotics.identification.arx import ARXModel

class LowPassFilter:

    def __init__(self, fcut, fsample):
        """
        A class that implements a low-pass filter of the first order

        :param fcut: Cut-off Frequency
        :param fsample: Sampling Frequency

        """
        f = fcut / fsample
        self.alpha = (2*np.pi*f)/(1 + 2*np.pi*f)
        a = [ - (1 - self.alpha)]
        b = [ self.alpha ]
        self.filter = ARXModel(a, b)


    def evaluate(self, _in):
        """
        Evaluates the filter

        :param _input: the input
        :return: the output
        """
        return self.filter.evaluate(_in)



class HighPassFilter:

    def __init__(self, fcut, fsample):
        """
        A class that implements a high-pass filter of the first order

        :param fcut: Cut-off Frequency
        :param fsample: Sampling Frequency

        """
        alpha = 1/(1 + 2*np.pi*fcut/fsample)
        a = [ - alpha]
        b = [ alpha, - alpha ]
        self.filter = ARXModel(a, b)


    def evaluate(self, _in):
        """
        Evaluates the filter

        :param _input: the input
        :return: the output
        """
        return self.filter.evaluate(_in)


class BandPassFilter:

    def __init__(self, fcut_1, fcut_2, fsample):
        """
        A class that implements a band-pass filter of the first order

        :param fcut_1, fcut_2: Cut-off Frequencies
        :param fsample: Sampling Frequency

        """
        self.l_filter = LowPassFilter(fcut_2, fsample)
        self.h_filter = HighPassFilter(fcut_1, fsample)


    def evaluate(self, _in):
        """
        Evaluates the filter

        :param _input: the input
        :return: the output
        """
        v = self.l_filter.evaluate(_in)
        return self.h_filter.evaluate(v)



class BandStopFilter:

    def __init__(self, fcut_1, fcut_2, fsample):
        """
        A class that implements a band-stop filter of the first order

        :param fcut_1, fcut_2: Cut-off Frequencies
        :param fsample: Sampling Frequency

        """
        self.l_filter = LowPassFilter(fcut_1, fsample)
        self.h_filter = HighPassFilter(fcut_2, fsample)


    def evaluate(self, _in):
        """
        Evaluates the filter

        :param _input: the input
        :return: the output
        """
        v1 = self.l_filter.evaluate(_in)
        v2 = self.h_filter.evaluate(_in)
        return (v1+v2)/2



class ButterworthFilter:

    def __init__(self, order, typ, fcuts, fsamp):
        """
        A class that implements a Butterworth filtrer

        :param order: Order of the filter (from 1)
        :param typ: Type of the filter, ‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’
        :param fcuts: Cut-off Frequencies, for lowpass and highpass it is a scalar, for bandpass and bandstop it is a two element list
        :param fsample: Sampling Frequency

        """
        if type(fcuts) == list:
            fcuts = np.array(fcuts)
        [b, a] = sig.butter(N = order, Wn = fcuts, btype = typ,
                            analog = False, output = 'ba', fs = fsamp)
        self.filter = ARXModel(a[1:], b)

    def evaluate(self, _in):
        """
        Evaluates the filter

        :param _input: the input
        :return: the output
        """
        return self.filter.evaluate(_in)

