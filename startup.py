import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import skimage as ski

from natsort import natsorted, ns
from skimage import data, img_as_float
from skimage import exposure


matplotlib.rcParams['font.size'] = 8


def plot_img_and_hist(image, axes, bins=256):
    """Plot an image along with its histogram and cumulative histogram.

    """
    image = img_as_float(image)
    ax_img, ax_hist = axes
    ax_cdf = ax_hist.twinx()

    # Display image
    ax_img.imshow(image, cmap=plt.cm.gray)
    ax_img.set_axis_off()

    # Display histogram
    ax_hist.hist(image.ravel(), bins=bins, histtype='step', color='black')
    ax_hist.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    ax_hist.set_xlabel('Pixel intensity')
    ax_hist.set_xlim(0, 1)
    ax_hist.set_yticks([])

    # Display cumulative distribution
    img_cdf, bins = exposure.cumulative_distribution(image, bins)
    ax_cdf.plot(bins, img_cdf, 'r')
    ax_cdf.set_yticks([])

    return ax_img, ax_hist, ax_cdf


# Load example images
folder_path = os.path.join(os.getcwd(), 'images')
list_files = os.listdir(folder_path)
list_files = natsorted(list_files)
image_list = []
for filename in list_files:
  filename = os.path.join(folder_path, filename)
  image_list.append(ski.io.imread(filename))
img1 = image_list[0]

# Contrast stretching
p2, p98 = np.percentile(img1, (2, 98))
img_rescale = exposure.rescale_intensity(img1, in_range=(p2, p98))

# Equalization
img_eq = exposure.equalize_hist(img1)

# Adaptive Equalization
img_adapteq = exposure.equalize_adapthist(img1, clip_limit=0.03)

# Display results
fig = plt.figure(figsize=(8, 5))
axes = np.zeros((2, 4), dtype=object)
axes[0, 0] = fig.add_subplot(2, 4, 1)
for i in range(1, 4):
    axes[0, i] = fig.add_subplot(2, 4, 1+i, sharex=axes[0,0], sharey=axes[0,0])
for i in range(0, 4):
    axes[1, i] = fig.add_subplot(2, 4, 5+i)