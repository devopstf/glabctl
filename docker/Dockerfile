FROM alpine:3.6

ARG DOWNLOAD_PACKAGES="bash python3 py-pip"
ARG PY_LIBRARIES="python-gitlab click click_help_colors"

ARG GLABCTL_USER=glabctl
ARG GLABCTL_GROUP=glabctl
ARG GLABCTL_UID=65530
ARG GLABCTL_GID=65530
ARG GLABCTL_PATH="/opt/glabctl"

# Resolve dependencies
RUN apk update && \
    apk add ${DOWNLOAD_PACKAGES} && \
    pip3 install --upgrade ${PY_LIBRARIES}

# Copy needed files
RUN mkdir -p $GLABCTL_PATH
COPY functions/ $GLABCTL_PATH/functions
COPY main.py $GLABCTL_PATH/main.py 
RUN chown -R $GLABCTL_UID:$GLABCTL_GID $GLABCTL_PATH && \
    ln -s $GLABCTL_PATH/main.py /usr/bin/glabctl

# Delete __pycache__ in case it exists
RUN rm -rf $GLABCTL_PATH/functions/__pycache__

RUN addgroup -g ${GLABCTL_GID} ${GLABCTL_GROUP} \
 && adduser -D -h "${GLABCTL_PATH}" -u ${GLABCTL_UID} -G ${GLABCTL_GROUP} -s /bin/bash ${GLABCTL_USER}

USER $GLABCTL_USER

ENTRYPOINT ["glabctl"]
