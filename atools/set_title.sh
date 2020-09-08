#!/bin/bash
#==========================================================================
#  File Name: set_title.sh
#  Author: Yidaochi
#  Created Time: Fri 04 Sep 2020 01:15:18 AM CST
#  only for csh
#==========================================================================

#add line in your cshrc: alias set_title="echo -e "\033]0;$1\007"" 
echo -e "\033]0;$1\007"
