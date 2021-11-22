import scrape
import time
while True:
    scrape.scrape(True)
    scrape.weather()
    print("\nPing at {}".format(time.strftime("%H, %M", time.localtime())))
    time.sleep(300)