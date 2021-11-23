import scrape
import time
import logging
import traceback
logging.basicConfig(filename='uhoh.log', filemode='w')

while True:

    try:
        scrape.scrape(True)
        scrape.weather()
        print("\nPing at {}".format(time.strftime("%H, %M", time.localtime())))
        time.sleep(290)

    except Exception as e:
        # Past errors are only with deleting files, so loop does not stop assuming only that happens
        print("uhoh, something bad happened, program hasnt stopped but might not scrape data correctly")
        logging.error(time.strftime("%y, %m, %d, %H, %M", time.gmtime())+traceback.format_exc())

