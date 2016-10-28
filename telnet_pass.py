# -*- coding: utf-8 -*-

import telnetlib
import time
from multiprocessing.dummy import Pool as ThreadPool

# 弱口令字典
user_pwd = [
    ["root", "root"],
    ["admin", "admin"]
]
# result = open('result_linux.txt', 'a+')
result = open('result_win.txt', 'a+')


def check_pass(ip_po):
    tem = ip_po.strip('\n').split(' ')
    host = tem[0]
    port = tem[1]
    # print 'testing ' + host + ' on ' + port,
    try:
        tn = telnetlib.Telnet(host, port=port, timeout=10)
        # tn.set_debuglevel(2)
        tn.read_until("login", timeout=10)
        tn.write(user.encode('ascii') + "\r\n".encode('ascii'))
        tn.read_until("word", timeout=10)
        tn.write(pwd.encode('ascii') + "\r\n".encode('ascii'))
        time.sleep(.5)
        r = tn.read_very_eager()
        # print r

        # Linux
        # if '~$' in r or '~#' in r:
        # print host + ' on ' + port + ' with ' + user + ' and ' + pwd + ' success!!!'
        # result.write(host + '\t' + port + '\t' + user + '\t' + pwd + '\n')
        # else:
        # pass
        # print 'failed'

        # Windows
        if 'Failed' in r or 'not allowed' in r:
            pass
        # print 'failed'
        else:
            print 'success!!!'
            result.write(host + '\t' + port + '\t' + user + '\t' + pwd + '\n')
        tn.close()
    except:
        pass
        # print 'timeout'


for i in user_pwd:
    user = i[0]
    pwd = i[1]
    print 'Testing ' + user + ' and ' + pwd
    # host_port = open('linux.txt', 'r')
    host_port = open('win.txt', 'r')
    ip_po = []
    done = True
    while done:
        # 多行多行处理
        for j in range(50):
            temp = host_port.readline()
            # print temp
            if temp != '':
                ip_po.append(temp)
            else:
                done = False
                break
        print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        print "Testing", len(ip_po), "IP:", ip_po
        # print len(ip_po)

        # 非多进程
        # for k in ip_po:
        #     check_pass(k)

        pool = ThreadPool(50)
        results = pool.map(check_pass, ip_po)
        pool.close()
        pool.join()
        ip_po = []
    host_port.close()
result.close()
print 'finish!!!'
