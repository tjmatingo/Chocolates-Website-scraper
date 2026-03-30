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

        # location

        try: 
            item['location'] = summary_box.css('div.top-card__subline-item::text').get()
        except: 
            item['location'] = summary_box.css('span.top-card__subline-item::text').get().strip()
            if 'followers' in item['location'] or 'connections' in item['location']:
                item['location'] = ' '

        item['followers'] = ''
        item['connections'] = ''

        for span_text in summary_box.css('span.top-card__subliner-item::text').getall():
            if 'followers' in span_text:
                item['followers'] = span_text.replace('followers', '').strip()
            if 'connections' in span_text:
                item['connections'] = span_text.replace('connections', '').strip()


        """
        ABOUT SECTION
        """
        item['about'] = response.css('section.summary div.core-section-container__content p::text').get(default='')

        '''
        EXPERIENCE SECTION
        '''

        item['experience'] = []
        experience_block = response.css('li.experience-item')