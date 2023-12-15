import json
import re

import scrapy


class TomatoSpider(scrapy.Spider):
    name = "tomato"
    allowed_domains = ["www.rottentomatoes.com"]

    def start_requests(self):
        for i in range(100):
            url = "https://www.rottentomatoes.com/napi/browse/movies_in_theaters/sort:popular?page=" + (i + 1).__str__()
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        data = response.json()
        for num, item in enumerate(data['grid']['list']):
            link = item['mediaUrl']
            if link:
                print("https://www.rottentomatoes.com" + link)
                yield scrapy.Request(url="https://www.rottentomatoes.com" + link, callback=self.parse_uurl)

    def parse_uurl(self, response):
        # print(response.text)
        script_content = response.xpath('//script[contains(text(), "dataLayer.push")]/text()').get()
        #
        # # 使用正则表达式提取"titleId"
        title_id_match = re.search(r'"titleId":"([^"]+)"', script_content)
        # # title_id_match = "cb28c837-b943-4ed8-9e4a-b1db47fcc59a"
        # print(title_id_match.group(1))
        print("https://www.rottentomatoes.com/napi/movie/" + title_id_match.group(1) + "/reviews/all")
        yield scrapy.Request(
            url="https://www.rottentomatoes.com/napi/movie/" + title_id_match.group(1) + "/reviews/all",
            callback=self.parse_comment)

    def parse_comment(self, response):
        # print(response.text)
        data = response.json()
        all_data=[]
        for num, item in enumerate(data['reviews']):
            quote = item['quote']
            score = item['scoreSentiment']
            # print(quote)
            # print(score)
            data = {"quote": quote, "score": score}
            all_data.append(data)
        file_path = "data.json"
        with open(file_path, "a") as json_file:
            json.dump(all_data, json_file)
