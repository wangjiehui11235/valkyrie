# coding=utf-8

import config
import pdb
import datetime
from uqer import DataAPI
import uqer

class AdjustTradeDate(object):
    def __init__(self, **kwargs):
        self._conn = kwargs.get('conn', None)
        self._uqer_token = kwargs.get('uqer_token', None)
        is_uqer_init = kwargs.get('is_uqer', 0)
        if is_uqer_init == 0:
            uqer.Client(token=self._uqer_token)
     
    def _fetch_all_date(self, start_date, end_date, columns):
        field = 'calendarDate,' + columns
        df = DataAPI.TradeCalGet(exchangeCD=u"XSHG",beginDate=start_date,
                                 endDate=end_date, field=field,pandas="1")
        return df
        
    def custom_fetch_end(self, start_date, end_date, columns):
        df = self._fetch_all_date(start_date, end_date, columns)
        df = df[df[columns] == 1]
        str_trade_date_list = list(set(df['calendarDate']))
        trade_date_list = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in str_trade_date_list]
        return trade_date_list
    
if __name__ == '__main__':
    uqer_token = config.uqer_token
    adjust_trade = AdjustTradeDate(uqer_token = uqer_token)
    start_date = datetime.datetime(2018, 5, 29).date()
    end_date = datetime.datetime(2018, 8, 29).date()
    print(adjust_trade.custom_fetch_end(start_date, end_date, 'isWeekEnd'))
    