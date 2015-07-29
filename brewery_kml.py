#pip install dstk --user --allow-external dstk --allow-unverified pykml
from pykml.factory import KML_ElementMaker as KML
from lxml import etree

def generate_kml(breweries):
    #create a KML doc
    brewery_doc = KML.Document()

    for brewery in breweries:
         brewery_doc.append(
            KML.Placemark(
                KML.name(brewery['name']),
                KML.description(brewery['name']),
                KML.Point(
                      KML.coordinates(str(brewery['lon']) + ","  +
                                      str(brewery['lat'])+ "," + "0"))
            ))

    brewery_kml = KML.kml(brewery_doc)
    return etree.tostring(brewery_kml, pretty_print=True)