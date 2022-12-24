CREATE TABLE `fantasy_mgr`.`tbl_fantasy_team_user_mtm` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `fk_fantasy_team_id` INT NULL,
  `fk_user_id` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_fantasy_team_id_idx` (`fk_fantasy_team_id` ASC) VISIBLE,
  INDEX `fk_user_id_idx` (`fk_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_mtm_fantasy_team_id`
    FOREIGN KEY (`fk_fantasy_team_id`)
    REFERENCES `fantasy_mgr`.`tbl_fantasy_team` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_mtm_user_id`
    FOREIGN KEY (`fk_user_id`)
    REFERENCES `fantasy_mgr`.`tbl_user` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION);
