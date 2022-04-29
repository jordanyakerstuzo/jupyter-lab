up:
	docker run -it \
		-p 8888:8888 \
		--mount type=bind,source=`pwd`/lib,target=/ext/lib \
		jupyter/pyspark-notebook