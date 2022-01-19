
# # Backup
# docker exec CONTAINER /usr/bin/mysqldump -u root --password=root DATABASE > backup.sql

# Restore
echo "cat <BACKUP.sql> | docker exec -i <CONTAINER> /usr/bin/mysql -u <MYSQL USER> --password=<MYSQL PASSWORD> <DATABASE>"
if [ "$#" -eq 5 ]; then
    cat $1 | docker exec -i $2 /usr/bin/mysql -u $3 --password=$4 $5;
fi