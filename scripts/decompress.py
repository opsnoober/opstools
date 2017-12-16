#!/usr/bin/env python
#-*- coding:utf-8 -*-
from __future__ import unicode_literals

'''
解压文件脚本
usage: decompress.py file_name[.tar.gz|.zip]
'''
__author__ = "kuilong.liu"

import tarfile
import zipfile
import os
import sys

def un_tar(file_name):
    tar = tarfile.open(file_name)
    names = tar.getnames()
    if os.path.isdir(file_name):
        pass
    else:
        os.mkdir(file_name+"_files")
        
    for name in names:
        tar.extract(name,file_name+"_files")
    tar.close()

def un_zip(file_name):
    zip_file = zipfile.ZipFile(file_name)
    if os.path.isdir(file_name):
        pass
    else:
        os.mkdir(file_name+"_files")
    for names in zip_file.namelist():
        zip_file.extract(names,file_name + "_files/")
    zip_file.close()
    

if __name__ == "__main__":
    file_name = sys.argv[-1]
    if file_name.endswith("tar.gz"):
        un_tar(file_name)
    elif file_name.endswith("zip"):
        un_zip(file_name)
    else:
        print "unknown file suffix"
