CREATE TABLE `fantasy_mgr`.`tbl_player` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(80) NOT NULL,
  `last_name` VARCHAR(80) NOT NULL,
  `career_ppg` DECIMAL(2,2) NOT NULL,
  `fK_ball_team_id` INT NULL,
  `fk_fantasy_team_id` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_ball_team_idx` (`fK_ball_team_id` ASC) VISIBLE,
  INDEX `fk_fantasy_team_idx` (`fk_fantasy_team_id` ASC) VISIBLE,
  CONSTRAINT `fk_ball_team`
    FOREIGN KEY (`fK_ball_team_id`)
    REFERENCES `fantasy_mgr`.`tbl_ball_team` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_fantasy_team`
    FOREIGN KEY (`fk_fantasy_team_id`)
    REFERENCES `fantasy_mgr`.`tbl_fantasy_team` (`id`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION);
