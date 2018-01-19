#_*_coding:utf-8_*_
''''' 
Created on 2017-10-19 
 
@author: Administrator 
'''  
import time,datetime
import os
import redis  
from multiprocessing import Pool


def Storage(msg,rhost):
    pl=redis.ConnectionPool(host=rhost,port=6379,db=0)  
    r_conn = redis.StrictRedis(connection_pool=pl)
    while True:  
        #获取对了信息
        task = r_conn.brpop('tq', 0)
        MQStr =  task[1];
        #打印进程处理和当前队列数量
        print '%s:%d'%(msg,r_conn.llen('tq')) 
        #将队列列表化进行数据处理
        List = MQStr.split(' ')  
        DirID = List[0]
        #生产文件路径
        Now = datetime.datetime.now()
        Filepath = './%s/%s.log'%(DirID,Now.strftime("%Y-%m-%d-%p"))
        if not os.path.exists(DirID):
            os.makedirs(DirID)
        #文件内容处理
        Contents = MQStr.replace(List[0],'').strip()
        #a以追加模式打开。若文件存在，则会追加到文件的末尾；若文件不存在，则新建文件。该模式不能使用read*()方法
        f = open(Filepath,'a')
        f.write(Contents)
        f.close()
        #print Contents,Filename
        #time.sleep(0.01);  

if __name__ == '__main__':
    #redis 服务器地址
    redis_host = '127.0.0.1'
    #进程定义 根据日志的量级自行调试
    pro_num = 20
    p = Pool(processes=pro_num)
    for i in range(1,pro_num):
         msg = 'Thread%d:'%i
         p.apply_async(Storage,args=(msg,redis_host,))
    p.close()
    p.join()