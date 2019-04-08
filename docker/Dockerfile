FROM alpine:3.6

ARG DOWNLOAD_PACKAGES="bash python3 py-pip"
ARG PY_LIBRARIES="python-gitlab click click_help_colors"

ARG PGCLI_USER=pgcli
ARG PGCLI_GROUP=pgcli
ARG PGCLI_UID=65530
ARG PGCLI_GID=65530
ARG PGCLI_PATH="/opt/pgcli"

# Resolve dependencies
RUN apk update && \
    apk add ${DOWNLOAD_PACKAGES} && \
    pip3 install --upgrade ${PY_LIBRARIES}

# Copy needed files
RUN mkdir -p $PGCLI_PATH
COPY functions/ $PGCLI_PATH/functions
COPY main.py $PGCLI_PATH/main.py 
RUN chown -R $PGCLI_UID:$PGCLI_GID $PGCLI_PATH && \
    ln -s $PGCLI_PATH/main.py /usr/bin/pgcli

# Delete __pycache__ in case it exists
RUN rm -rf $PGCLI_PATH/functions/__pycache__

RUN addgroup -g ${PGCLI_GID} ${PGCLI_GROUP} \
 && adduser -D -h "${PGCLI_PATH}" -u ${PGCLI_UID} -G ${PGCLI_GROUP} -s /bin/bash ${PGCLI_USER}

USER $PGCLI_USER

ENTRYPOINT ["pgcli"]
