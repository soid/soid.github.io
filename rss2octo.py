from dateutil.parser import parse
import xml.etree.ElementTree as ET

# read input file
# TODO take the file name from script arguments
tree = ET.parse('source/dw.xml').find("channel")

# RSS namespaces
nsDict = {
    'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
    'atom': 'http://www.w3.org/2005/Atom'
    }

# Translit russian titles for latin spelled URLs
# taken from http://ruprog.net/ru/knowledge/python/183/
def translit(locallangstring):
    conversion = {
        u'\u0410' : 'A',    u'\u0430' : 'a',
        u'\u0411' : 'B',    u'\u0431' : 'b',
        u'\u0412' : 'V',    u'\u0432' : 'v',
        u'\u0413' : 'G',    u'\u0433' : 'g',
        u'\u0414' : 'D',    u'\u0434' : 'd',
        u'\u0415' : 'E',    u'\u0435' : 'e',
        u'\u0401' : 'Yo',   u'\u0451' : 'yo',
        u'\u0416' : 'Zh',   u'\u0436' : 'zh',
        u'\u0417' : 'Z',    u'\u0437' : 'z',
        u'\u0418' : 'I',    u'\u0438' : 'i',
        u'\u0419' : 'Y',    u'\u0439' : 'y',
        u'\u041a' : 'K',    u'\u043a' : 'k',
        u'\u041b' : 'L',    u'\u043b' : 'l',
        u'\u041c' : 'M',    u'\u043c' : 'm',
        u'\u041d' : 'N',    u'\u043d' : 'n',
        u'\u041e' : 'O',    u'\u043e' : 'o',
        u'\u041f' : 'P',    u'\u043f' : 'p',
        u'\u0420' : 'R',    u'\u0440' : 'r',
        u'\u0421' : 'S',    u'\u0441' : 's',
        u'\u0422' : 'T',    u'\u0442' : 't',
        u'\u0423' : 'U',    u'\u0443' : 'u',
        u'\u0424' : 'F',    u'\u0444' : 'f',
        u'\u0425' : 'H',    u'\u0445' : 'h',
        u'\u0426' : 'Ts',   u'\u0446' : 'ts',
        u'\u0427' : 'Ch',   u'\u0447' : 'ch',
        u'\u0428' : 'Sh',   u'\u0448' : 'sh',
        u'\u0429' : 'Sch',  u'\u0449' : 'sch',
        u'\u042a' : '"',    u'\u044a' : '"',
        u'\u042b' : 'Y',    u'\u044b' : 'y',
        u'\u042c' : '\'',   u'\u044c' : '\'',
        u'\u042d' : 'E',    u'\u044d' : 'e',
        u'\u042e' : 'Yu',   u'\u044e' : 'yu',
        u'\u042f' : 'Ya',   u'\u044f' : 'ya',
    }
    translitstring = []
    for c in locallangstring:
        translitstring.append(conversion.setdefault(c, c))
    return ''.join(translitstring)

# conversion RSS -> YaML loop
for item in tree.findall("item"):
    title = item.find("title").text

    guid = item.find("guid").text.strip()
    guid = guid.rsplit("?", 1)[1]

    pubDateOrig = item.find("pubDate").text
    pubDate = parse(pubDateOrig)
    description = item.find("description").text
    summary = item.find("itunes:summary", namespaces=nsDict)
    image = item.find("itunes:image", namespaces=nsDict).attrib['href']
    duration = item.find("itunes:duration", namespaces=nsDict)


    # # # # #
    # check extracted vars
    if description is None:
        description = ""

    enclosure = item.find("enclosure", namespaces=nsDict)
    if enclosure is not None:
        podfile = enclosure.attrib['url']
        podfileLength = enclosure.attrib['length']
    else:
        # error
        print "Error: No URL set for podcast: " + title


    # # # # #
    # post name (and the URL of the post) is made of the date and the image file name

    # meaningful URLS ?
    #imgFileName = image.rsplit("/", 1)[1].rsplit(".", 1)[0]
    #filename = pubDate.strftime("%Y-%m-%d-") + imgFileName
    filename = pubDate.strftime("%Y-%m-%d-") \
               + translit(title) \
        .replace(" ", "_") \
        .replace("/", "_") \
        .replace("\"", "") \
        .replace("?", "_")

    print filename, title
#    print guid, "Title:", title, pubDate, description, \
#        summary.text, image, duration.text, podfile


    # # # # #
    # writing YAML
    f = open("source/_posts/" + filename + ".markdown", "w")
    f.write("---\n")
    f.write("layout: post\n")
    f.write("title: \"" + title.replace("\"", "\\\"").encode("UTF8") + "\"\n")
    f.write("date: " + str(pubDate) + "\n")
    f.write("comments: true\n")
    # f.write("categories:\n")
    # f.write("- Italy\n")
    f.write("filename: " + podfile + "\n")
    f.write("length: " + podfileLength + "\n")
    # f.write("summary:\n")
    f.write("---\n")
    f.write("\n")
    f.write(description.encode("utf-8"))
    f.close()
