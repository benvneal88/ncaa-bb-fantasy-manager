create user svc_app_user;
create database ncaa_fantasy DEFAULT CHARACTER SET utf8;
create database staging DEFAULT CHARACTER SET utf8;
GRANT ALL PRIVILEGES ON ncaa_fantasy.* TO 'svc_app_user'@'%';
GRANT ALL PRIVILEGES ON staging.* TO 'svc_app_user'@'%';