import requests, xmltodict
from subprocess import Popen, PIPE

def geocode(query):
    key = 'iA6urWl77cgH20jhoNWQB5nSAvgKaDGt'
    query = query.replace(' ', '+')
    url = 'https://www.mapquestapi.com/geocoding/v1/address?key=' + key + '&inFormat=kvp&outFormat=json&location=' + query + '&thumbMaps=false'
    response = requests.get(url).json()
    return response['results'][0]['locations'][0]['latLng'].values()
# lat,lon = geocode('jacob circle mumbai')

def trafficData():
    key = '67NeB11TRMEkpcJHHAgtA8DYXHnCd8st'
    url = 'https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/xml?point=' + str(lat) + '%2C' + str(lon) + '&key=' + key
    response = requests.get(url)
    with open('trafficData.xml', 'wb') as file: 
        file.write(response.content) 
    with open('trafficData.xml','rb') as file:
        trafficDict = xmltodict.parse(file)['flowSegmentData']
    file.close()
    currentSpeed, currentTime = int(trafficDict['currentSpeed']), int(trafficDict['currentTravelTime'])
    freeSpeed, freeTime = int(trafficDict['freeFlowSpeed']), int(trafficDict['freeFlowTravelTime'])
    return currentSpeed, currentTime, freeSpeed, freeTime
# currentSpeed, currentTime, freeSpeed, freeTime = trafficData()
lat, lon = 18.981046, 72.82678
def convertToDegrees(x):
    degree = int(x)
    degDecimal = (x - degree) * 60
    minute = int(degDecimal)
    minDecimal = degDecimal - minute
    seconds = round(minDecimal*60, 1)
    output = str(degree) + '°' + str(minute) + "'" + str(seconds)
    return output
convertLat, convertLon = convertToDegrees(lat), convertToDegrees(lon)

def showLocation():
    url = "https://www.google.com/maps/place/" + convertLat + "%22N+" + convertLon + "%22E/@" + str(lat) + "," + str(lon) + ",17z"
    script = '''
    tell application "Safari"
        tell window 1
            set current tab to (make new tab with properties {URL:"''' + url + '''"})
        end tell
        activate
    end tell
    '''
    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    stdout, stderr = p.communicate(script)
showLocation()
