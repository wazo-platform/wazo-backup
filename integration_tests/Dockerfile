FROM xivo/xivo-backup

WORKDIR /usr/src/xivo-backup/bin
RUN for bin in $(ls .) ; do \
        ln -sf $PWD/$bin /usr/sbin/$bin ; \
    done
