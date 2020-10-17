from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from googleplaces import GooglePlaces, types
from bs4 import BeautifulSoup
import urllib, json, requests, os, pickle


def result(request):
    # get the winner from previous post
    winner = request.POST.get('winner')
    winner = winner.strip()
    winner = winner.replace("&amp;", "&")

    # open and read user data from text file
    filePath = os.path.join(settings.STATICFILES_DIRS[0], "user_data.txt")
    user_data = read_pickle(filePath)  

    # find the google place nearby again
    googResults = goog_place(user_data["lat_lng"], user_data["radius"]).places

    # get more details on winner restaurant/place
    place = find_restaurant(winner, googResults)
    place.get_details()

    photos = []
    for photo in place.photos:
        aphoto = {
            "pho": photo.get(maxheight=500, maxwidth=500),
            # "mime": photo.mimetype,
            "url": photo.url,
            # "data": photo.data
        }

        photos.append(aphoto)
        
    # scrap menu from yelp.com
    menu_url = get_menu(winner, place.formatted_address)
    response = requests.get(menu_url)
    soup = BeautifulSoup(response.text, "html.parser")
    filter_menu(soup)
    allResults = soup.findAll(class_="menu-sections")
    
    print(allResults)
    if (allResults is None):
        menu_url = None

    # convert result set to str
    to_file = ""
    for x in allResults:
        to_file += str(x)

    # write scraped html to html file which will be imported in frontend
    with open("eats/templates/yelp_menu.html", "w", encoding="utf-8") as file:
        file.write(to_file)
    file.close()

    context = {
        "name":         winner,
        "location":     place.geo_location,
        "phone":        place.local_phone_number,
        "details":      place.details,
        "website":      place.website,
        "url":          place.url,
        "photos":       photos,
        "menu":         menu_url
    }

    return render(request, 'eats/results.html', context=context)


#send request to google api for restaurants in selected radius of user
def goog_place(lat_lng, radius):
    google_places = GooglePlaces(settings.SECRET_KEY)

    result = google_places.nearby_search(
        lat_lng=lat_lng,
        keyword='Restaurants',
        radius=radius,
        types=[types.TYPE_RESTAURANT]
    )

    return result


# read from file with pickle
def read_pickle(file_path):
    with open(file_path, 'rb') as handle:
        return pickle.loads(handle.read())


# search for restaurant from result set of google places
def find_restaurant(winner, google):
    for place in google:
        if place.name == winner:
            place.get_details()
            print(place)
            return place

    return None


# scrape yelp.com for restaurant's menu
def get_menu(winner, address):
    city = address.split(", ")
    name = winner.replace("'", "")
    name = name.replace("&", "and")
    name = "https://www.yelp.com/menu/" + name.replace(" ", "-") + "-" + city[1]

    return name


# parsse result set from yelp and create dicts
def filter_menu(menu):
    # section-header -> alternate -> innerHTML = category name

    # u-space-b3 -> menu-item -> arrange arrange--6 -> arrange_unit arrange_unit--fill 
    #   arrrange -> arrange_unit arrange_unit--fill menu-item-details | h4 innerHTML = food name | p innerHTML = description
    # ALTERNATIVELY: H4 innerHTML for dish name & P innerHTML for description

    # img class=photo-box-img == food image
    # li class=menu-item-price-amount = price

    # list of dist categories
    #   Dish name
    #   Dish price
    #   Dish discription
    # [{name: nname, price: pricee, description: desc, photo: pho}]

    for photo in menu.findAll("div", {'class':'photo-box'}):
        photo.decompose()

    for div in menu.findAll("div", {'class':'menu-item-details-stats'}):
        div.decompose()
