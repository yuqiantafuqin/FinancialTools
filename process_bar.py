#encoding:utf-8

import sys

def process_bar(di, loop_num, prefix_desc='', post_desc='', bar_len=50, style='#'):
    """
    进度条
    di - 当前循环数
    loop_num 总循环次数
    prefix_desc - 进度条标签，显示在最开头位置
    post_desc - 进度条标签，显示在后面位置
    bar_len - 进度条长度，一个长度为一个字符，默认50个字符长度
    style - 进度条填充的样式，默认为#，显示效果为[######      ]
    """  
    percent = 1. * di / loop_num   
    hashes = style * int(percent * bar_len)   
    spaces = ' ' * (bar_len - len(hashes))   
    sys.stdout.write("\r%s %s/%s %s [%s] %d%%" % (prefix_desc, di, loop_num, post_desc, hashes + spaces, percent * 100))   
    sys.stdout.flush()  
    if di == loop_num: 
        sys.stdout.write('\n')
        sys.stdout.flush() 
    
