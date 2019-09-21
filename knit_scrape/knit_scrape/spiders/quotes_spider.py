import scrapy

class PetiteKnitSpiser(scrapy.Spider):
    name = "petiteknit"
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        }

    def __init__(self, category=None, *args, **kwargs):
        super(PetiteKnitSpiser, self).__init__(*args, **kwargs)

        self.start_page_links = 'h1 a::attr(href)' #link to all the adresses from the startpage

    def start_request(self):
        urls  = ['https://www.petiteknit.com/collections/my-size-dansk',
                    ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_startpage)

    def parse_startpage(self,response):
        link_css = self.start_page_links
        self.logger.info(f'blogs in response.url? {"blogs" in response.url}. Response: {response.url}')
        for next_page in response.css(link_css).getall():
            if next_page is not None:
                parser = self.parse_blog if self.is_blog_url(next_page) else self.parse
                yield response.follow(next_page, callback=parser)
    
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)