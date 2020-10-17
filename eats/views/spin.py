from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from googleplaces import GooglePlaces, types
import urllib, json, requests, os, math, pickle

def spin(request):
    #get radius from previous post
    radius = request.POST.get('radopt')
    #if user chose 10+ miles set to 30 miles
    if radius == 11:
        radius = 30 * 1609.34
    #if user chose <1 mile set to .5 mile
    elif radius == 0:
        radius = .5 * 1609.34
    else:
        radius = (float(radius)) * 1609.34
    
    req = request.POST.get('location')
    location = req.split(',')

    lat_lng = {
        "lat": location[0],
        "lng": location[1]
    }
 
    # dict for user data to write to file
    user_data = {
        "lat_lng" : lat_lng,
        "radius" : radius
    }

    # write to file for result.py using pickle
    filePath = os.path.join(settings.STATICFILES_DIRS[0], "user_data.txt")
    with open(filePath, 'wb') as handle:
        pickle.dump(user_data, handle)
    
    #get nearby restaurants from google places
    type = [types.TYPE_RESTAURANT]
    googResults = googPlace(lat_lng, radius, type).places
    names = []

    #if # of restaurants in area is <5, direct to [not enough restaurants in area page]
    if len(googResults)-1 >= 5:
        for result in googResults:
            #get more details on a restaurant/place
            # result.get_details()
            names.append(result.name)
    else :
        return render(request, 'eats/invalid.html')

    #number of times to repeat list of places to reach 100 criteria
    rounds = math.ceil(100/len(googResults))

    context = {
        "pname": names,
        "rounds": rounds,
    }

    return render(request, 'eats/spin.html', context=context)


#send request to google api for restaurants in selected radius of user
def googPlace(lat_lng, radius, types):
    google_places = GooglePlaces(settings.SECRET_KEY)

    result = google_places.nearby_search(
        lat_lng = lat_lng,
        keyword = 'Restaurants',
        radius = radius,
        types=types
    )

    return result


#helper to create a list of name and location
def getPlaces(goog):
    place = [goog.name, goog.geo_location]

    return place
    