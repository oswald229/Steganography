import imageio
import matplotlib.pyplot as plt

from helpers.stegano_helper import Steganography


class Steganographor:
    """
    Class that will handle Steganography process.
    """

    def __init__(self, start_idx, receiver_path, secret_path):
        """

        :param start_idx: [row, col] - Starting index of the secret picture.
        :param receiver_path: string - Receiving image path.
        :param secret_path: string - Secret picture path.
        """

        self._receiver_path = receiver_path
        self._receiver = imageio.imread(receiver_path)
        self._receiver_binary_pixels = []

        self._secret_path = secret_path
        self._secret = imageio.imread(secret_path)
        self._secret_binary_pixels = []

        self._start_idx = start_idx

        self._receiving_idxs = []

        if self._secret.size > self._receiver.size:
            raise ValueError("Secret picture size cannot be bigger than receiver size.")

        self._new_pixels = []

        self._result = self._receiver

    def get_idxs(self, start, secret_row_size, secret_col_size, tab):
        """
        :param start: Starting index.
        :param secret_row_size: Number of row in the secret image/tab.
        :param secret_col_size: Number of col in the secret image/tab.
        :param tab: Receiver (Image or tab).
        :return: List of indexes.
        """
        idxs = []

        i = start[0]
        j = start[1]

        # TODO : Remove or add "="

        if j + secret_col_size > tab.shape[1]:

            raise ValueError('Wrong starting index (columns)')

        elif i + secret_row_size > tab.shape[0]:

            raise ValueError('Wrong srating index (rows)')

        for k in range(0, secret_row_size):
            for l in range(0, secret_col_size):
                idxs.append([i + k, j + l])

        return idxs

    def pixels_to_binaries(self, idxs, tab):
        binary_pixels = []

        for i in idxs:
            row = i[0]
            col = i[1]

            # Pixel with transparency bit
            if len(tab[row, col]) == 4:
                bin_pixel = Steganography.int_to_bin(tab[row, col][:-1])

                # Pixel without transparency bit
            elif len(tab[row, col]) == 3:
                bin_pixel = Steganography.int_to_bin(tab[row, col])
            else:
                raise ValueError("Wrong pixel format.")

            binary_pixels.append(bin_pixel)

        return binary_pixels

    def encode(self):

        self._receiving_idxs = self.get_idxs(self._start_idx, self._secret.shape[0], self._secret.shape[1],
                                             self._receiver)

        self._receiver_binary_pixels = self.pixels_to_binaries(self._receiving_idxs, self._receiver)

        if len(self._receiver_binary_pixels) == self._secret.shape[0] * self._secret.shape[1]:
            self._secret_binary_pixels = self.pixels_to_binaries(
                self.get_idxs([0, 0], self._secret.shape[0], self._secret.shape[1], self._secret), self._secret)

            # self._secret_binary_pixels = []
            # for j in range(0, self._secret.shape[0]):
            #     for k in range(0, self._secret.shape[1]):
            #
            #         if len(self._secret[j][k]) == 4:
            #             bin_pixel = Steganography.int_to_bin(self._secret[j][k][:-1])
            #         elif len(self._secret[j][k]) == 3:
            #             bin_pixel = Steganography.int_to_bin(self._secret[j][k])
            #         else:
            #             raise ValueError("Wrong pixel format.")
            #
            #         self._secret_binary_pixels.append(bin_pixel)

        if len(self._receiver_binary_pixels) == len(self._secret_binary_pixels):
            for m in range(0, len(self._receiver_binary_pixels)):
                self._receiver_binary_pixels[m] = Steganography.merge_rgb(self._receiver_binary_pixels[m],
                                                                          self._secret_binary_pixels[m])
                self._receiver_binary_pixels[m] = Steganography.bin_to_int(self._receiver_binary_pixels[m])
                self._receiver_binary_pixels[m] = list(self._receiver_binary_pixels[m])
                self._receiver_binary_pixels[m].append(255)
                self._receiver_binary_pixels[m] = tuple(self._receiver_binary_pixels[m])

        n = 0
        for i in self._receiving_idxs:

            row = i[0]
            col = i[1]
            if len(self._result[row, col]) == 4:

                self._result[row, col] = self._receiver_binary_pixels[n]
            else:
                self._result[row, col] = self._receiver_binary_pixels[n][:3]

            n += 1

        return self._result

    @staticmethod
    def decode(secret):

        for i in range(0, secret.shape[0]):
            for j in range(0, secret.shape[1]):

                if len(secret[i, j]) == 4:
                    pixel = Steganography.int_to_bin(secret[i, j][:-1])

                elif len(secret[i, j]) == 3:
                    pixel = Steganography.int_to_bin(secret[i, j])
                else:
                    raise ValueError("Wrong pixel format.")

                # Move the last 4 bits from LSB to MSB

                r = pixel[0][4:] + '1111'
                g = pixel[1][4:] + '1111'
                b = pixel[2][4:] + '1111'
                rgb = tuple([r, g, b])
                new_pixel = Steganography.bin_to_int(rgb)

                new_pixel = list(new_pixel)
                new_pixel.append(255)
                new_pixel = tuple(new_pixel)

                if len(secret[i, j]) == 4:

                    secret[i, j] = new_pixel
                else:
                    secret[i, j] = new_pixel[:3]
        # plt.imshow(secret)

        # plt.show()
        return secret
