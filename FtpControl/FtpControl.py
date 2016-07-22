#/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import sys
from FtpBaseModel import FtpBase


class FtpControl(FtpBase):

    def __init__(self, project_conf_name):
        super(FtpControl, self).__init__(project_conf_name)
        self.file_relative_path = self.__get_local_file_dir()
        self.all_upload_files = self.__ignore()
        self.total_upload_files = len(self.all_upload_files)

    def __get_local_file_dir(self):
        if not os.path.isdir(self.local_project_rootdir):
            print "本地项目根目录不存在或错误,请检查本地项目根目录配置."

        for root, dirs, files in os.walk(self.local_project_rootdir):
            for f in files:
                absdir = os.path.join(root, f)
                file_relative_path = absdir[
                    len(self.local_project_rootdir) + 1:]
                yield file_relative_path

    def __ignore_suffix(self, all_upload_files):
        suffix = list(set([f.split('.')[-1] for f in all_upload_files]))
        # ignore suffix file
        ignored_suffix_file = []
        if len(self.suffix_files):
            for s in self.suffix_files.split(','):
                if s not in suffix:
                    print "{0}后缀文件不存在,请检查配置文件忽略后缀选项".format(s)
                    sys.exit(1)
                else:
                    for f in all_upload_files:
                        if f.endswith(s):
                            ignored_suffix_file.append(f)

            all_upload_files = [
                f for f in all_upload_files if f not in ignored_suffix_file]
        else:
            print "未设置忽略后缀文件"
        return all_upload_files

    def __ignore_dirs(self, all_upload_files):
        dirs = list(set([os.path.dirname(f) for f in all_upload_files]))
        # ignore dir
        ignored_dirs = []
        if len(self.ignore_dirs):
            for d in self.ignore_dirs.split(','):
                if d not in dirs:
                    print "忽略文件夹{0}不存在,请检查项目配置文件忽略文件夹选项".format(d)
                    sys.exit(1)
                else:
                    for f in all_upload_files:
                        if d in os.path.dirname(f):
                            ignored_dirs.append(f)

            all_upload_files = [
                f for f in all_upload_files if f not in ignored_dirs]
        else:
            print "未设置忽略目录"
        return all_upload_files

    def __ignore_absfile(self, all_upload_files):
        # ignore absfile
        ignored_absfile = []
        if len(self.abs_files):
            for f in self.abs_files.split(','):
                try:
                    all_upload_files.remove(f)
                    ignored_absfile.append(f)
                except:
                    print "忽略文件{0}不存在".format(f)
                    sys.exit(1)
        else:
            print "未设置忽略文件"
        return all_upload_files

    def __ignore(self):
        all_upload_files = [f for f in self.file_relative_path]

        # ignore suffix file
        all_upload_files = self.__ignore_suffix(all_upload_files)

        # ignore dir
        all_upload_files = self.__ignore_dirs(all_upload_files)

        # ignore absfile
        all_upload_files = self.__ignore_absfile(all_upload_files)

        return all_upload_files

    def __cwd_dir(self, dir):
        try:
            self.ftp.cwd(dir)
        except:
            self.ftp.mkd(dir)
            print "创建文件夹{0}成功".format(dir)
            self.ftp.cwd(dir)

    def __mkdirs(self, dir):
        for dirname in dir.split("/"):
            self.__cwd_dir(dirname)

    def __upload(self, filename, fb, filerootdir, text):
        self.ftp.storbinary('STOR {0}'.format(filename), fb)
        print "{0}文件{1}成功".format(text, filerootdir)

    def __timewrite(self):
        with open('runtime/{0}'.format(self.project_conf_name), 'w+') as f:
            filetime = time.localtime()
            line = time.strftime('%Y-%m-%d %H:%M:%S', filetime)
            f.write(line)

    def __traverse_file(self):
        for filerootdir in self.all_upload_files:
            self.__cwd_dir("/" + self.project_name)
            dirs = os.path.dirname(filerootdir)
            local_file_path = os.path.join(
                self.local_project_rootdir, filerootdir)
            dirfile = os.path.basename(filerootdir)
            fb = open(local_file_path, 'rb')

            filemtime = time.localtime(os.stat(local_file_path).st_mtime)
            filetime = time.strftime('%Y-%m-%d %H:%M:%S', filemtime)

            yield [filerootdir, dirfile, fb, filetime, dirs]

    def init(self):
        for item in self.__traverse_file():
            self.__mkdirs(item[4])
            self.__upload(item[1], item[2], item[0], '初始化')
        self.__timewrite()
        print "{0}初始化成功,已上传{1}文件".format(self.project_name, self.total_upload_files)

    def update(self):
        total_update_file = 0
        recode_time = open(
            'runtime/{0}'.format(self.project_conf_name)).readline()

        need_update_files = [item[0] for item in self.__traverse_file() if item[
            3] > recode_time]

        print "\n需要更新的文件有:"
        for file in need_update_files:
            print file

        start = raw_input("\n如果你确定更新以上文件,请输入y:\n")
        if start == "y":
            for item in self.__traverse_file():
                if item[3] > recode_time:
                    self.__cwd_dir(item[4])
                    self.__upload(item[1], item[2], item[0], '更新')
                    total_update_file += 1
            self.__timewrite()
            print "\n本次总共更新{0}个文件\n".format(total_update_file)
        else:
            print "退出本次更新\n"
            sys.exit(1)
