# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LagouJobItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()


class LagouJobItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    title = scrapy.Field()
    min_salary = scrapy.Field()  # 薪资
    max_salary = scrapy.Field()
    city = scrapy.Field()  # 城市
    min_experience = scrapy.Field()  # 经验
    max_experience = scrapy.Field()
    education = scrapy.Field()  # 学历
    post = scrapy.Field()  # 岗位
    category = scrapy.Field()  # 类型
    label = scrapy.Field()  # 标签
    company = scrapy.Field()  # 公司
    release_time = scrapy.Field()  # 发布时间
    temptation = scrapy.Field()  # 职位诱惑
    description = scrapy.Field()  # 职位描述
    address = scrapy.Field()  # 地址


class LagouCompanyItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    name = scrapy.Field()
    city = scrapy.Field()  # 城市
    signature = scrapy.Field()  # 签名
    scale = scrapy.Field()  # 规模
    business = scrapy.Field()  # 工商信息
    establish_time = scrapy.Field()  # 成立时间
    registered_capital = scrapy.Field()  # 注册资本
    legal_person = scrapy.Field()  # 法人代表
    description = scrapy.Field()  # 描述
