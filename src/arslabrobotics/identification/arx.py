#
# arx.py
#

__all__ = [ "ARXSolver", "ARXModel", "NeuralARX" ]

import numpy as np

class ARXSolver:

    def __init__(self, data_in_out, output_lag, input_lag):
        """
        An helper class to solve the linear system identification problem using
        the auto-regressive model::

            y(k) + a0 * y(k-1) + a1 * y(k-2) + ... y(k-n) = b0 * u(k) + b1 * u(k-1) + ... u(k-m)

        :param data_in_out: A matrix [ [ u(k), y(k) ] ] containing input/output sampled data
        :param output_lag: The number of delay blocks for the output (n)
        :param input_lag: The number of delay blocks for the input (m)

        """
        self.data_in_out = data_in_out
        self.output_lag = output_lag
        self.input_lag = input_lag
        self.data_len = len(self.data_in_out)

    def solve(self) -> tuple:
        """
        Solves the ARX model

        :return: A tuple (a_parameters, b_parameters)
        """
        U = np.array( self.data_in_out[ : , 0] ).reshape(-1, 1)
        Y = np.array( self.data_in_out[ : , 1] ).reshape(-1, 1)
        n_rows = self.data_len - self.output_lag
        regression_matrix = np.zeros( (n_rows, self.output_lag + self.input_lag + 1) )
        for i in range(0, self.output_lag):
            regression_matrix[:, i] = - Y[i: i + n_rows].flatten()
        for i in range(0, self.input_lag + 1):
            regression_matrix[:, self.output_lag + i] = U[i + 1: i + 1 + n_rows].flatten()
        theta_hat, residuals, rank, s = np.linalg.lstsq(regression_matrix, Y[self.output_lag:], rcond=None)
        a_params = theta_hat[:self.output_lag]
        b_params = theta_hat[self.output_lag:]
        return a_params, b_params#, residuals[0] / self.data_len


class ARXModel:

    def __init__(self, a_params, b_params):
        self.a_params = a_params
        self.b_params = b_params
        self.output_lag = len(a_params)
        self.input_lag = len(b_params) - 1
        self.y_memory = [ 0 ] * self.output_lag
        self.u_memory = [ 0 ] * self.input_lag

    def evaluate(self, _input):
        output = 0.0
        for i in range(self.output_lag):
            output += - self.y_memory[i] * self.a_params[i]
        for i in range(self.input_lag):
            output += self.u_memory[i] * self.b_params[i + 1]
        output += _input * self.b_params[0]
        self.y_memory = self.y_memory[1:]
        self.y_memory.append(output)
        self.u_memory = self.u_memory[1:]
        self.u_memory.append(_input)
        return output


class NeuralARX:

    def __init__(self, data_in_out, output_lag, input_lag):
        self.data_in_out = data_in_out
        self.output_lag = output_lag
        self.input_lag = input_lag
        self.data_len = len(self.data_in_out)

    def prepare(self):
        U = np.array( self.data_in_out[ : , 0] ).reshape(-1, 1)
        Y = np.array( self.data_in_out[ : , 1] ).reshape(-1, 1)

        nn_in, nn_out = [], []
        for i in range(self.data_len - max([self.output_lag, self.input_lag + 1])):

            u_window = U[i:(i + self.input_lag + 1)]
            y_window = Y[i:(i + self.output_lag)]

            nn_input = np.row_stack( (u_window, y_window) )

            nn_in.append(nn_input)
            nn_out.append(Y[i + self.output_lag])

        return np.array(nn_in), np.array(nn_out)



