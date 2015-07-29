#!/usr/bin/env python2.7
from bs4 import BeautifulSoup
import urllib2
import re
#pip install dstk --user --allow-external dstk --allow-unverified dstk
import dstk
from brewery_kml import generate_kml



def get_coordinates(address):
    geocoder = dstk.DSTK()
    resp = geocoder.street2coordinates(address)
    if resp[address]:
        lat = resp[address]["latitude"]
        lon = resp[address]["longitude"]
        return lat, lon

    #Return lat = 0, lon = 0 when response is None
    return 0, 0

def clean_address(addr):
     #Need to remove NAME CHANGE and Date from the value
     r = re.sub(r"(NAME CHANGE|CLOSED|MOVED|NO BREWING HERE) \d{4}$", " ", addr)
     return r

def clean_cells(cell):
    if cell.string:
         data = " ".join(cell.string.split())
         return data
    else:
        return "Missing"

def get_breweries(html_tables):
    breweries = []
    for table in html_tables:
        cells = table.find_all("td")
        name = clean_cells(cells[0])
        address = clean_address(clean_cells(cells[1]))
        phone = clean_cells(cells[2])
        website =  clean_cells(cells[3])
        city_st_zip = clean_cells(cells[4])
        lat, lon =  get_coordinates(address + " " + city_st_zip)

        if not lat or not lon:
            continue

        brewery = {"name":name,
               "address":address,
               "phone":phone,
               "website":website,
               "city_st_zip":city_st_zip,
               "lat": lat,
               "lon": lon}

        breweries.append(brewery)
    return breweries


def cheers(state):
    print "Getting brewery page for %s ...." % state

    try:
        r = urllib2.urlopen("http://www.bcca.com/services/pf/usbl_%s.asp" % state)
        r.encoding = 'windows-1252'
    except urllib2.HTTPError:
        print "Could not access site...moving to back files"
        r = open("brewgeo/bcca_pages/BCCA_MI.html", "r")

    html = BeautifulSoup(r)
    html_tables = html.find_all(id="table4")
    print "Scraping Tables...."
    breweries = get_breweries(html_tables)
    print "Generating KML File"
    kml = generate_kml(breweries)
    kml_file = open("brewgeo/kml/%s_BCCA_Breweries.kml" % state, "w")
    kml_file.write(kml)
    kml_file.close()
    print "KML file saved"


if __name__ == "__main__":
    state = raw_input("Please Enter the State Abbreviation: ")
    cheers(state)