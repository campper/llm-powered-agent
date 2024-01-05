nohup python ./src/datahelper.py > ./logs/downloads.log 2>&1 &
tail -f ./logs/downloads.log
