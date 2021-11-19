import MySQLdb
import requests
from scrapy import Selector

from MySpider import settings


conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', password='wangkai1995', db='article_spider', charset='utf8')
cusor = conn.cursor()


def crawl_ips():
    headers = {
        'User-Agent': settings.USER_AGENT
    }
    for i in range(1, 10):
        re = requests.get('https://www.kuaidaili.com/free/inha/{0}/'.format(i), headers=headers)
        selector = Selector(text=re.text)
        all_trs = selector.css('.table-bordered tbody tr')
        for tr in all_trs:
            ip_address = tr.css('td::text').extract()[0]
            port = tr.css('td::text').extract()[1]
            speed_str = tr.css('td::text').extract()[5]
            proxy_type = tr.css('td::text').extract()[3]
            if speed_str:
                speed = float(speed_str.split('秒')[0])
            else:
                speed = 0
            cusor.execute(
                "insert agent_ip(ip, port, proxy_type, speed) VALUES ('{0}', '{1}', '{2}', {3}) ON DUPLICATE KEY UPDATE ip=VALUES(ip)"
                    .format(ip_address, port, proxy_type, speed)
            )
            conn.commit()


class GetAgentIp:
    def delete_ip(self, ip):
        delete_sql = """DELETE FROM agent_ip WHERE ip = '{0}'""".format(ip)
        cusor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        http_url = 'http://wenshu.court.gov.cn/'
        proxy_url = 'http://{0}:{1}'.format(ip, port)
        try:
            proxy_dict = {'http': proxy_url}
            res = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            print('失效')
            self.delete_ip(ip)
            return False
        else:
            res_code = res.status_code
            if res_code >= 200 and res_code < 300:
                print('生效')
                return True
            else:
                print('失效')
                self.delete_ip(ip)
                return False

    def get_rand_ip(self):
        rand_sql = """SELECT ip, port FROM agent_ip ORDER BY RAND() LIMIT 1"""
        cusor.execute(rand_sql)
        for ip_info in cusor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            judge_res = self.judge_ip(ip, port)
            if judge_res:
                return 'http://{0}:{1}'.format(ip, port)
            else:
                return self.get_rand_ip()


if __name__ == '__main__':
    crawl_ips()
