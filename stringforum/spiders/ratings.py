import scrapy
import numpy as np 
from scrapy import Request
from stringforum.items import StringRating 
from scrapy.spiders import CrawlSpider, Rule

class SFSpider(scrapy.Spider):
    name = "ratings"
    allowed_domains = ["www.stringforum.net"]
    start_urls = [
        "https://www.stringforum.net/stringsearch.php?start=0&limit=50&minbew=1&details=1/",
        ]


    def parse(self, response):
        for row in response.xpath("//table[@bgcolor='#0A0A0A']/tr[@bgcolor='#C0C0C0']"):
            name=row.xpath("./td/a[@class='y']/text()").extract()[0]
            rts=row.xpath("./td/a[@class='y']/text()").extract()[1]
            if row.xpath("./td[@align='right']/text()").extract_first():
                PPR=float(row.xpath("./td[@align='right']/text()").extract_first())
            else:
                PPR=np.nan

            # Need to handle exception here
            if row.xpath("./td/img[@src='grsq8x.gif' or @src='redsq8x.gif']/@width").extract_first():
                overall=float(row.xpath("./td/img[@src='grsq8x.gif' or @src='redsq8x.gif']/@width").extract_first())
            else:
                overall=0

            # Error handling, there are 'transparent.gif'
            ratings=[float(x) for x in row.xpath("./td/img[@src='redsq8.gif' or @src='grsq8.gif' or @src='grysq8.gif' or @src='transparent.gif']/@width").extract()]
            
            good_or_bad=row.xpath("./td/img[@src='redsq8.gif' or @src='grsq8.gif' or @src='grysq8.gif' or @src='transparent.gif']/@src").extract()
            for idx, tag in enumerate(good_or_bad):
                if tag=='redsq8.gif':
                    ratings[idx]=-1*ratings[idx]
                elif (tag == 'grysq8.gif') or (tag=='transparent.gif'):
                    ratings[idx]=0
            ratings_scaled=[x/42 for x in ratings] # For Luxilon 82/120 >> average plus or minus

            output=StringRating()#
            output['name']=name
            output['rts']=rts

            output['Durability']=ratings_scaled[0]
            output['Power']=ratings_scaled[1]

            output['Control']=ratings_scaled[2]
            output['Feel']=ratings_scaled[3]

            if len(ratings)>4:
                output['Comfort']=ratings_scaled[4]
                output['Spin']=ratings_scaled[5]
                output['Tension_Stability']=ratings_scaled[6]
            else:
                output['Comfort']=np.nan
                output['Spin']=np.nan
                output['Tension_Stability']=np.nan

            output['Overall']=overall/42
            output['PPR']=PPR
            yield output
        
        next_page = response.xpath("//*[contains(text(),'Next')]/@href").extract_first()
        if next_page is not None:
            next_page_url=response.urljoin( next_page )
            print('Visited :',next_page_url)
            yield Request(next_page_url, callback=self.parse)





