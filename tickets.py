# -*- coding: utf-8 -*-
"""Train tickets query via command-line.

Usage:
    tickets [-GCDTKZYO] (<from> <to> <date>)

Options:
    -h,--help   显示帮助菜单
    -G          高铁
    -C          城际
    -D          动车
    -T          特快
    -K          快速
    -Z          直达
    -Y          旅游
    -O          其他

Example:
    tickets beijing shanghai 2016-08-25
    tickets 北京 上海 明天
"""
import os
import re
import time
import logging
import logging.handlers
import requests
from res.stations import stations
from res.pinyin import PinYin
from train import TrainCollection
from docopt import docopt
from datetime import datetime, timedelta
from requests.packages.urllib3.exceptions import InsecureRequestWarning

logger = logging.getLogger(__name__)


def logger_init():
    path = './log'
    if not os.path.exists(path):
        os.makedirs(path)
    filename = path + '/all.log'
    fh = logging.handlers.RotatingFileHandler(filename, mode='a+', maxBytes=1048576, backupCount=3)
    fh.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s',
                        datefmt='%Y-%M-%d %H:%M:%S',
                        handlers=[sh, fh])


def get_arg():
    arguments = docopt(__doc__)
    # 当没有传入附加参数时 将默认参数均设置为True
    argkeys = ['-C', '-D', '-G', '-K', '-O', '-T', '-Y', '-Z']
    for key in argkeys:
        if arguments[key]:
            return arguments
    for key in argkeys:
        arguments[key] = True
    return arguments


def get_station_info(arguments):
    p2e = PinYin()
    p2e.load_word()
    try:
        from_station = stations.get(p2e.hanzi2pinyin(string=arguments['<from>']))
        if from_station is None:
            raise ValueError
        to_station = stations.get(p2e.hanzi2pinyin(string=arguments['<to>']))
        if to_station is None:
            raise KeyError
    except ValueError:
        logger.info('Invalid from_station name: {}'.format(arguments['<from>']))
        exit()
    except KeyError:
        logger.info('Invalid to_station name: {}'.format(arguments['<to>']))
        exit()
    else:
        return from_station, to_station


def get_date_info(arguments):
    tmp_date = arguments['<date>']
    trs = {'今天': 0, '明天': 1, '后天': 2, '大后天': 3, '0': 0, '1': 1, '2': 2, '3': 3}
    if tmp_date in trs.keys():
        now = datetime.today() + timedelta(days=trs[tmp_date])
        date = now.strftime('%Y-%m-%d')
    else:
        try:
            if len(tmp_date) == 10:
                date = tmp_date
            elif len(tmp_date) == 8:
                date = time.strftime('%Y-%m-%d', time.strptime(tmp_date, '%Y%m%d'))
            elif len(tmp_date) == 6:
                date = time.strftime('%Y-%m-%d', time.strptime(tmp_date, '%y%m%d'))
            else:
                raise Exception
        except:
            logger.info('Invalid date: {}'.format(arguments['<date>']))
            exit()
    return date


def get_urls(arguments):
    html = requests.get('https://kyfw.12306.cn/otn/leftTicket/init').text
    url_model = 'https://kyfw.12306.cn/otn/{}?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'
    query_code = re.search(r"CLeftTicketUrl = '(.*?)';", html).group(1)
    date = get_date_info(arguments)
    from_station, to_station = get_station_info(arguments)
    url = url_model.format(
        query_code, date, from_station, to_station
    )
    return url


def get_head():
    headers = {
        'Cookie': 'RAIL_DEVICEID=X27r3coZZsqOEYKcfbc0xY1_s5aYoCcX8-EzeZWGLUnNBaQVKrNcMwrr2ZscDxUDPEGmzyBRzcU54fvt5aDnvxRcgGhKv7hmP5LTsQiLIRZ8aN1SoBhtTgW6Zh9EBiltVGXjplRWU_IE_3OTRf7QarduXP-k6DKt;'
    }
    return headers


def cli():
    """command-line interface"""
    arguments = get_arg()
    headers = get_head()
    url = get_urls(arguments)
    try:
        response = requests.get(url, verify=False, headers=headers)
        logger.debug(response)
    except:
        logger.error('Timeout error!')
        exit()
    if response.status_code == requests.codes.ok:
        try:
            res_json = response.json()
        except:
            logger.warning('JSON parse failed. Try again.')
            exit()
        logger.debug(res_json)
        if res_json['status'] and res_json['data'] != '':
            rows = res_json['data']  # 一级解析
            trains = TrainCollection(rows, arguments)  # 二级解析 创建trains对象
            try:
                trains.pretty_print()
            except:
                logger.warning('prettytable print failed.')
                exit()
        else:
            logger.error('Result not found. Please check the code or contact with the author.')


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全请求警告
    logger_init()
    cli()
