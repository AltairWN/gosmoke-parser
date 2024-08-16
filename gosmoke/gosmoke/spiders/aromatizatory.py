import scrapy


class AromatizatorySpider(scrapy.Spider):
    name = "aromatizatory"
    allowed_domains = ["gosmoke.ru"]
    start_urls = ["https://gosmoke.ru/aromatizatory"]

    def parse(self, response):
        if(response.url == "https://gosmoke.ru/"):
            return

        sectionList = response.css('.list-categories a::attr(href)').extract()

        if sectionList:
            for url in sectionList:
                yield scrapy.Request(response.urljoin(url + "?limit=500"), callback=self.parse)
            return

        productsList = response.xpath('//div[@id="content"]//a[@itemprop="url"]/@href').extract()

        if productsList:
            for url in productsList:
                yield scrapy.Request(response.urljoin(url), callback=self.parse)
            return

        productContent = response.xpath('//div[@id="content"]')

        if productContent:
            productData = {
                'name': productContent.css('h1::text').extract_first(),
                'description': productContent.css('.product-description p::text').extract_first(),
                'brand': response.css('.list-group-categories a.active::text')[1].extract(),
            }

            yield productData

        pass
