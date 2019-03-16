FROM alpine:3.6

ARG DOWNLOAD_PACKAGES="bash python3 py-pip"
ARG PY_LIBRARIES="python-gitlab click click_help_colors"

# Resolve dependencies
RUN apk update && \
    apk add ${DOWNLOAD_PACKAGES} && \
    pip3 install --upgrade ${PY_LIBRARIES}

# Copy needed files
RUN mkdir -p /opt/pgcli
COPY functions/ /opt/pgcli/functions
COPY main.py /opt/pgcli/main.py

# Delete __pycache__ in case it exists
RUN rm -rf /opt/pgcli/functions/__pycache__

ENTRYPOINT ["/opt/pgcli/main.py"]
