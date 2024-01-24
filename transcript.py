import scrapy


class TranscriptSpider(scrapy.Spider):
    name = "transcript"
    allowed_domains = ["www.listennotes.com"]
    start_urls = ["https://www.listennotes.com/best-podcasts/?sort_type=listen_score&region=us"]

    def parse(self, response):
        product_container = response.xpath('//div[@class="grid grid-cols-1 gap-4"]/div[contains(@class, "ln-page-card")]')

        counter = 0
        total = 0

        for product in product_container:
            transcript_exists = product.xpath('.//span[@class="text-black font-semibold text-sm"]')

            total += 1
            if transcript_exists:
                counter += 1
            else:
                pass

            pagination = response.xpath('//div[@class="grid grid-cols-1 gap-4"]/div[contains(@class, "ln-page-card flex justify-center")]')
            next_page_url = pagination.xpath('.//div/a[contains(@rel, "next")]/@href').get()

            if next_page_url:
                yield response.follow(url = next_page_url, callback= self.parse)

        print(f"Number of transcripts found: {counter}")
        print(f"Total number of Products: {total}")

            # yield{
            #    'transcript' : transcript_exists
            # }