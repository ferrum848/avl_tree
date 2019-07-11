docker run --rm -it \
			--net=host \
			-v `pwd`/../src:/src \
			-v $PYCHARM_ROOT:/pycharm \
			-e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v ~/.Xauthority:/root/.Xauthority \
			-v /home/ds/soft/pycharm:/pycharm \
    		-v /home/ds/pycharm-settings/smtool_gui:/root/.PyCharmCE2018.2 \
    		-v /home/ds/pycharm-settings/smtool_gui__idea:/workdir/.idea \
    		-v `pwd`/../../smtool_research/data:/data \
			interactive-segmentation-gui bash