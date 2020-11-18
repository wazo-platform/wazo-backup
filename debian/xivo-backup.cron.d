PATH=/usr/sbin

1 0 * * *   root       xivo-backup data /var/backups/xivo/data && xivo-backup db /var/backups/xivo/db
