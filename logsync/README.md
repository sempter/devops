项目说明
	本项目利用redis 的队列对日志文件进行批量同步处理
	Logfiles => Clients =》 Redis_MQ => Server => Files
	Clients负责使用多线程监听日志更新和生产队列
	Server负责使用多进程监听队列更新和将队列同步写入到本地
部署说明
	1、Redis安装（略）
	2、使用python2.6x 2.7x 运行
	3、安装python  redis 模块建议使用pip install reids