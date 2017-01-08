#! /bin/bash

# Author: Jian Wang
# Date: 2017-1-7
# Email: wj_hust08@hust.edu.cn

cmd=${1}
id=$RANDOM$RANDOM
cache="/var/cache/jntask"

if [ ! -f ${cache}/running_tasks/${id} ]; then
   while [[ $(ls ${cache}/running_tasks | wc -l) -ge 8 ]]; do
      echo hi
      sleep 1
   done
   touch ${cache}/running_tasks/${id}
   ${cmd}
   #rm ${cache}/running_tasks/${id}
fi
