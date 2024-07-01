import os
import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
from tkinter import filedialog, Tk
from ipywidgets import widgets, interact
from IPython.display import display

def select_file():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    file_path = filedialog.askopenfilename(parent=root)
    root.attributes('-topmost', False)

    if file_path:
        image = Image.open(file_path).convert('RGB')
        image = np.array(image)
        return file_path, image
    else:
        raise FileNotFoundError("Not selected")

def convert_to_gray(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return gray_image

def apply_threshold(threshold, image, gray_image, file_path):
    alpha = 0.5  
    beta = 1.0 - alpha
    mask = gray_image < threshold
    binary_colored_image = np.ones_like(image) * 255
    binary_colored_image[mask] = [200, 150, 100]
    blended_image = cv2.addWeighted(image, beta, binary_colored_image, alpha, 0)

    plt.figure(figsize=(15, 10))
    plt.imshow(cv2.cvtColor(blended_image, cv2.COLOR_RGB2BGR))
    plt.title('Blend')
    plt.axis('off')
    plt.show()

    print(f"Threshold: {threshold:.2f}")

    mask = gray_image < threshold
    binary_colored_image = np.ones_like(image) * 255
    binary_colored_image[mask] = [200, 150, 100]
    binary_colored_image = cv2.cvtColor(binary_colored_image, cv2.COLOR_RGB2BGR)

    alpha = 0.6  
    beta = 1.0 - alpha

    blended_image = cv2.addWeighted(image, beta, binary_colored_image, alpha, 0)
    base_name = os.path.basename(file_path)
    result_image_path = os.path.splitext(base_name)[0] + '_result.png'
    result_text_path = os.path.splitext(base_name)[0] + '_result.txt'
    
    directory, filename = os.path.split(file_path)
    save_path = os.path.join(directory, result_image_path)
    result_text_path = os.path.join(directory, result_text_path)

    try:
        plt.imsave(save_path, binary_colored_image)
    except Exception as e:
        print(f"Error saving the image: {e}")

    dark_pixel_percent = np.mean(gray_image < threshold) * 100
    print(f"Percentage of dark pixels: {dark_pixel_percent:.2f}%")

    try:
        with open(result_text_path, 'w') as f:
            f.write(f"Percentage of dark pixels: {dark_pixel_percent:.2f}%\n")
            f.write(f"Threshold: {threshold}\n")
            
    except Exception as e:
        print(f"Error saving the image: {e}")

    plt.figure(figsize=(15, 10))
    plt.subplot(1, 2, 1)
    plt.imshow(image)
    plt.title('Image')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(binary_colored_image)
    plt.title('Result')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

def setup_widgets(image, gray_image, file_path):
    threshold_slider = widgets.IntSlider(min=0, max=255, step=1, value=127, continuous_update=False)
    threshold_text = widgets.FloatText(value=127)
    
    def update_threshold_text(change):
        threshold_text.value = change.new

    def on_threshold_text_change(change):
        threshold_slider.value = change['new']

    threshold_slider.observe(update_threshold_text, names='value')
    threshold_text.observe(on_threshold_text_change, names='value')

    display(widgets.HBox([threshold_text]))

    def interactive_apply_threshold(threshold):
        apply_threshold(threshold, image, gray_image, file_path)

    interact(interactive_apply_threshold, threshold=threshold_slider)
