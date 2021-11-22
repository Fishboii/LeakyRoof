import scrape
import time
while True:
    scrape.scrape(True)
    scrape.weather()
    print("\nwaiting for image update")
    time.sleep(300)