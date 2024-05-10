# HostScan
一个简单的host碰撞辅助测试脚本
```
> python .\hostscan.py -h
usage: hostscan.py [-h] [-I IPFILE] [-D HOSTFILE]

host碰撞辅助测试脚本

options:
  -h, --help            show this help message and exit
  -I IPFILE, --ipfile IPFILE
                        保存ip列表的文件
  -D HOSTFILE, --hostfile HOSTFILE
                        保存host列表的文件
```

准备一个IP列表，一个Host列表，然后运行下列命令,结果保存在`/result/<ip>.txt`中

```
> python .\hostscan.py -I .\ips.txt -D .\hosts.txt                 
```
