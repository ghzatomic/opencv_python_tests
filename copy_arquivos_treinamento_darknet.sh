#/bin/sh

cd content/darknet/
mkdir -p ./obj/
mkdir -p backup
wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137
cp ../../roboflow.zip ./ 
unzip roboflow.zip 
rm roboflow.zip
rm ../../roboflow.zip
cp train/_darknet.labels data/obj.names
mkdir data/obj

rm -rf train/*
rm -rf valid/*
rm -rf data/obj/*

cp train/*.jpg data/obj/
cp valid/*.jpg data/obj/

cp train/*.txt data/obj/
cp valid/*.txt data/obj/