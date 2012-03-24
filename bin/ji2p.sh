#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "usage: $0 <java package>"
    echo "sample: $0 sun.net.www.protocol.http"
    echo "gives sun/net/www/protocol/http"
    exit -1
fi

INP=$1

echo $INP | sed 's:\.:/:g'