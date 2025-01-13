# MetaPix

MetaPix is a user-friendly web application that allows you to upload your pictures and view all their EXIF metadata. Additionally, it displays the GPS location data on an interactive OpenStreetMap map.

## Features

- **Upload Pictures**: Easily upload images to the platform.
- **View EXIF Metadata**: See detailed EXIF metadata including camera settings, date, time, and more.
- **GPS Location Display**: Visualize the GPS coordinates embedded in your images on an OpenStreetMap interface.

## How to Use

1. **Upload your image**: Click on the 'Upload' button and select the picture you want to analyze.
2. **View Metadata**: Once uploaded, MetaPix will display all available EXIF metadata.
3. **See GPS Location**: If the image contains GPS data, the location will be marked on an OpenStreetMap for easy viewing.

## Educational Purpose

MetaPix is an educational tool designed to identify privacy and security exposures that can arise in backend development. It specifically highlights the potential risks when client user pictures are returned to the frontend without proper privacy measures.

Note: Use sample pictures from this repository to try the app: [EXIF Samples](https://github.com/ianare/exif-samples)

## Installation

To run MetaPix locally, follow these steps:

- Install python 3.11 or higher
- Create a python venv
- Clone the repository
- Install necessary packages


```bash
python -m venv venv

cd venv

git clone "https://github.com/Mending-Electronics/MetaPix.git"

Scripts\activate

pip install -r requirements.txt
```



![picture](https://github.com/Mending-Electronics/MetaPix/blob/main/captures/capture1.png?raw=true "picture")
