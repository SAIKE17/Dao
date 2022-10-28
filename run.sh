#!/bin/sh

# sudo docker exec sign-python /bin/bash -c "cd /home/python/Dao && python run.py hifini"

# 执行命令
run(){
    echo "执行命令为: $*"
    sudo docker exec sign-python /bin/bash -c "cd /home/python/Dao && $*"
}

manual(){
    echo '选择签到网站 1、mteam 2、pttime 3、lemon 4、hdtime 5、btschool 6、hifini 7、smzdm '
    # shellcheck disable=SC2162
    read type
    if [ "$type" == 1 ]
    then
        web='mteam'
    elif [ "$type" == 2 ]
    then
        web='pttime'
    elif [ "$type" == 3 ]
    then
        web='lemon'
    elif [ "$type" == 4 ]
    then
        web='hdtime'
    elif [ "$type" == 5 ]
    then
        web='btschool'
    elif [ "$type" == 6 ]
    then
        web='hifini'
    elif [ "$type" == 7 ]
    then
        web='smzdm'
    else
        exit 1
    fi
    run "python run.py $web"
}

if [ x"$1" = x ]; then # 未带参数，进行手动选择
    manual
else # 带参数执行
    run $*
fi