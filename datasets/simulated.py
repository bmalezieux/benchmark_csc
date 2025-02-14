import numpy as np

from benchopt import BaseDataset


class Dataset(BaseDataset):

    name = "Simulated"
    __name__ = 'test'

    # List of parameters to generate the datasets. The benchmark will consider
    # the cross product for each key in the dictionary.
    parameters = {
        'n_samples, n_atoms': [
            (20, 10)
        ]
    }

    def __init__(self, n_samples=20, n_atoms=10, kernel_size=5,
                 signal_length=100, std_noise=0.1, sparsity=0.1,
                 random_state=27):
        # Store the parameters of the dataset
        self.n_samples = n_samples
        self.n_atoms = n_atoms
        self.kernel_size = kernel_size
        self.signal_length = signal_length
        self.noise = std_noise
        self.sparsity = sparsity
        self.random_state = random_state

    def get_data(self):
        rng = np.random.RandomState(self.random_state)
        D = rng.normal(size=(self.n_atoms, self.kernel_size))

        theta = rng.random(size=(self.n_samples,
                                 self.n_atoms,
                                 self.signal_length - self.kernel_size + 1))
        theta = theta > 1 - self.sparsity

        y = np.concatenate([
            np.sum([
                np.convolve(theta_k, d_k, mode="full")
                for theta_k, d_k in zip(theta[i, :, :], D)
            ], axis=0).reshape(1, -1)
            for i in range(theta.shape[0])
        ], axis=0)
        y += rng.normal(scale=self.noise, size=y.shape)

        data = dict(D=D, y=y)

        return theta.shape, data
