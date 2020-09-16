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
import time

#=============== Global parameters start ==============#
Author_name = "Yidaoliu"
Mail        = "bazhahei@hei.com"
#=============== Global parameters end   ==============#

def read_rtl(i_f):
  m_name = (i_f.split("/")[-1]).split(".")[0]   #module name
  print('module_name:', m_name)
  i_fr = open(i_f, "r")
  i_fr_l = i_fr.readlines()
  inp_lst = []
  oup_lst = []
  wth_max_len = 0   # width max len
  port_sta_l = 0    # port list start line
  port_end_l = 0    # port list end line
  port_end_flag = 0
  li = 0
  #   need add comparison between port list num and io port num in file content 
  for ifl in i_fr_l:
    li = li + 1
    cmt = ifl[ifl.find("//"):]  # comment
    ctt = ifl[:ifl.find("//")]  # content
    # print("'%s'" % ctt)
    ifl_lst = re.split(r'[\s]+', ctt.strip(" "))
    # print(ifl_lst)
    if 'input' == ifl_lst[0]:
      inp_lst.append(ifl_lst)
      if len(ifl_lst) >= 3:
        if wth_max_len < len(ifl_lst[1]):
          wth_max_len = len(ifl_lst[1])
    elif 'output' == ifl_lst[0]:
      oup_lst.append(ifl_lst)
      if len(ifl_lst) >= 3:
        if wth_max_len < len(ifl_lst[1]):
          wth_max_len = len(ifl_lst[1])
    elif 'module' == ifl_lst[0]:
      port_sta_l = li
    elif ');' == ifl_lst[0] and port_end_flag == 0:
      port_end_l = li
      port_end_flag = 1
  print('port_sta_l:', port_sta_l)
  print('port_end_l:', port_end_l)
  print('wth_max_len:', wth_max_len)
  reg_lst = []
  for inp in inp_lst:
    # print("inp", inp)
    if len(inp) <= 2:
      reg_lst.append("%-*s%s" % (5+wth_max_len+1, "reg", inp[1]))
      # print("%-*s%s" % (5+wth_max_len+1, "reg", inp[1]))
    elif len(inp) == 3:
      reg_lst.append("%-5s%-*s%s" % ("reg", wth_max_len+1, inp[1], inp[2]))
      # print("%-5s%-*s%s" % ("reg", wth_max_len+1, inp[1], inp[2]))
    else:
      sig_name = "".join(inp[2:])
      reg_lst.append("%-5s%-*s%s" % ("reg", wth_max_len+1, inp[1], sig_name))
      # print("%-5s%-*s%s" % ("reg", wth_max_len+1, inp[1], sig_name))
  wire_lst = []
  for oup in oup_lst:
    # print("oup", oup)
    if len(inp) <= 2:
      wire_lst.append("%-*s%s" % (5+wth_max_len+1, "wire", inp[1]))
      # print("%-*s%s" % (5+wth_max_len+1, "wire", inp[1]))
    elif len(inp) == 3:
      wire_lst.append("%-5s%-*s%s" % ("wire", wth_max_len+1, inp[1], inp[2]))
      # print("%-5s%-*s%s" % ("wire", wth_max_len+1, inp[1], inp[2]))
    else:
      sig_name = "".join(inp[2:])
      wire_lst.append("%-5s%-*s%s" % ("wire", wth_max_len+1, inp[1], sig_name))
      # print("%-5s%-*s%s" % ("wire", wth_max_len+1, inp[1], sig_name))

  sig_max_len = 0   # signal max len
  port_lst = []
  for i in range(port_sta_l, port_end_l-1):
    ifl = i_fr_l[i]
    ctt = ifl[:ifl.find("//")]  # content
    ifl_lst = re.split(r'\,', ctt.strip(" "))
    if ifl_lst[0] != "":
      port_lst.append(ifl_lst[0])
    if len(ifl_lst[0]) > sig_max_len:
      sig_max_len = len(ifl_lst[0])
  tie_line_lst = []
  tie_line_lst.append("%s %s_inst(" % (m_name, m_name))
  for p_i in range(len(port_lst)):
    p = port_lst[p_i]
    if p_i != len(port_lst) - 1:
      tie_line_lst.append("  .%-*s(%-*s)," % (sig_max_len+4, p, sig_max_len+4, p))
    else:
      tie_line_lst.append("  .%-*s(%-*s)" % (sig_max_len+4, p, sig_max_len+4, p))
  tie_line_lst.append(");")

  return reg_lst, wire_lst, tie_line_lst

