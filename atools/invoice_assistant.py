#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@File Name :  invoice_assistant.py
@Author    :  Liu chi
@Email     :  liuchi@eswin.com
@Time      :  2020-11-26
@Desc      :  
"""
import os


def read_file(path):
  print("[info] path: '%s'" % path)
  for root, dirs, files in os.walk(path):
    for f in files:
      if 'pdf' in f:
        print(f)
def pdf_parser(pdf):
  print("pdf:", pdf)

def main():
  current_path = os.getcwd()
  read_file(current_path)
  pdf_parser('.\\21952885.pdf')

if __name__ == '__main__':
  main()

