echo 'drop database social_event_db;' | mysql -u root --password=password
echo 'create database social_event_db;' | mysql -u root --password=password
mysql < social_event_db.sql -u root --password=password
