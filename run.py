#/usr/bin/env python
# coding:utf-8

from FtpControl.FtpControl import FtpControl
import datetime
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def man():
    runtime = os.path.exists('runtime')
    remote_project_name = os.path.exists('remote_project_name')
    if not runtime and not remote_project_name:
        os.makedirs('runtime')
        os.makedirs('remote_project_name')

    try:
        project_conf_name = sys.argv[1]
    except:
        print "请输入项目配置文件名称:"
        sys.exit(1)
    try:
        valve = sys.argv[2]
    except:
        valve = ''

    ftp = FtpControl(project_conf_name)

    if not os.path.isfile('runtime/{0}'.format(project_conf_name)):
        with open('runtime/{0}'.format(project_conf_name), 'w+') as f:
            line = datetime.datetime.now() - datetime.timedelta(seconds=120)
            f.write(str(line))

    if valve == "init":
        ftp.init()
    else:
        ftp.update()


if __name__ == "__main__":
    man()
