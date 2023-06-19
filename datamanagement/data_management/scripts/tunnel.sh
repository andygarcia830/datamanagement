#!/bin/bash
SSH_HOST=$1
SSH_PORT=$2
SSH_LOGIN=$3
LOCAL_PORT=$4
DESTINATION_HOST=$5
DESTINATION_PORT=$6
PEM_FILE=$7
COMMAND="/usr/bin/ssh -N -f -L $LOCAL_PORT:$DESTINATION_HOST:$DESTINATION_PORT $SSH_HOST -p $SSH_PORT -l $SSH_LOGIN -i $PEM_FILE"
COMMAND2=$8
APP_STAT=`ps -efa --cols 1024 | grep -v "grep" | grep "$COMMAND" | awk '{print $2;}'`
if [ "$APP_STAT" == "" ]
then
  if [ "$COMMAND2" == "stop" ]
  then
    echo "Tunnel $COMMAND not running."
    exit
  fi
  echo $COMMAND
  exec $COMMAND
exit
fi

if [ "$COMMAND2" == "stop" ]
  then
     kill -9 $APP_STAT
     echo "Stopped tunnel $COMMAND"
     exit
fi
echo "Tunnel $COMMAND is currently running."
exit
