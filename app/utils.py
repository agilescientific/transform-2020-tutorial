import base64
from io import BytesIO

import numpy as np
import requests
from PIL import Image
import matplotlib.pyplot as plt


def plot(probs, class_names):
    """
    Make a plot and return a base64 encoded string.
    """
    y = list(range(len(probs)))
    y_min, y_max = y[0]-0.75, y[-1]+0.75

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.barh(y, probs, color='orange', align='center', edgecolor='none')
    bars[np.argmax(probs)].set_color('red')
    ax.set_yticks(y)
    ax.set_yticklabels(class_names, size=12)
    ax.set_xscale('log')
    ax.set_ylim(y_max, y_min)  # Label top-down.
    ax.grid(c='black', alpha=0.15, which='both')
    ax.patch.set_facecolor("white")
    fig.patch.set_facecolor("none")

    for i, p in enumerate(probs):
        ax.text(min(probs), i, "{:0.2e}".format(p), va='center')

    plt.tight_layout()

    # Put in memory.
    handle = BytesIO()
    plt.savefig(handle, format='png', facecolor=fig.get_facecolor())
    plt.close()

    # Encode.
    handle.seek(0)
    figdata_png = base64.b64encode(handle.getvalue()).decode('utf8')

    return figdata_png

# We need the following:
#  - im_to_arr
#  - fetch_image
#  - predict_from_image
