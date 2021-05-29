
import asyncio
from arsenic import get_session, keys, browsers, services
import pandas as pd
from requests_html import HTML 
import itertools
import time

import logging
import structlog #pip install structlog

def set_arsenic_log_level(level = logging.WARNING):
    #Create logger
    logger = logging.getLogger('arsenic')

    def logger_factory():
        return logger

    structlog.configure(logger_factory=logger_factory)
    logger.setLevel(level)

async def get_product_data(body_container):
    datas = []
    
    # print(f'ini list_containe{list_container}')

    for j in range(len(body_container)-1):

        # parse reviewer
        reviewerEl = await body_container[j].get_element(".DrjyGw-P._1SRa-qNz.NGv7A1lw._2yS548m8._2cnjB3re._1TAWSgm1._1Z1zA2gh._2-K8UW3T._2AAjjcx8")
        reviewer = await reviewerEl.get_text()

        # parse rating
        ratingEl = await body_container[j].get_element(".zWXXYhVR")
        rating = await ratingEl.get_attribute("title")
        rating = str(rating).split(" ")[0]

        # parse written_date
        written_dateEl = await body_container[j].get_element(".DrjyGw-P._26S7gyB4._1z-B2F-n._1dimhEoy")
        written_date = await written_dateEl.get_text()
        written_date = written_date.replace("Written", "")

        # parse review_title
        titleEl = await body_container[j].get_element("._2tsgCuqy")
        title = await titleEl.get_text()

        # parse review text
        review_El = await body_container[j].get_element(".DrjyGw-P._26S7gyB4._2nPM5Opx")
        review_textEl = await review_El.get_element("._2tsgCuqy")
        review_text = await review_textEl.get_text()
        review_text = review_text.replace("\n", " ")
        
        # branch
        branch = "Universal Studios Japan"

        # print(review)
        data = {
            'reviewer':reviewer,
            'rating':rating,
            'written_date':written_date,
            'title':title,
            'review_text':review_text,
            'branch':branch
        }
        datas.append(data)
    
    return datas

async def scraper(url):
    service = services.Chromedriver(binary='/Users/macbook/Documents/chromedriver')
    browser = browsers.Chrome()
    browser.capabilities = {
        "goog:chromeOptions": {"args": ["--headless", "--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage"]}
    }
    async with get_session(service, browser) as session:
        
        await session.get(url)
        body = await session.get_element("._1c8_1ITO")
        review_div = await session.get_elements("div._1c8_1ITO > div")
        product_data = await get_product_data(review_div)
        return product_data
  
async def run():
    results = []
    number_page = 5
    for i in range(0, number_page):
        url = f"https://www.tripadvisor.com/Attraction_Review-g34515-d102432-Reviews-or{i}0-Universal_Studios_Florida-Orlando_Florida.html"
        results.append(
            asyncio.create_task(scraper(url))
        )
    list_of_links = await asyncio.gather(*results)
    results = list(itertools.chain.from_iterable(list_of_links))
    return results

if __name__ == "__main__":
    set_arsenic_log_level()
    start = time.time()
    df = asyncio.run(run())
    df_review = pd.DataFrame(df)
    df_review.to_csv('universal_studios_japan.csv', index=False)
    end = time.time() - start
    print(f'total time is: {end}')