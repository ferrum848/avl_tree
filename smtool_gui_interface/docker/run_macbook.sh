docker run --rm -it \
			--net=host \
			-v `pwd`/../src:/src \
			--entrypoint="" \
			-v $PYCHARM_ROOT:/pycharm \
			-e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v ~/.Xauthority:/root/.Xauthority \
			-v /home/alex/pycharm:/pycharm \
    		-v /home/alex/pycharm-settings/import/pascal_voc:/root/.PyCharmCE2018.1 \
    -v /home/alex/pycharm-settings/import__idea:/workdir/.idea \
			smtool_gui bash
