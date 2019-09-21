import scrapy

class PetiteKnitSpiser(scrapy.Spider):
    name = "petiteknit"
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        }
    start_urls  = ['https://www.petiteknit.com/collections/my-size-dansk/']
    def parse(self,response):
        link_css = 'div.reveal a::attr(href)'
        next_urls = response.css(link_css).getall()

        #with open('scraped_urls.csv','wb') as f:
        #    f.write(','.join(next_urls))
       
        for next_page in response.css('div.reveal a::attr(href)'):
            yield response.follow(next_page, callback=self.parse_recipe)
    
    def parse_recipe(self, response):
        instructions = response.css("div.product-details-wrapper").css("div.product-description.rte").css("p::text").getall()
        yield {
            'name': response.css("title::text").get().strip(),
            'language': instructions[0].split()[-1],
            'description': instructions[1],
            'size_guide': instructions[2],
            'size_available': instructions[3],
            'size': instructions[4],
            'knitting_gauge': instructions[5],
            'yarn': instructions[6],
        }

        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)

        # self.log('Saved file %s' % filename)
        
        # page = response.url.split("/")[-1]
        # title = response.css("title::text").get().strip()
        # instructions = response.css("div.product-details-wrapper").css("div.product-description.rte").css("p::text").getall()
        
        # # l = ItemLoader(item=ArtscraperItem(), response=response)
        # l.add_value('page', page)
        # l.add_value('title', self.authors_css)
        # l.add_value('price', self.alt_authors_css)
        # l.add_value('language', instructions[0].split()[-1])
        # l.add_value('description', instructions[1])
        # l.add_value('size_guide', instructions[2])
        # l.add_value('size_available', instructions[3])
        # l.add_value('size', instructions[4])
        # l.add_value('knitting_gauge', instructions[5])
        # l.add_value('yarn', instructions[6])
        # yield l.load_item()


class AuthorSpider(scrapy.Spider):
    name = 'author'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # follow links to author pages
        for href in response.css('.author + a::attr(href)'):
            yield response.follow(href, self.parse_author)

        # follow pagination links
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }