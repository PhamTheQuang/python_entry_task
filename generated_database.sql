BEGIN;
CREATE TABLE `admin_tab` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `username` varchar(128) NOT NULL,
    `salt` varchar(32) NOT NULL,
    `password_digest` varchar(128) NOT NULL,
    `token` varchar(32) NOT NULL,
    `token_expire_time` integer UNSIGNED
)
;
CREATE TABLE `user_tab` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `username` varchar(128) NOT NULL,
    `salt` varchar(32) NOT NULL,
    `password_digest` varchar(128) NOT NULL,
    `token` varchar(32) NOT NULL,
    `token_expire_time` integer UNSIGNED,
    `full_name` varchar(128) NOT NULL,
    `portrait` varchar(100) NOT NULL
)
;
CREATE TABLE `event_tab` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `title` varchar(128) NOT NULL,
    `description` longtext NOT NULL,
    `start_time` integer UNSIGNED NOT NULL,
    `end_time` integer UNSIGNED NOT NULL,
    `total_comments` bigint NOT NULL,
    `total_likes` bigint NOT NULL,
    `total_participants` bigint NOT NULL,
    `location` varchar(128) NOT NULL,
    `address` varchar(128) NOT NULL,
    `lon` double precision NOT NULL,
    `lat` double precision NOT NULL,
    `main_picture` varchar(100) NOT NULL,
    `create_time` integer UNSIGNED NOT NULL,
    `channel_id` integer NOT NULL
)
;
CREATE TABLE `channel_tab` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(128) NOT NULL
)
;
CREATE TABLE `picture_tab` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `image` varchar(100) NOT NULL,
    `event_id` integer NOT NULL
)
;
CREATE TABLE `comment_tab` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `content` longtext NOT NULL,
    `create_time` integer UNSIGNED NOT NULL,
    `event_id` integer NOT NULL,
    `user_id` integer NOT NULL,
    `reply_comment_id` integer
)
;
CREATE TABLE `like_tab` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `create_time` integer UNSIGNED NOT NULL,
    `event_id` integer NOT NULL,
    `user_id` integer NOT NULL,
    UNIQUE (`event_id`, `user_id`)
)
;
CREATE TABLE `participant_tab` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `create_time` integer UNSIGNED NOT NULL,
    `event_id` integer NOT NULL,
    `user_id` integer NOT NULL,
    UNIQUE (`event_id`, `user_id`)
)
;
CREATE INDEX `admin_tab_ee0cafa2` ON `admin_tab` (`username`);
CREATE INDEX `admin_tab_70c33c9f` ON `admin_tab` (`token`, `token_expire_time`);
CREATE INDEX `user_tab_ee0cafa2` ON `user_tab` (`username`);
CREATE INDEX `user_tab_70c33c9f` ON `user_tab` (`token`, `token_expire_time`);
CREATE INDEX `event_tab_9e85bf2d` ON `event_tab` (`channel_id`);
CREATE INDEX `event_tab_fcfb25b4` ON `event_tab` (`create_time`, `start_time`, `end_time`);
CREATE INDEX `event_tab_c64bee8f` ON `event_tab` (`create_time`, `end_time`);
CREATE INDEX `event_tab_5958a4fc` ON `event_tab` (`create_time`, `channel_id`, `start_time`, `end_time`);
CREATE INDEX `event_tab_60a6c68a` ON `event_tab` (`create_time`, `channel_id`, `end_time`);
CREATE INDEX `picture_tab_a41e20fe` ON `picture_tab` (`event_id`);
CREATE INDEX `comment_tab_a41e20fe` ON `comment_tab` (`event_id`);
CREATE INDEX `comment_tab_6340c63c` ON `comment_tab` (`user_id`);
CREATE INDEX `comment_tab_08318ab0` ON `comment_tab` (`reply_comment_id`);
CREATE INDEX `like_tab_a41e20fe` ON `like_tab` (`event_id`);
CREATE INDEX `like_tab_6340c63c` ON `like_tab` (`user_id`);
CREATE INDEX `participant_tab_a41e20fe` ON `participant_tab` (`event_id`);
CREATE INDEX `participant_tab_6340c63c` ON `participant_tab` (`user_id`);

COMMIT;
