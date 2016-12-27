#!/usr/bin/env bash

LOGS=$(mktemp)
nosetests --with-coverage --cover-package=tooldog 2> $LOGS
cat $LOGS
grep TOTAL $LOGS | awk '{ print "TOTAL: "$4; }'
rm $LOGS
