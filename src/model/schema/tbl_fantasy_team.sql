CREATE TABLE IF NOT EXISTS `tbl_fantasy_team` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(80) NOT NULL,
  `display_name` VARCHAR(45) NULL,
  `draft_order` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE);