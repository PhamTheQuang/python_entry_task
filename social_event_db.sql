CREATE TABLE IF NOT EXISTS `social_event_db`.`admin_tab` (
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`username` VARCHAR(128) NOT NULL,
	`salt` VARCHAR(32) NOT NULL,
	`password_digest` VARCHAR(128) NOT NULL,
	`token` VARCHAR(32) NULL,
	`token_expire_time` INT UNSIGNED NULL,
	PRIMARY KEY (`id`),
	UNIQUE INDEX idx_username (`username`),
	INDEX idx_token (`token`)
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `social_event_db`.`user_tab` (
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`username` VARCHAR(128) NOT NULL,
	`salt` VARCHAR(32) NOT NULL,
	`password_digest` VARCHAR(60) NOT NULL,
	`full_name` VARCHAR(128) NULL,
	`token` VARCHAR(32) NULL,
	`portrait` VARCHAR(2086) NULL,
	`token_expire_time` INT UNSIGNED NULL,
	PRIMARY KEY (`id`),
	UNIQUE INDEX idx_username (`username`),
	INDEX idx_token (`token`)
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `social_event_db`.`event_tab` (
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`title` VARCHAR(128) NOT NULL,
	`description` TEXT NOT NULL,
	`start_time` INT UNSIGNED NOT NULL,
	`end_time` INT UNSIGNED NOT NULL,
	`channel_id` BIGINT UNSIGNED NOT NULL,
	`total_comments` BIGINT UNSIGNED NOT NULL DEFAULT 0,
	`total_likes` BIGINT UNSIGNED NOT NULL DEFAULT 0,
	`total_participants` BIGINT UNSIGNED NOT NULL DEFAULT 0,
	`location` VARCHAR(128) NOT NULL,
	`address` VARCHAR(128) NOT NULL,
	`lon` FLOAT NOT NULL,
	`lat` FLOAT NOT NULL,
	`main_pictures` VARCHAR(2086) NOT NULL DEFAULT "",
	`create_time` INT UNSIGNED NOT NULL,
	PRIMARY KEY (`id`),
	INDEX idx_channel_id (`create_time`, `channel_id`),
	INDEX idx_period (`create_time`, `start_time`, `end_time`),
	INDEX idx_channel_id_period (`create_time`, `channel_id`, `start_time`, `end_time`)
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `social_event_db`.`picture_tab` (
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`event_id` BIGINT UNSIGNED NOT NULL,
	`path` VARCHAR(2086) NOT NULL,
	PRIMARY KEY (`id`),
	INDEX idx_event_id (`event_id`)
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `social_event_db`.`channel_tab` (
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(128) NOT NULL,
	PRIMARY KEY (`id`)
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `social_event_db`.`comment_tab` (
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`content` TEXT NOT NULL,
	`user_id` BIGINT UNSIGNED NOT NULL,
	`event_id` BIGINT UNSIGNED NOT NULL,
	`reply_comment_id` BIGINT UNSIGNED NULL,
	`create_time` INT UNSIGNED NOT NULL,
	PRIMARY KEY (`id`),
	INDEX idx_event_id (`event_id`)
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `social_event_db`.`like_tab` (
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`user_id` BIGINT UNSIGNED NOT NULL,
	`event_id` BIGINT UNSIGNED NOT NULL,
	`create_time` INT UNSIGNED NOT NULL,
	PRIMARY KEY (`id`),
	INDEX idx_event_id_user_id (`event_id`, `user_id`)
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `social_event_db`.`participant_tab` (
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`user_id` BIGINT UNSIGNED NOT NULL,
	`event_id` BIGINT UNSIGNED NOT NULL,
	`create_time` INT UNSIGNED NOT NULL,
	PRIMARY KEY (`id`),
	INDEX idx_event_id_user_id (`event_id`, `user_id`)
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;
