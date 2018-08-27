import scrapy

class DmozSpider(scrapy.Spider):
    name = "strings_rating"
    allowed_domains = ["https://www.stringforum.net/"]
    start_urls = [
        "https://www.stringforum.net/strings.php?sdnr=1721&count=1/",
    ]
    def parse(self, response):
        #filename = response.url.split("/")[-2]
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        output={}
        output['String']=response.xpath("//tr/td[@class='ya']/text()").extract_first()
        output['Adjective']=response.xpath("//span/text()").extract()
        output['Descriptions']=response.xpath("//table/tr/td[@class='z' and @colspan='7']/text()").extract_first().strip()
        
        #8個項目 name: 分數
        ratings=response.xpath("//td/img[@src='redsq8.gif' or @src='grsq8.gif']/@width").extract()[0:7]
        ratings.append(response.xpath("//tr/td[@bgcolor='#E0E0E0']/text()").extract()[1][0:2])
        items=response.xpath("//tr/td[@class='z' and @bgcolor='#C0C0C0']/text()").extract()[0:8]

        for item, rating in zip(items,ratings):
            name=item.strip()
            output[name]=rating
        yield output



# Today's goal 08/26
# Scrap all tecnifibre strings into one csv


    # take the size of each adjective:
    #response.xpath("//span/@style").extract_first()[-4:-2]
    #response.xpath("//span/@style").extract() #list of font sizes associated with adjectives

    # find all the adjectives to this string:
    #response.xpath("//span/text()").extract() #.strip() take out the preceeding

    # find the product description:
    #response.xpath("//table/tr/td[@class='z' and @colspan='7']/text()").extract_first().strip() #take out the preceeding

    # find all the ratings: first 7 elements
    #response.xpath("//td/img[@src='redsq8.gif' or @src='grsq8.gif']/@width").extract()[0:7]
    #response.xpath("//tr/td[@bgcolor='#E0E0E0']/text()").extract()[1][0:2] # the overall rating in percentage

    # find all the rating components: first 8 elements
    #response.xpath("//tr/td[@class='z' and @bgcolor='#C0C0C0']/text()").extract()[0:8]. #.strip() take out the preceeding


# Need to find a way to save the info

# Need to find a way to proceed to other pages/strings
