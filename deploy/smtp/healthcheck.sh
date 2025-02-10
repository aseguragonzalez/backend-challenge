#!/bin/bash

curl -s -o /dev/null -w "%{http_code}" http://localhost:80 | grep -q "200"
status=$?

if [ $status -eq 0 ]; then
  exit 0
else
  exit 1
fi
