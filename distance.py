import simplejson
from urllib import request


def getDistance(source, destination):
	url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&key=AIzaSyAUXAfBkeayPbydQpFWAbKXYxyKBwsQSLA"

	url = url.format(source, destination)
	result = simplejson.load(request.urlopen(url))
	# driving_distance = result['rows'][0]['elements'][0]['distance']['value']
	list = result['rows'][0]['elements']
	# print(list)
	dist = []
	for item in list:
		if item['status'] != 'NOT_FOUND': 
			dist.append({'dist' : item['distance']['value'] / 1000, 'tim' : item['duration']['text'] })
		else:
			dist.append({'dist' : -1, 'tim' : -1})
	return dist

#=====================================================================================================================================
#=====================================================================================================================================

if __name__ == '__main__':
	source = '25.3076591,82.9910195'
	destination = '25.3076591,82.9910195|17.4480215,78.3483768|error'
	print(getDistance(source, destination))

# ####RESPONSE
# [{'elements': [{'status': 'OK', 'duration': {'value': 0, 'text': '1 min'}, 'distance': {'value': 0, 'text': '1 m'}}, 
# 				{'status': 'OK', 'duration': {'value': 90217, 'text': '1 day 1 hour'}, 'distance': {'value': 1262425, 'text': '1,262 km'}}, 
# 				{'status': 'OK', 'duration': {'value': 44673, 'text': '12 hours 25 mins'}, 'distance': {'value': 797578, 'text': '798 km'}}
# 				]
# 				}]
