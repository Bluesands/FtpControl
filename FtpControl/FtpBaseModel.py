#/usr/bin/env python
# -*- coding: utf-8 -*-
from ftplib import FTP
import os
import sys
import socket
import ConfigParser


class FtpBase(object):

    def __init__(self, project_conf_name):
        self.project_conf_name = project_conf_name
        self.ftp = FTP()
        self.__base_dir = os.getcwd()

        self.__host = self.getconf()[0]
        self.__port = self.getconf()[1]
        self.__pasv = self.getconf()[2]
        self.__username = self.getconf()[3]
        self.__password = self.getconf()[4]
        self.remote_project_rootdir = self.getconf()[5]
        self.local_project_rootdir = self.getconf()[6]
        self.suffix_files = self.getconf()[7]
        self.abs_files = self.getconf()[8]
        self.ignore_dirs = self.getconf()[9]
        self.project_name = self.login()

    def __del__(self):
        print "关闭ftp连接"
        self.ftp.close()
        print "退出fpt"
        self.ftp.quit

    def getconf(self):
        conf = ConfigParser.ConfigParser()
        conf.read(os.path.join(self.__base_dir,
                               'conf/{0}.ini'.format(self.project_conf_name)))
        host = conf.get('server', 'host')
        port = conf.get('server', 'port')
        pasv = conf.get('pasv', 'set_pasv')
        username = conf.get('user', 'username')
        password = conf.get('user', 'password')
        remote_project_rootdir = conf.get(
            'project_dir', 'remote_project_rootdir')
        local_project_rootdir = conf.get(
            'project_dir', 'local_project_rootdir')
        suffix_files = conf.get('ignore_files', 'suffix_files')
        abs_files = conf.get('ignore_files', 'abs_files')
        ignore_dirs = conf.get('ignore_dirs', 'dirs')

        cfg = [host, port, pasv, username, password, remote_project_rootdir,
               local_project_rootdir, suffix_files, abs_files, ignore_dirs]
        return cfg

    def __choice_project(self, ftp):
        if os.path.isfile('remote_project_name/{0}'.format(self.project_conf_name)):
            project_name = open(
                'remote_project_name/{0}'.format(self.project_conf_name)).readline()
        else:
            if self.remote_project_rootdir == "/":
                fl = ftp.nlst()
                for i in range(len(fl)):
                    print i + 1, fl[i]
                input_word = raw_input("请选择项目文件夹:\n")
                try:
                    project_name = fl[int(input_word) - 1]
                except:
                    project_name = self.local_project_rootdir.split("/")[-1]
            else:
                project_name = self.remote_project_rootdir.split("/")[-1]

            with open('remote_project_name/{0}'.format(self.project_conf_name), 'wt') as f:
                f.write(project_name)
        return project_name

    def login(self):

        ftp = self.ftp
        try:
            socket.setdefaulttimeout(60)
            # 0主动模式 1 被动模式
            ftp.set_pasv(self.__pasv)
            ftp.connect(self.__host, self.__port)
            ftp.login(self.__username, self.__password)
            print '成功登录到{0}'.format(self.__host)
        except:
            print "连接或登录失败"
            print "请检查ftp用户名和密码是否有误"
            sys.exit(1)
        project_name = self.__choice_project(ftp)
        return project_name
