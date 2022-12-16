CREATE TABLE `fantasy_mgr`.`tbl_fantasy_team` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(80) NOT NULL,
  `display_name` VARCHAR(45) NULL,
  `draft_order` INT NULL,
  `fk_user_id` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE,
  INDEX `fk_user_id_idx` (`fk_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_user_id`
    FOREIGN KEY (`fk_user_id`)
    REFERENCES `fantasy_mgr`.`tbl_user` (`id`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION);
