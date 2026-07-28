import numpy as np

class BuildMLP3Meteo:
    def __init__(self, in_size: int, hd_size: int, out_size: int, input_data, target_data) -> None:
        self.weights_input_hidden = 0.2 * np.random.random((in_size, hd_size)) - 0.1
        self.weights_hidden_output = 0.2 * np.random.random((hd_size, out_size)) - 0.1
        self.input_data = input_data
        self.target_data = target_data
        self.normalize_array = np.array([[10000, 800, 1200, 1500, 2000, 1013, 1013, 1013, 150]]) # [[cape, cin, srh_01, srh_03, srh_06, lcl_p, lfc_p, el_p, bulk_shear_06]]

    def __str__(self) -> str:
        return f'Weights input -> hidden: {self.weights_input_hidden}\nWeights hidden -> output: {self.weights_hidden_output}\nInput data: {self.input_data}'

    def relu(self, x):
        return (x > 0) * x

    def relu_derivative(self, x):
        return x > 0

    def normalize(self):
        normalize_data = self.input_data / self.normalize_array
        return normalize_data

    def forward(self):
        self.layer_in = self.normalize()
        self.layer_hd = self.relu(np.dot(self.layer_in, self.weights_input_hidden))
        self.dropout = np.random.randint(2, size=self.layer_hd.shape)
        self.layer_hd *= self.dropout * 2
        self.layer_out = np.dot(self.layer_hd, self.weights_hidden_output)

    def backward(self):
        delta_out = self.layer_out - self.target_data
        delta_hd = np.dot(delta_out, self.weights_hidden_output.T) * self.relu_derivative(self.layer_hd)
        delta_hd *= self.dropout * 2
        self.weights_hidden_output -= np.dot(self.layer_hd.T, delta_out) * 0.01
        self.weights_input_hidden -= np.dot(self.layer_in.T, delta_hd) * 0.01

    def save_weights(self):
        return self.weights_input_hidden, self.weights_hidden_output

    def start(self):
        self.layer_in = self.normalize()
        self.layer_hd = self.relu(np.dot(self.layer_in, self.weights_input_hidden))
        self.layer_out = np.dot(self.layer_hd, self.weights_hidden_output)
        return self.layer_out