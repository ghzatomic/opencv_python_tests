cd content/darknet
./darknet detector train data/obj.data cfg/custom-yolov4-detector.cfg yolov4.conv.137 -dont_show -map
#./darknet detector train data/obj.data cfg/custom-yolov4-detector.cfg yolov4-tiny.conv.29 -dont_show -map