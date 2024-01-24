import scrapy
# Scrapy docs : https://docs.scrapy.org/en/2.7/topics/request-response.html#scrapy.http.Response.follow

class WorldometerSpider(scrapy.Spider):
    name = "worldometer"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["http://www.worldometers.info/world-population/population-by-country/"]

    def parse(self, response):
        #title = response.xpath('//h1/text()').get()

        # Xpath points to the name of the countries
        countries = response.xpath('//td/a')

        for country in countries:
            # This returns the text of the names of the ocuntries
            country_name = country.xpath(".//text()").get()

            # Getting links listed in a website
            link = country.xpath(".//@href").get()

            # yield scrapy.Request(url=absolute_url)


            # the 3 different ways to retreive URL's in Scrapy
            ################ absolute_url #############
            # absolute_url = f'https://www.worldometers.info/{link}'
            # absolute_url = response.urljoin(link)

            ############ relative url #############

            yield response.follow(url=link, callback=self.parse_country, meta={'country': country_name})


    def parse_country(self, response):
        country = response.request.meta['country']
        rows = response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        #response.xpath("(//table[contains(@class,'table')])[1]/tbody/tr") This is another way to do it.


        # Traverse through the rows
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()


            # return these as a dictionary and export it as a csv file
            # by running scrapy crawl worldometer -o population_with_countries.json
            # command: scrapy crawl 'name of file' -o 'name-of-the-json-file'.json
            yield{
                'country': country,
                'year': year,
                'population': population
            }