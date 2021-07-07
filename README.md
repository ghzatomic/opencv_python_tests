sudo apt install python3-opencv libopencv-dev

mkdir content
cd content
git clone https://github.com/roboflow-ai/darknet.git

./copy_arquivos_treinamento_darknet.sh

python darknet_generate_config.py

./exec_treinamento_darknet.sh

