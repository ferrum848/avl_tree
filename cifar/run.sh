docker build -t cifar .

docker  run --rm -it \
			-v /home/alex/work2/ml/cifar:/work \
			-v /home/alex/pycharm:/pycharm \
			-e DISPLAY=$DISPLAY \
    		-v /tmp/.X11-unix:/tmp/.X11-unix \
    		-v ~/.Xauthority:/root/.Xauthority \
		--entrypoint="" \
    		--shm-size='1G' \
    		-e PYTHONUNBUFFERED='1' \
                --net=host \
			cifar bash
