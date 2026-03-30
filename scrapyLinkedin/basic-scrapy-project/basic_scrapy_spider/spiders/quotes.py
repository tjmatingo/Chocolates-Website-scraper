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

        summary_box = response.css('div.top-card-layout__card')
        item['name'] = summary_box.css('h1::text').get().strip()
        item['description'] = summary_box.css('h2::text').get().strip()

        # location

        try: 
            item['location'] = summary_box.css('div.top-card-layout__first-subline-item span::text').get()
        except: 
            item['location'] = summary_box.css('span.top-card__subline-item::text').get().strip()
            if 'followers' in item['location'] or 'connections' in item['location']:
                item['location'] = ' '

        item['followers'] = ''
        item['connections'] = ''

        for span_text in summary_box.css('div.not-first-middot span::text').getall():
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
        experience_blocks = response.css('li.experience-group__position')
        for block in experience_blocks:
            experience = {}
            # organisation profile url 
            experience['organisation_profile'] = block.css('h4 a::attr(href)').get(default='').split('?')[0]

            # location
            experience['location'] = block.css('p.experience-item__meta-item::text').get(default='').strip()


            try: 
                experience['description'] = block.css('p.show-more-less-text__text--more::text').get().strip()
            except Exception as e:
                print('experience --> desctiption', e)
                try:
                    experience['description'] = block.css('p.show-more-less-text__text--less::text').get().strip()
                except Exception as e:
                    print('experience --> desctiption', e)
                    experience['description'] = ''
            
            # time range
            try:
                data_ranges = block.css('span.data-range time::text').getall()

                if len(data_ranges) == 2:
                    experience['start_time'] = data_ranges[0]
                    experience['end_time'] = data_ranges[1]
                    experience['duration'] = block.css('span.data-range__duration::text').get()
                elif len(data_ranges) == 1:
                    experience['start_time'] = data_ranges[0]
                    experience['end_time'] = 'present'
                    experience['duration'] = block.css('span.data-range__duration::text').get()

            except Exception as e:
                print('experience --> time ranges', e)
                experience['start_time'] = ''
                experience['end_time'] = ''
                experience['duration'] = ''

            item['experience'].append(experience)