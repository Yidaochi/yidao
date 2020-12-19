#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@File Name :  invoice_assistant.py
@Author    :  Liu Chi
@Email     :  liuchi@eswin.com
@Time      :  2020-11-26
@Desc      :  
"""
import os
import time

def read_path(path):
  print("[info] path: '%s'" % path)
  year = time.strftime("%Y")
  with open('info.txt', 'w') as inf:
    money_sum = 0
    date_lst  = []
    for root, dirs, files in os.walk(path):
      for f in files:
        if 'pdf' in f:
          date  = "%s-%s-%s; " % (year, f.split('-')[0], f.split('-')[1])
          date_lst.append(date)
          money = (f.split('-')[-1]).split('.pdf')[0]
          # print('money:', money)
          money_sum += float(money)
    print('money_sum:', money_sum)
    inf.write("Total %s days.\n" % len(date_lst))
    for date in date_lst:
      inf.write(date)
    inf.write("\nmoney_sum: %s\n" % str(money_sum))



def main():
  current_path = os.getcwd()
  read_path(current_path)

if __name__ == '__main__':
  main()

