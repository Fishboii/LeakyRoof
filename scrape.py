from bs4 import BeautifulSoup
import requests
import wget
import time
from PIL import Image
from math import sqrt
import os
import classify


def clrdiff(minclr, maxclr, clr):
    """only takes tupules/list (R, G, B)
    find % diff from minimum colour using vector length
    not entirely accurate in terms of colour intensity percentage but close enough"""
    # finally something for A level vectors!
    vectorlength = sqrt((maxclr[0] - minclr[0]) ** 2 + (maxclr[1] - minclr[1]) ** 2 + (maxclr[2] - minclr[2]) ** 2)
    diffclr = sqrt((clr[0] - minclr[0]) ** 2 + (clr[1] - minclr[1]) ** 2 + (clr[2] - minclr[2]) ** 2)
    return diffclr / vectorlength


def scrape(deletefile=False):
    """
    deletefile = False by default
    set True to delete png file after grabbing data
    """

    # process HTML from requests using bs4 parser
    html_page = requests.get('https://www.ema.gov.sg/solarmap.aspx')
    # mmm soup
    soup = BeautifulSoup(html_page.content, 'html.parser')

    # find location of image
    imglink = soup.findAll("img")[-1].attrs['src']

    # set file name as (year, month, day, hour, minute)
    filename = "irrdata20{}".format(time.strftime("%y, %m, %d, %H, %M", time.gmtime()).replace(", ", "") + ".png")

    # get image form imageurl
    wget.download('https://www.ema.gov.sg/' + imglink, out=filename)

    # load image into PIL
    im = Image.open(filename)

    # set of points in image to get colours of
    clr = []
    points = [(1389, 1120), (1313, 1141), (1212, 1082), (1179, 1149), (990, 1049), (1338, 1036), (1389, 1015),
              (1368, 952), (1292, 986), (1128, 948), (1208, 877), (1397, 868), (1502, 826), (1590, 919), (1569, 1011),
              (1871, 872), (2039, 726), (1783, 684), (1527, 654), (1191, 742), (977, 885), (570, 847), (881, 747),
              (583, 583), (906, 499), (1107, 591), (1162, 310), (1405, 541), (444, 1233), (1254, 1267), (58, 54),
              (2442, 163), (2446, 1384)]

    for i in points:
        clr.append(im.getpixel((i[0], i[1])))

    # convert colour of each pixel to %
    pctgclr = []
    for i in clr:
        pctgclr.append(clrdiff((0, 100, 0), (141, 239, 124), i))

    # check control variables
    if (pctgclr[-2], pctgclr[-1]) != (1.0, 0.0):
        raise NameError(
            "Minmax values does not match minmax points, min = {}, max = {}".format(pctgclr[-1], pctgclr[-2]))

    # plug numbers into csv file
    fileappend = open("data.csv", "a")
    # datetime
    fileappend.write("\n{}".format(time.strftime("%y, %m, %d, %H, %M", time.localtime()).replace(", ", "")))
    for i in range(len(pctgclr) - 3):
        # add value
        fileappend.write(", {}".format(pctgclr[i]))
    fileappend.close()

    if deletefile:
        # 10s before closing in order to make sure it is not being used
        time.sleep(10)
        os.remove(filename)

    elif not deletefile:
        time.sleep(10)


def weather():
    """Add weather data to csv file"""
    # get page and datasets
    html_page = requests.get('http://www.weather.gov.sg/weather-forecast-2hrnowcast-2/')
    soup = BeautifulSoup(html_page.content, 'html.parser')
    fileappend = open("data.csv", "a")
    for i in range(1, 49):
        # index 0 and 25 are titles, so skip them
        if i == 25:
            continue
        else:
            cls = soup.findAll('tr')[i]
            # something to do with encoding where \xa0 appears
            weather = cls.text.strip(" ").replace("\xa0", "")
            fileappend.write(", {}".format(classify.weather(weather.lower())))
    fileappend.close()
