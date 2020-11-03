#!/bin/bash
ulimit -c unlimited
for ((;;))
do
    SEEDFILE=`ls cstrike/maps | shuf -n 1`
    NOW=`date +%T | sed 's/:/-/g'`
    FILENAME=`cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1`
    cat cstrike/maps/$SEEDFILE | zzuf -s=$RANDOM -r=0.05 -b12- > cstrike/maps/$FILENAME.bsp && chmod 0775 cstrike/maps/$FILENAME.bsp
    zzuf --max-crashes=1 --max-memory=-1 --quiet --max-usertime=15 --signal --ratio=0 ./hl2_linux -novid -console '+sv_pure -1' +map $FILENAME
    if [ -e core ]
        then
            echo "Core dumped, renaming to core.$RANDOM.$FILENAME.$NOW and saving $FILENAME.bsp"
            cp core corefiles/core.$RANDOM.$FILENAME.$NOW
            rm core
            cp cstrike/maps/$FILENAME.bsp crashes
        else
            echo "Hang/SIGKILL/successful run. (mut. $SEEDFILE)"

    fi
done
