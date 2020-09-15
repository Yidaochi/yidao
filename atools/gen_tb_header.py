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
  inp_lst = []
  oup_lst = []
  max_len = 0
  port_sta_l = 0    # port list start line
  port_end_l = 0    # port list end line
  li = 0
  for ifl in i_fr.readlines():
    li = li + 1
    cmt = ifl[ifl.find("//"):]  # comment
    ctt = ifl[:ifl.find("//")]  # content
    # print("'%s'" % ctt)
    ifl_lst = re.split(r'[\s]+', ctt.strip(" "))
    # print(ifl_lst)
    if 'input' == ifl_lst[0]:
      inp_lst.append(ifl_lst)
      if len(ifl_lst) >= 3:
        if max_len < len(ifl_lst[1]):
          max_len = len(ifl_lst[1])
    elif 'output' == ifl_lst[0]:
      oup_lst.append(ifl_lst)
      if len(ifl_lst) >= 3:
        if max_len < len(ifl_lst[1]):
          max_len = len(ifl_lst[1])
    elif 'module' == ifl_lst[0]:
      port_sta_l = li
    elif ');' == 


  print('max_len', max_len)
  reg_lst = []
  for inp in inp_lst:
    # print("inp", inp)
    if len(inp) <= 2:
      reg_lst.append("%-*s%s" % (5+max_len+1, "reg", inp[1]))
      # print("%-*s%s" % (5+max_len+1, "reg", inp[1]))
    elif len(inp) == 3:
      reg_lst.append("%-5s%-*s%s" % ("reg", max_len+1, inp[1], inp[2]))
      # print("%-5s%-*s%s" % ("reg", max_len+1, inp[1], inp[2]))
    else:
      sig_name = "".join(inp[2:])
      reg_lst.append("%-5s%-*s%s" % ("reg", max_len+1, inp[1], sig_name))
      # print("%-5s%-*s%s" % ("reg", max_len+1, inp[1], sig_name))
  wire_lst = []
  for oup in oup_lst:
    # print("oup", oup)
    if len(inp) <= 2:
      wire_lst.append("%-*s%s" % (5+max_len+1, "wire", inp[1]))
      # print("%-*s%s" % (5+max_len+1, "wire", inp[1]))
    elif len(inp) == 3:
      wire_lst.append("%-5s%-*s%s" % ("wire", max_len+1, inp[1], inp[2]))
      # print("%-5s%-*s%s" % ("wire", max_len+1, inp[1], inp[2]))
    else:
      sig_name = "".join(inp[2:])
      wire_lst.append("%-5s%-*s%s" % ("wire", max_len+1, inp[1], sig_name))
      # print("%-5s%-*s%s" % ("wire", max_len+1, inp[1], sig_name))

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
