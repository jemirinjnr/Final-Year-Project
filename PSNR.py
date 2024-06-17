import numpy as np

def psnr(original_image, decrypted_image):
  """
  Calculate the Peak Signal-to-Noise Ratio (PSNR) between two images.

  Args:
      original_image: The original image.
      decrypted_image: The decrypted image.

  Returns:
      The PSNR in dB.
  """
  mse = np.mean((original_image - decrypted_image) ** 2)
  if mse == 0:
    return np.inf
  max_pixel = np.max(original_image)
  psnr = 10 * np.log10(max_pixel**2 / mse)
  return psnr

# Example usage
original_image = np.array([   # Replace with your original image data
    [100, 120, 150],
    [80, 180, 200],
    [50, 210, 230]
])
decrypted_image = np.array([  # Replace with your decrypted image data
    [95, 115, 145],
    [75, 175, 195],
    [45, 205, 225]
])

psnr_value = psnr(original_image, decrypted_image)
print(f"PSNR between original and decrypted image: {psnr_value:.2f} dB")
