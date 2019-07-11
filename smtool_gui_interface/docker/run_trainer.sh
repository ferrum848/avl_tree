docker run --rm -it \
			--net=host \
			-v `pwd`/../src:/src \
			--entrypoint="" \
			-v $PYCHARM_ROOT:/pycharm \
			-e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v ~/.Xauthority:/root/.Xauthority \
			-v /home/ds/soft/pycharm-community-2019.1.2:/pycharm \
    		-v /home/ds/pycharm-settings/smtool_gui:/root/.PyCharmCE2019.1 \
    		-v /home/ds/pycharm-settings/smtool_gui__idea:/workdir/.idea \
    		-v `pwd`/../../encnet_research/data:/data_encnet \
    		-v `pwd`/../../smtool_research/data:/data_smtool \
			docker.deepsystems.io/smtool_gui bash