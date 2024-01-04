nohup python ./src/datahelper.py > ./log/downloads.log 2>&1 &
tail -f ./log/downloads.log
