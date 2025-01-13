from flask import Flask, request, render_template
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from fractions import Fraction
from geopy.geocoders import Nominatim

app = Flask(__name__)

class Worker(object):
    def __init__(self, img):
        self.img = img
        self.exif_data = self.get_exif_data()
        self.lat = self.get_lat()
        self.lon = self.get_lon()
        self.date = self.get_date_time()
        super(Worker, self).__init__()

    @staticmethod
    def get_if_exist(data, key):
        if key in data:
            return data[key]
        return None

    @staticmethod
    def convert_to_degrees(value):
        """Helper function to convert the GPS coordinates
        stored in the EXIF to degrees in float format"""
        d = float(Fraction(value[0]))
        m = float(Fraction(value[1]))
        s = float(Fraction(value[2]))
        return d + (m / 60.0) + (s / 3600.0)

    def get_exif_data(self):
        """Returns a dictionary from the exif data of a PIL Image item. Also
        converts the GPS Tags"""
        exif_data = {}
        info = self.img._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)

                # Print extra tags info
                print(f"{decoded} : {value}")
                    
                # Isolate GPSInfo from exif data in a dict
                if decoded == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_data[sub_decoded] = value[t]

                    exif_data[decoded] = gps_data
                else:
                    exif_data[decoded] = value                    

        return exif_data

    def get_lat(self):
        """Returns the latitude, if available, from the 
        provided exif_data (obtained through get_exif_data above)"""
        if 'GPSInfo' in self.exif_data:
            gps_info = self.exif_data["GPSInfo"]
            gps_latitude = self.get_if_exist(gps_info, "GPSLatitude")
            gps_latitude_ref = self.get_if_exist(gps_info, 'GPSLatitudeRef')
            if gps_latitude and gps_latitude_ref:
                lat = self.convert_to_degrees(gps_latitude)
                if gps_latitude_ref != "N":
                    lat = 0 - lat
                return lat
        return None

    def get_lon(self):
        """Returns the longitude, if available, from the 
        provided exif_data (obtained through get_exif_data above)"""
        if 'GPSInfo' in self.exif_data:
            gps_info = self.exif_data["GPSInfo"]
            gps_longitude = self.get_if_exist(gps_info, 'GPSLongitude')
            gps_longitude_ref = self.get_if_exist(gps_info, 'GPSLongitudeRef')
            if gps_longitude and gps_longitude_ref:
                lon = self.convert_to_degrees(gps_longitude)
                if gps_longitude_ref != "E":
                    lon = 0 - lon
                return lon
        return None

    def get_date_time(self):
        """Returns the date and time, if available, from the exif_data"""
        return self.exif_data.get('DateTime')

def get_address_from_coordinates(lat, lon):
    geolocator = Nominatim(user_agent="flask_app")
    location = geolocator.reverse(f"{lat}, {lon}")
    address = location.raw.get('address', {})
    return {
        'country': address.get('country', 'N/A'),
        'city': address.get('city', 'N/A') or address.get('town', 'N/A') or address.get('village', 'N/A'),
        'zipcode': address.get('postcode', 'N/A')
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    if file:
        filename = file.filename
        filepath = os.path.join('static', filename)
        file.save(filepath)
        
        image = Image.open(filepath)
        worker = Worker(image)
       
        info_dict = {
            "Filename": image.filename.replace('static\\', ''),
            "Image Size": image.size,
            "Image Height": image.height,
            "Image Width": image.width,
            "Image Format": image.format,
            "Image Mode": image.mode,
            "Image is Animated": getattr(image, "is_animated", False),
            "Frames in Image": getattr(image, "n_frames", 1)
        }
        gps_dict = worker.exif_data.get("GPSInfo", {})
        latitude = worker.lat
        longitude = worker.lon

        address_info = {}
        if latitude and longitude:
            try:
                address_info = get_address_from_coordinates(latitude, longitude)
            except Exception as e:
                print(f"Error in reverse geocoding: {e}")
                address_info = {'country': 'N/A', 'city': 'N/A', 'zipcode': 'N/A'}
        
        extra_info_dict = {tag: value for tag, value in worker.exif_data.items() if tag != "GPSInfo" and tag != "MakerNote"}
        maker_note_dict = {tag: value for tag, value in worker.exif_data.items() if tag == "MakerNote"}

        return render_template('index.html', filename=filename, info_dict=info_dict, gps_dict=gps_dict, latitude=latitude, longitude=longitude, gps_info_dict=address_info, extra_info_dict=extra_info_dict, maker_note_dict=maker_note_dict)

if __name__ == '__main__':
    app.run(debug=True)
