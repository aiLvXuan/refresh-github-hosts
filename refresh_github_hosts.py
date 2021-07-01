#!/usr/bin/env python3
from __future__ import print_function
from urllib.request import urlopen
import os
import ctypes, sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# Create by LvXuan
class refesh_github_hosts:

    def get_hosts(self) -> str:
        url = 'https://raw.fastgit.org/521xueweihan/GitHub520/main/hosts'
        try:
            response = urlopen(url)
            return response.read().decode('utf-8')
        except BaseException:
            print('无法访问：' + url)
            url = 'https://github.com/521xueweihan/GitHub520/blob/main/hosts'
            try:
                print('正在请求：' + url)
                response = urlopen(url)
                return response.read().decode('utf-8')
            except BaseException:
                print('无法访问：' + url)
                return ''

    def input_hosts_path(self) -> str:
        host_path = os.path.join('C:/Windows/System32/drivers/etc/hosts')
        while not os.path.exists(host_path):
            host_path = os.path.join(input('请输入Hosts文件路径：').replace('\\', '/'))
        return host_path

    def get_loc_hosts_file(self, path) -> str:
        host = open(path, 'r', encoding='utf-8')
        hosts_str = ''
        for line in host:
            hosts_str += line
        host.close()
        return hosts_str.strip()

    def version_check(self, loc_hosts: str, github_hosts) -> bool:
        start = False
        loc_update_time = ''
        remote_update_time = ''
        for line in loc_hosts.splitlines():
            if line.find('# GitHub520 Host Start') != -1:
                start = True
            if start and line.find('# Update time:') != -1:
                index = line.find(':')
                loc_update_time = line[index + 1:].strip()
                break
        if loc_update_time == '':
            return True

        start = False
        for line in github_hosts.splitlines():
            if line.find('# GitHub520 Host Start') != -1:
                start = True
            if start and line.find('# Update time:') != -1:
                index = line.find(':')
                remote_update_time = line[index + 1:].strip()
                break
        if remote_update_time == '':
            return True
        print('Update time:', remote_update_time)
        return remote_update_time > loc_update_time

    def handler(self, loc_hosts: str, github_hosts: str) -> str:
        if github_hosts == '':
            print('没有获取到 GitHub hosts !')
            return loc_hosts
        github_hosts += '\n\n'
        star_index = loc_hosts.find('# GitHub520 Host Start')
        end_index = loc_hosts.find('# GitHub520 Host End') + 20
        if star_index >= 0 and end_index >= 0:
            loc_hosts = loc_hosts[:star_index] + github_hosts + loc_hosts[end_index:]
        else:
            loc_hosts += '\n\n\n' + github_hosts
        return loc_hosts

    def refresh_dns(self):
        os.system('ipconfig /flushdns')

    def did_modify(self):
        hosts_path = self.input_hosts_path()
        loc_hosts = self.get_loc_hosts_file(hosts_path)
        github_hosts = self.get_hosts()
        if github_hosts == '':
            input('请检查网络连接！')
            exit(-1)

        if not self.version_check(loc_hosts, github_hosts):
            input("已是最新！")
            return

        if not is_admin():
            print("请使用管理员权限")
            if sys.version_info[0] == 3:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            else:  # in python2.x
                ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)
            exit(-1)
        result = self.handler(loc_hosts, github_hosts)
        with open(hosts_path, 'w') as file:
            file.write(result)
        print('写入完成，如没有修改请检查杀毒软件')
        self.refresh_dns()
        key = input("回车退出程序：")


if __name__ == '__main__':
    refesh_github_hosts().did_modify()
