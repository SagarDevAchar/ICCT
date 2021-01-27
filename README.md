# ICCT (Image Colour Channel Tool) #
Tkinter based Image Colouring / Filtering Tool (with OpenCV-Python & Numpy)

#

The following documentation corresponds to the **Initial Version (v1.0)** of ICCT

## Features:

* **Read Formats:** JPEG / JPG / PNG / BMP
* **Write Formats:** JPEG / JPG / PNG
* 7 Image Filters / Effects:
  * **Adjust:** Alter the brightness and contrast of the image with full range provision from Black (Dark) to White (Bright)
  * **Specific:** Focuses only on a particular RGB colour switching all other colours to Black / White based on the selection
  * **Intensity:** Additive / Subractive changes to the RGB channels of the image
  * **Greyscale:** Converts the Image to a weighted greyscale (R -> 0.299, G -> 0.587, B -> 0.114)
  * **Inverse:** Invertion / Negation of the image with a variable degree of inversion
  * **Ceiling:** Sets the maximum value for the R G B Channels. Any pixel exceeding the limits with be set to Black
  * **Floor:** Sets the minimum value for the R G B Channels. Any pixel exceeding the limits with be set to Black
* Image Colour Picker / Sampler and Format Conversion (*with* Alpha channel support):
  * RGB
  * HSL
  * CMYK
  * HEX
* **Image Visualizer for R G B channel visualization:** A 2D / 3D graphical analysis for images (Alpha unsupported)

## Usage:

1.  Browse for a supported Image File from your Local Storage
1.  Select the **Mode of Operation** using the dropdown menu
1.  Cumulative Filters:
    * *CHECKED*: The filters will be applied to one another hence adding up the effects
    * *UNCHECKED*: The respective filter will be applied to the original image discarding the previous preview
1.  Vary the parameters as desired using either the slider or the entry
1.  Click on **"Apply Parameters"** to see the effect being applied to the Image Preview (this may take a few seconds based on the resolution of the image)
    * Clicking on any point on the image will reveal the colour of that particular pixel in the **Picker** panel
    * The **Toolbar** at the bottom of the **Image Preview** panel can be used to Pan & Zoom on the Image
    * The **"Visualize"** button opens a new graph window showing the RGB Channel Graphs of the current image preview
    * The **"Reset Preview"** button removes all filters and previews the original image (all filters will be discarded)
1.  The current preview image with the filters applied can be saved to the desired location by clicking on the **"Save Current Preview"** button
1.  The **"X"** button clears everything and sets the application to its default state

## Disclaimer:

This is ***NOT*** a fully polished / professional application. Hence, the features & functionality of the application are basic & limited. Although carefully coded, a few bugs might have crept in. Bug Reports under the *[Issues Tab](https://github.com/SagarDevAchar/ICCT/issues)* are appreciated

#

Thank you for using ICCT..! :smile:
