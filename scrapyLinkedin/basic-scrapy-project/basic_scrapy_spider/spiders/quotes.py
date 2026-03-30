import scrapy


class LinkedInPeopleProfileSpider(scrapy.Spider):
    name = 'linkedIn_people_profile'

    async def start(self):
        profile_list = ['reidhoffman']
        for profile in profile_list:
            linked_people_url = f'https://www.linkedin.com/in/{profile}/'
            yield scrapy.Request(url=linked_people_url, callback=self.parse_profile, meta={'profile':profile, 'linkedin_url':linked_people_url})


    def parse_profile(self, response):
        item = {}
        item['profile'] = response.meta['profile']
        item['url'] = response.meta['linkedin_url']

        '''
        SUMMARY SECTION
        '''

        summary_box = response.css('section.top-card-layout')
        item['name'] = summary_box.css('h1::text').get().strip()
        item['description'] = summary_box.css('h2::text').get().strip()