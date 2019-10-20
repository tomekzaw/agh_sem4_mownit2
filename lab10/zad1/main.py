import numpy as np
import math

def pad(A, length): # pads vector to specified length
    arr = np.zeros(length, dtype=complex)
    arr[:len(A)] = A
    return arr

def pad2n(A): # pad vector with zeroes to length of 2^k
    k = int(math.ceil(math.log2(len(A))))
    n = int(pow(2, k))
    x = pad(A, n)
    return x, n

def split(x):
    return x[0::2], x[1::2] # even, odd

def F(n): # Fourier matrix
    return np.fromfunction(lambda i, j: np.exp(-2j*np.pi*i*j/n), (n, n), dtype=complex)

def E(n): # diagonal matrix
    return np.diag(np.fromfunction(lambda i: np.exp(-2j*np.pi*i/n), (n//2,), dtype=complex))

def my_dft(x): # Discrete Fourier Transform
    x, n = pad2n(x)
    return F(n) @ x

def my_idft(y): # Inverse Discrete Fourier Transform
    y, n = pad2n(y)
    return np.conj(F(n) @ np.conj(y)) / n

def my_fft(x): # Fast Fourier Transform
    x, n = pad2n(x) # or: n = x.shape[0]
    if n == 2:
        return np.array([x[0]+x[1], x[0]-x[1]], dtype=complex) # or: F(2) @ x, or: if n == 1: return x
    even, odd = map(my_fft, split(x)) # even, odd = my_fft(x[0::2]), my_fft(x[1::2])
    Ediag = np.diag(E(n))
    return np.concatenate((even + Ediag * odd, even - Ediag * odd))

def my_ifft(y):  # Inverse Fast Fourier Transform
    y, n = pad2n(y)
    return np.conj(my_fft(np.conj(y))) / n

if __name__ == "__main__":
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=complex)
    y_dft = my_dft(x)
    y_fft = my_fft(x)
    y_np = np.fft.fft(x)
    z_dft = my_idft(y_dft)
    z_fft = my_ifft(y_fft)
    z_np = np.fft.ifft(y_np)
    for v in (x, y_dft, y_fft, y_np, z_dft, z_fft, z_np):
        print(np.real_if_close(v))
