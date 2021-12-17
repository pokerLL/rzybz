#!/usr/bin/env bash

# 转移到其他目录需要修改文件夹
dir="/home/ubuntu/rzybz"

# 一键启动或者重启的脚本

cd $dir

echo "停止旧服务"
# 停止旧服务
uwsgi --stop uwsgi.pid

# 短暂延迟，否则启动失败
sleep 1

# 启动新服务
uwsgi --ini uwsgi.ini
echo "启动服务成功"


