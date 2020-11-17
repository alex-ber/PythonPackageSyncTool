FROM alexberkovich/alpine-anaconda3:0.0.5

COPY requirements.txt etc/requirements.txt
COPY requirements-tests.txt etc/requirements-tests.txt

RUN set -ex && \
    #latest pip,setuptools,wheel
    pip install --upgrade pip==20.2.4 setuptools==50.3.2 wheel==0.35.1 && \
    pip install -r etc/requirements.txt  && \
    pip install -r etc/requirements-tests.txt

#CMD ["/bin/sh"]
CMD tail -f /dev/null

#docker rmi -f reqsync-i
#docker rm -f reqsync
##docker build --squash . -t reqsync-i
#docker build . -t reqsync-i
#docker exec -it $(docker ps -q -n=1) bash
#docker tag utils-i alexberkovich/python_package_sync_tool:0.6.1
#docker push alexberkovich/python_package_sync_tool:0.6.1
# EOF
