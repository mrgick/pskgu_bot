#!/bin/sh

EXPORT=./export.sh
SETTINGS_CFG=./settings.cfg

if [ ! -f $EXPORT ]; then
    echo -e "'$EXPORT' not fount!">&2
    exit 1
fi

if [ -f $SETTINGS_CFG ]; then
    source $EXPORT
    source $SETTINGS_CFG
else
    echo -e "'$SETTINGS_CFG' not found!\n" \
            "\tPlease, see '$EXPORT' and define your own settings!">&2
    exit 1
fi

export LAUNCH_SH="$0"

if [ ! -f $LOGFILE ]; then
    mkdir -p $(dirname $LOGFILE)
    touch $LOGFILE
fi

if [ -f $MAIN_PY ]; then
    $PYTHON_EXEC $MAIN_PY $LAUNCH_OPTS $@
else
    echo -e "'$MAIN_PY' not found to launch!">&2
    exit 1
fi

