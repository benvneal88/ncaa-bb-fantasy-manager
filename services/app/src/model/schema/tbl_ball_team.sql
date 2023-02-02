CREATE TABLE IF NOT EXISTS `tbl_ball_team` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `name_short` VARCHAR(255) NOT NULL,
  `region` VARCHAR(45) NULL,
  `seed` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE);
