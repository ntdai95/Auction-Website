
# Backup
echo "docker exec <CONTAINER> /usr/bin/mysqldump -u <MYSQL USER> --password=<MYSQL password> <DATABASE> > <BACKUP.sql>"
echo $#
if [ $# -eq 5 ]; then
    docker exec $1 /usr/bin/mysqldump -u $2 --password=$3 $4 > $5
fi
# Restore
# cat backup.sql | docker exec -i CONTAINER /usr/bin/mysql -u root --password=root DATABASE