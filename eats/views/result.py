from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from googleplaces import GooglePlaces, types
import urllib, json, requests, random, os


def result(request):
    # get the winner from previous post
    winner = request.POST.get('winner')

    # open and read user data from text file
    filePath = os.path.join(settings.STATICFILES_DIRS[0], "user_data.txt")
    textfile = open(filePath, "r")
    text = textfile.read().split('\n', 1)
    lat_lng = text[0]
    radius = text[1]

    # find the winner google place
    googResults = googPlace(lat_lng, radius, winner).places

    # get more details on a restaurant/place
    place = googResults[0]
    place.get_details()
    
    photos = []
    for photo in place.photos:
        aphoto = {
            "pho": photo.get(maxheight=500, maxwidth=500),
            # "mime": photo.mimetype,
            "url": photo.url,
            # "data": photo.data
        }
        # aphoto.append(photo.get(maxheight=500, maxwidth=500))
        # aphoto.append(photo.mimetype)
        # aphoto.append(photo.url)
        # aphoto.append(photo.data)
        photos.append(aphoto)

    context = {
        "name":         place.name,
        "location":     place.geo_location,
        "phone":        place.local_phone_number,
        # "details":      place.details,
        # "website":      place.website,
        "url":          place.url,
        "photos":       photos
    }
    print("location: ", place.geo_location)
    # print("context: ", photos[0]['url'])

    return render(request, 'eats/results.html', context=context)


#send request to google api for restaurants in selected radius of user
def googPlace(lat_lng, radius, name):
    google_places = GooglePlaces(settings.SECRET_KEY)

    result = google_places.nearby_search(
        lat_lng=lat_lng,
        keyword='Restaurants',
        radius=radius,
        types=[types.TYPE_RESTAURANT],
        name=name
    )

    return result



#helper to create a list of name and location
def getPlaces(goog):
    place = [goog.name, goog.geo_location]

    return place
