DATE=`date +%F_%T`
STATUS=`cd /home/instafame/instafameapp && git status -s`

if [[ -z "${STATUS}" ]]; then
        echo "$DATE Repo is up to date, nothing to do here."
else
        echo "$DATE Repo is out of sync, updating now"
        /bin/bash /home/instafame/instafameapp/scripts/cron/git_autocommit.sh
fi
