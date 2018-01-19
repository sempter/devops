#_*_coding:utf-8_*_
import os,time
import redis  
import threading

def Tail(ID,path,redis):
        f = open(path, 'r')
        record_inode = os.stat(path).st_ino  #inode number
        f.seek(0,2) #跳到文件追后开始同步
        while True:
        #line = f.readline()
        line = f.read(10000) #每次读取10000字节
        if line: #判断文件是否存在更新
            redis.lpush('tq', '%s %s'%(ID,line)) #添加队列
        else:#如果文件没有更新，作以下处理（考虑到日志会切割，滚动）
            if os.path.exists(path): ### File exists 
                if record_inode != os.stat(path).st_ino:
                    print '%s File Change'%ID
                    record_inode = os.stat(path).st_ino  # record new inode number
                    f.close() ## close file 
                    f = open(path, 'r')
                    f.seek(0,0)
                    print 'Open File %s Change'%ID
                else:
                    pass
            else:
                pass
        time.sleep(0.1)
        f.close()

def main():
    pool=redis.ConnectionPool(host='127.0.0.1',port=6379,db=0) #Redis 队列服务器配置
    conn_redis = redis.StrictRedis(connection_pool=pool)
    filelist = [
        {'ID':'175wechat','logpath':'/data/logs/anjubao_wechat/debug.log'},
        {'ID':'175zhengjiaAlipay','logpath':'/data/logs/anjubao_zhengjiaAlipay/debug.log'},
    ]
    ###初始化同步线程，针对每个文件启动一个线程
    threads = []
    for th in range(len(filelist)):
        th = threading.Thread(target=Tail, name=filelist[th]['ID'], args=(filelist[th]['ID'],filelist[th]['logpath'],conn_redis)) 
        threads.append(th)
    print 'Init threads!'
    for t in threads:
        t.start()
    print 'Start threads!'
    for j in threads:
        j.join()
    print 'Join threads!'

if __name__ == '__main__':
    main()
    print 'Done'