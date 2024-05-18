#!/usr/bin/bash

# get all keys
# find the type for each key
# get value(s) for key
# list, string, hash, set

for each in $( redis-cli KEYS \* ); do
  result=$(redis-cli type $each)
  value=""
  if [ $result == "list" ]
  then
    value=$(redis-cli lrange $each 0 -1)
  elif [ $result == "string" ]
  then
    value=$(redis-cli get $each)
  elif [ $result == "hash" ]
  then
    value=$(redis-cli hgetall $each)
  elif [ $result == "set" ]
  then
    value=$(redis-cli smembers $each)
  fi
  printf "key %s\t\t type %s\t\t value %s.\n" $each $result $value
done
