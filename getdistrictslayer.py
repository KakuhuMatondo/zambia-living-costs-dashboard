import requests

url = "http://riskprofilesundrr.org/geoserver/wfs?srsName=EPSG%3A4326&typename=geonode%3Adistricts&outputFormat=json&version=1.0.0&service=WFS&request=GetFeature"

response = requests.get(url)

if response.status_code == 200:
    with open("districts.geojson", "w") as f:
        f.write(response.text)
    print("GeoJSON data saved successfully.")
else:
    print("Failed to fetch GeoJSON data.")
