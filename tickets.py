
"""
Usage:
     tickets.py [-gdktz] <from> <to> <date>

Options:
     -h,--help   显示帮助菜单
     -g          高铁
     -d          动车
     -t          特快
     -k          快速
     -z          直达
"""

import requests
import station
from docopt import docopt
from prettytable import PrettyTable
from COLORAMA import Colored


def cli():
     arguments = docopt(__doc__)
     from_station = station.get_telecode(arguments['<from>'])
     to_station = station.get_telecode(arguments['<to>'])
     date = arguments['<date>']
     url = ('https://kyfw.12306.cn/otn/leftTicket/query?'
            'leftTicketDTO.train_date={}&'
            'leftTicketDTO.from_station={}&'
            'leftTicketDTO.to_station={}&'
            'purpose_codes=ADULT').format(date, from_station, to_station)
     r = requests.get(url)
     print(url)
     train_table = PrettyTable()
     train_table.field_names = ['车次', '车站', '时间', '历时', '一等座', '二等座', '软卧', '软座', '硬卧', '硬座', '无座']
     raw_trains = r.json()['data']['result']
     options = ''.join([key for key, value in arguments.items() if value is True])
     color = Colored()

     for trains in raw_trains:
          train = trains.split('|')
          train_no = color.yellow(train[3])
          initial = train[3][0].lower()
          from_station_telecode = train[6]
          to_station_telecode = train[7]
          from_station_name = color.red(station.get_name(from_station_telecode))
          to_station_name = (station.get_name(to_station_telecode))
          start_time = train[8]
          arrive_time = train[9]
          lishi = train[10]
          first_class_seat = train[31] or '--'
          second_class_seat = train[30] or '--'
          soft_sleep = train[23] or '--'
          soft_seat = train[24] or '--'
          hard_sleep = train[28] or '--'
          hard_seat = train[29] or '--'
          no_seat = train[26] or '--'
          if not options or initial in options:
               train_table.add_row([
                    train_no,
                    '\n'.join([from_station_name, to_station_name]),
                    '\n'.join([start_time, arrive_time]),
                    lishi,
                    first_class_seat,
                    second_class_seat,
                    soft_sleep,
                    soft_seat,
                    hard_sleep,
                    hard_seat,
                    no_seat
                    ])
     print(train_table)

if __name__ == '__main__':
     cli()