def write_tb(tb_f_name, text, reg_lst, wire_lst, tie_line_lst):
  tb_fw = open(tb_f_name, "w")
  tb_name = tb_f_name.split('.')[0]
  #========== tb header start ==========#
  print("//==========================================================================") 
  print("//  File Name: %s" % (tb_f_name))
  print("//  Author: %s" % (Author_name))
  print("//  Mail: %s" % (Mail))
  print("//  Date: %s" % (time.strftime("%Y-%m-%d", time.localtime())))
  print("//  Function:")
  print("//    ")
  print("//  History:")
  print("//    %s  Initial version" % (time.strftime("%Y-%m-%d", time.localtime())))
  print("//==========================================================================")
  tb_fw.write("//==========================================================================\n") 
  tb_fw.write("//  File Name: %s\n" % (tb_f_name))
  tb_fw.write("//  Author: %s\n" % (Author_name))
  tb_fw.write("//  Mail: %s\n" % (Mail))
  tb_fw.write("//  Date: %s\n" % (time.strftime("%Y-%m-%d", time.localtime())))
  tb_fw.write("//  Function:\n")
  tb_fw.write("//    \n")
  tb_fw.write("//  History:\n")
  tb_fw.write("//    %s  Initial version\n" % (time.strftime("%Y-%m-%d", time.localtime())))
  tb_fw.write("//==========================================================================\n")
  #========== tb header end   ==========#
  #========== tb content start   ==========#
  text_arry = text.split("\n")
  for tl in text_arry:
    if re.match(r"module", tl):
      # print(tl)
      tb_fw.write("module %s;\n" % tb_name)
    elif "this line script start insert" in tl:
      # print("tl:'%s'" % tl)
      tb_fw.write("\n")
      for ipt in reg_lst:
        tb_fw.write("  %s\n" % ipt)
      tb_fw.write("\n")
      for opt in wire_lst:
        tb_fw.write("  %s\n" % opt)
      tb_fw.write("\n")
      for tie_line in tie_line_lst:
        tb_fw.write("  %s\n" % tie_line)
      tb_fw.write("\n")
    else:
      tb_fw.write("%s\n" % tl)
  #========== tb content end   ==========#
  tb_fw.close()


def tb_template():
  text = """\
`timescale 1ns/10ps
module template_tb;
  parameter NAME = "";
  parameter DUMP_FSDB = 1;
  parameter END_TIME = 1500;
  parameter CLK_PERIOD = 10;
  //this line script start insert
  
  // clock
  always
    #(CLK_PERIOD/2.0)  clk = ~clk;
  initial begin
    clk  = 1'b1;
    rst_n   = 1'b1;
    #CLK_PERIOD rst_n = 1'b0;
    #CLK_PERIOD rst_n = 1'b1;
  end

  //dump wave
  initial begin
    if (DUMP_FSDB == 1) begin
      $fsdbDumpfile("test.fsdb");
      $fsdbDumpvars("+all");
    end
    if (END_TIME != 0) begin
      #END_TIME;
      $finish;
    end
  end
endmodule
  """
  return text

def main():
  i_f = args.i
  tb_f_name = args.o

  reg_lst, wire_lst, tie_line_lst = read_rtl(i_f)
  text = tb_template()
  write_tb(tb_f_name, text, reg_lst, wire_lst, tie_line_lst)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
      description="This script for generating tb header",
      epilog="eg: ./gen_tb_header.py -f ../../works/counter.v -o ../tb/counter_tb3.v")
  parser.add_argument("-i",type=str, help="Your rtl file: [path]/a.v")
  parser.add_argument("-o",type=str, help="Output file name: *.v")
  args = parser.parse_args()

  main()
