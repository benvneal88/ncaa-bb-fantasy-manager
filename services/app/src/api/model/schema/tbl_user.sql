CREATE TABLE IF NOT EXISTS `tbl_user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(80) NULL,
  `last_name` VARCHAR(80) NULL,
  `user_name` VARCHAR(80) NULL,
  `email` VARCHAR(80) NOT NULL,
  `is_active` BIT(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `user_name_UNIQUE` (`user_name` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE);
