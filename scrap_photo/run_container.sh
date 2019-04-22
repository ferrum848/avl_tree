docker build -t scrap_foto .

docker  run --rm -it \
			-v /home/alex/work2/scrap_foto:/work \
			-v /home/alex/pycharm:/pycharm \
			-e DISPLAY=$DISPLAY \
    		-v /tmp/.X11-unix:/tmp/.X11-unix \
    		-v ~/.Xauthority:/root/.Xauthority \
		--entrypoint="" \
    		--shm-size='1G' \
    		-e PYTHONUNBUFFERED='1' \
                --net=host \
			scrap_foto bash
