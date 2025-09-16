C.H.A.N.G.E. (Change Detection Helper for Analyzing New Geospatial Events)
Overview
C.H.A.N.G.E. is a Python application designed to facilitate change detection in geospatial data using the openEO framework. It allows users to compare two satellite images—an archive image and a crisis image—to identify and quantify changes in land cover or other features over time. This tool is particularly useful for environmental monitoring, disaster response, and land management.

Features
Image Loading: Easily load satellite images from specified collections.
Reclassification: Apply custom reclassification algorithms to both archive and crisis images to prepare the data for comparison.
Difference Mapping: Compute the difference between the reclassified crisis image and the archive image to highlight changes.
Binary Mask Creation: Generate a binary mask to isolate areas of significant change based on a specified threshold.
Area Calculation: Calculate the impacted area of the detected changes, providing valuable quantitative insights.
Requirements
Python 3.x
openEO Python client library
Access to an openEO backend (e.g., cloud.openeo.org)
Installation
Bash 
Copy codeCode copied
pip install openeo
Usage
Connect to openEO Backend: Establish a connection to your preferred openEO backend.

Load Images: Load the archive and crisis images using their respective collection IDs.

Reclassify Images: Apply reclassification functions to the loaded images to prepare them for change detection.

Compute Differences: Calculate the difference between the two reclassified images.

Create Binary Mask: Generate a binary mask to highlight areas of change.

Calculate Impacted Area: Specify the geometry of interest and calculate the total impacted area.

Example
Python 
Copy codeCode copied
# Example code snippet to demonstrate usage
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

Contact
For questions or support, please contact [deinncoentis.nicola@gmail.com].

C.H.A.N.G.E. aims to streamline the process of detecting and analyzing changes in geospatial data, making it easier for researchers, policymakers, and environmentalists to respond to dynamic landscapes and environmental challenges.