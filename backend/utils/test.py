#!/bin/bash

id=$1
echo $id
cp -r site-10 site-$id
cd site-$id
sed -i "s/10/$id/" *