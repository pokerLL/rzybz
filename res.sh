#!/bin/bash

echo "尝试重新加载静态文件"

echo "yes" | python3 manage.py collectstatic

echo "尝试重启uwsgi服务"

./bootstart.sh
