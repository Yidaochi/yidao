#!/usr/bin/python3
#==========================================================================
#  File Name: gen_tb_header.py
#  Author: Yidaoliu
#  Mail:
#  Created Time: 2020-09-09
#  Function:
#==========================================================================
import argparse
import sys
import re

def read_rtl(i_f):
  i_fr = open(i_f, "r")
  for ifl in i_fr.readlines():
    cmt = ifl[ifl.find("//"):]  # comment
    ctt = ifl[:ifl.find("//")]  # content
    ifl_lst = re.split(r'[\s]+',ctt)
    if re.match(r'input', ctt):
      print(ifl)
      #print("input: %s" % ifl_lst[1:])
      if len(ifl_lst[1:]) <= 1:
        pass#print("%-45s %s" % ('reg', ifl_lst[1]))
    if re.match(r'output', ctt):
      print(ifl)
      #print("output: %s" % ifl_lst[1:])
      if len(ifl_lst[1:]) <= 1:
        pass#print("%-45s %s" % ('wire', ifl_lst[1]))

def write_tb(text):
  text_arry = text.split("\n")
  for l in text_arry:
    #print("l:'%s'" % l)
    pass


def tb_template():
  text = """\
//==========================================================================
//  File Name: template_tb.v
//  Author: Yidaoliu
//  Mail: bazhahei@hei.com
//  Date: 2020-09-09
//  Function:
//    
//  History:
//    2020-09-09  Initial version
//==========================================================================
`timescale 1ns/10ps
module template_tb;
  parameter NAME = "";
  parameter DUMP_FSDB = 1;
  parameter END_TIME = 1500;
  parameter CLK_PERIOD = 10;
  
  // clock
  always
    #(CLK_PERIOD/2.0)  clk = ~clk;
  initial
  begin
    clk  = 1'b1;
    rst_n   = 1'b1;
    #CLK_PERIOD rst_n = 1'b0;
    #CLK_PERIOD rst_n = 1'b1;
  end

  initial
  begin
    if (DUMP_FSDB == 1)
    begin
      $fsdbDumpfile("test.fsdb");
      $fsdbDumpvars("+all");
    end
    if (END_TIME != 0)
    begin
      #END_TIME;
      $finish;
    end
  end
endmodule
  """
  return text

def main():
  i_f = args.f
  read_rtl(i_f)

  text = tb_template()
  write_tb(text)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
      description="This script for generating tb header",
      epilog="eg: ./gen_tb_header.py -f ../../works/counter.v -o ../tb/counter_tb3.v")
  parser.add_argument("-f",type=str, help="Your rtl file: [path]/a.v")
  parser.add_argument("-o",type=str, help="Output file name: [path]/*.v")
  args = parser.parse_args()

  main()
