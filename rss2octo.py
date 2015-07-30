# Required Libraries
import os
import re
import glob
# import html2text
from dateutil.parser import parse

import xml.etree.ElementTree as ET

nsDict = {
    'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
    'atom': 'http://www.w3.org/2005/Atom'
    }


# TODO take the file name from script arguments
tree = ET.parse('source/dw.xml').find("channel")

for item in tree.findall("item"):
    title = item.find("title").text

    guid = item.find("guid").text.strip()
    guid = guid.rsplit("?", 1)[1]

    pubDateOrig = item.find("pubDate").text
    pubDate = parse(pubDateOrig)
    description = item.find("description")
    summary = item.find("itunes:summary", namespaces=nsDict)
    image = item.find("itunes:image", namespaces=nsDict).attrib['href']
    duration = item.find("itunes:duration", namespaces=nsDict)

    enclosure = item.find("enclosure", namespaces=nsDict)
    if enclosure is not None:
        podfile = enclosure.attrib['url']
        podfileLength = enclosure.attrib['length']
    else:
        # error
        print "Error: No URL set for podcast: " + title

    # post name (and the URL of the post) is made of the date and the image file name

    # meaningful URLS ?
    #imgFileName = image.rsplit("/", 1)[1].rsplit(".", 1)[0]
    #filename = pubDate.strftime("%Y-%m-%d-") + imgFileName
    filename = pubDate.strftime("%Y-%m-%d-") + guid

    print filename
    print guid, "Title:", title, pubDate, description.text, \
        summary.text, image, duration.text, podfile

    f = open("source/_posts/" + filename + ".markdown", "w")
    f.write("---\n")
    f.write("layout: post\n")
    f.write("title: \"" + title.encode("UTF8") + "\"\n")
    f.write("date: " + str(pubDate) + "\n")
    f.write("comments: true\n")
    # f.write("categories:\n")
    # f.write("- Italy\n")
    f.write("filename: " + podfile + "\n")
    f.write("length: " + podfileLength + "\n")
    # f.write("summary:\n")
    f.write("---\n")
    f.write("\n")
    f.write("{% img " + image + " %}")
    f.close()