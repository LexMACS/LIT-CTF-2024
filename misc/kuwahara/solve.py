#!/usr/bin/env python3
"""
Solution to the problem!
"""

import numpy as np
import cv2
from encoder import encode, decode

def kuwahara(original_image, window_size):
    """
    Kuwahara Algorithm. This function applies the Kuwahara algorithm to an image.
    
    Args:
        original_image (ndarray): The original image to apply the Kuwahara algorithm to.
        window_size (int): The size of the window used for calculating the local statistics.

    Returns:
        tuple: A tuple containing the following elements:
            - averages (ndarray): An array of shape (4, H, W, C)
                                containing the average values for each subregion.
            - stddevs (ndarray): An array of shape (4, H, W)
                                containing the standard deviations for each subregion.
    """
    image = original_image.astype(np.float32, copy=False)

    averages = np.empty((4, *image.shape), dtype=image.dtype)
    stddevs = np.empty((4, *image.shape[:2]), dtype=image.dtype)

    image_2d = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(image.dtype, copy=False)

    averages_2d = np.empty((4, *image.shape[:2]), dtype=image.dtype)
    squared_image = image_2d ** 2

    kxy = np.ones(window_size + 1, dtype=image.dtype) / (window_size + 1)
    shift = [(0, 0), (0, window_size), (window_size, 0), (window_size, window_size)]
    for k in range(4):
        kx = ky = kxy
        # sepFilter2D's are so awesome, really freaking fast
        cv2.sepFilter2D(image, -1, kx, ky, averages[k], shift[k])
        cv2.sepFilter2D(image_2d, -1, kx, ky, averages_2d[k], shift[k])
        cv2.sepFilter2D(squared_image, -1, kx, ky, stddevs[k], shift[k])
        stddevs[k] = stddevs[k] - averages_2d[k] ** 2
    return averages, stddevs

def kuwahara_encryption(original_image, message, window_size=5):
    """
    Applies the Kuwahara algorithm to an original image and encrypts a message within it.

    Parameters:
    - original_image (ndarray): The original image to be processed.
    - message (str): The message to be encrypted within the image.
    - window_size (int): The size of the window used in the Kuwahara algorithm. Default is 5.

    Returns:
    - ndarray: The filtered image with the encrypted message.
    """
    averages, stddevs = kuwahara(original_image, window_size)
    indices = np.argmin(stddevs, axis=0)
    sorted_indices = np.argsort(stddevs, axis=0)

    # Start at (window_size, window_size) to avoid the border, where
    # the Kuwahara Algorithm might not get enough pixels.
    start_x = start_y = window_size
    for m in message:
        indices[start_x][start_y] = sorted_indices[m][start_x][start_y]
        start_y += 1
        if start_y == original_image.shape[1] - window_size:
            start_y = window_size
            start_x += 1

    # Second favorite function when writing this, take_along_axis. Epic.
    filtered = np.take_along_axis(averages, indices[None,...,None], 0).reshape(original_image.shape)
    return filtered.astype(original_image.dtype)

def kuwahara_decryption(original_image, enc_image, window_size=5):
    """
    Decodes an encoded image using the Kuwahara algorithm.

    Parameters:
    original_image (ndarray): The original image used for encoding.
    enc_image (ndarray): The encoded image to be decoded.
    window_size (int, optional): The size of the window used
                                for the Kuwahara algorithm. Default is 5.

    Returns:
    list: The original message from the encoded image.
    """
    averages, stddevs = kuwahara(original_image, window_size)
    indices = np.argmin(stddevs, axis=0)
    sorted_indices = np.argsort(stddevs, axis=0)
    averages = averages.astype(original_image.dtype)
    differences = []
    for i in range(enc_image.shape[0]):
        for j in range(enc_image.shape[1]):
            if not np.array_equal(enc_image[i][j], averages[indices[i][j]][i][j]):
                for k in range(1, 4):
                    ind = sorted_indices[k][i][j]
                    if np.array_equal(enc_image[i][j], averages[ind][i][j]):
                        differences.append(k)
                        break
    return differences

# Load the noisy image
input_image = cv2.imread('img/noisy_image.png')
encoded_image = cv2.imread('img/encoded_image.png')

# DECRYPTION:

decoded_indices = kuwahara_decryption(input_image, encoded_image)

final_message = decode([dec - 1 for dec in decoded_indices], 3)
print("Flag: ", final_message)
