import scrapy
import datetime
import math

## There are 100 lines in the table before any loading ##

def remove_years(d, years):
    try:
        return d.replace(year = d.year - years)
    except ValueError:
        return d + (date(d.year - years, 1, 1) - date(d.year, 1, 1))

def set_urls(current_date, lower_date, end_date):
    urls = []
    required_iter = math.ceil((current_date - end_date).days/100) 

    for _ in range(required_iter):
        
        ## Transform dates to datetime obj to use timestamp() 
        lower_bound = datetime.datetime(lower_date.year, lower_date.month, lower_date.day)    
        upper_bound = datetime.datetime(current_date.year, current_date.month, current_date.day)

        ## Timestamps to use url
        lower_unix = lower_bound.timestamp()
        upper_unix = upper_bound.timestamp()

        urls.append('https://ca.finance.yahoo.com/quote/GOOG/history?period1={:.0f}&period2={:.0f}&interval=1d&filter=history&frequency=1d'.format(lower_unix, upper_unix))

        current_date = lower_date - datetime.timedelta(days=1)
        lower_date = current_date - datetime.timedelta(days=100)
        
    return urls

class YahooSpider(scrapy.Spider):

    ## Get today's date and 100 days before today
    counter = 0
    first_date = datetime.date.today()
    current_date = first_date + datetime.timedelta(days=1)
    lower_date = current_date - datetime.timedelta(days=100)
    end_date = remove_years(first_date + datetime.timedelta(days=1), 20)
    

    name = 'yahoo_spider'
    start_urls = set_urls(current_date, lower_date, end_date)
    
    ## This url contains a row with null values
    ## start_urls = ['https://ca.finance.yahoo.com/quote/GOOG/history?period1=1427760000&period2=1430352000&interval=1d&filter=history&frequency=1d']

    def parse(self, response):
        COL_SELECTOR = 'table'
        TEST_SELECTOR = './/tbody/tr'


        for row in response.css(COL_SELECTOR).xpath(TEST_SELECTOR):

            DATE_SELECTOR = './/td[1]/span/text()'
            OPEN_SELECTOR = './/td[2]/span/text()'
            HIGH_SELECTOR = './/td[3]/span/text()'
            LOW_SELECTOR = './/td[4]/span/text()'
            CLOSE_SELECTOR = './/td[5]/span/text()'
            ADJ_CLOSE_SELECTOR = './/td[6]/span/text()'
            VOLUME_SELECTOR = './/td[7]/span/text()'
            
            RATIO_SELECTOR = './/td[2]/strong/text()'
            ACTION_SELECTOR = './/td[2]/span/text()'

            date1 = row.xpath(DATE_SELECTOR).extract_first()
            open1 = row.xpath(OPEN_SELECTOR).extract_first()
            high1 = row.xpath(HIGH_SELECTOR).extract_first()
            low1 = row.xpath(LOW_SELECTOR).extract_first()
            close1 = row.xpath(CLOSE_SELECTOR).extract_first()
            adj_close = row.xpath(ADJ_CLOSE_SELECTOR).extract_first()
            volume1 = row.xpath(VOLUME_SELECTOR).extract_first()

            ratio = row.xpath(RATIO_SELECTOR).extract_first()
            action1 = row.xpath(ACTION_SELECTOR).extract_first()

            if( open1 and high1 and low1 and close1 and adj_close and volume1 ):
                yield {
                    'date1': date1,
                    'open1': open1,
                    'high1': high1,
                    'low1': low1,
                    'close1': close1,
                    'adj_close': adj_close,
                    'volume1': volume1,
                    'company': 'GOOG',
                }
            elif(not high1):
                yield {
                    'date1' : date1,
                    'company' : 'GOOG',
                    'action': action1,
                    'ratio' : ratio,
                }