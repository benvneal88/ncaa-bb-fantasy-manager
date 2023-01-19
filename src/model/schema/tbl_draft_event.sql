CREATE TABLE IF NOT EXISTS `tbl_draft_event` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `fk_fantasy_team_id` INT NOT NULL,
  `fk_player_id` INT NOT NULL,
  `created_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_fantasy_team_id_idx` (`fk_fantasy_team_id` ASC) VISIBLE,
  INDEX `fk_player_id_idx` (`fk_player_id` ASC) VISIBLE,
  CONSTRAINT `fk_fantasy_team_id`
    FOREIGN KEY (`fk_fantasy_team_id`)
    REFERENCES `tbl_fantasy_team` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_player_id`
    FOREIGN KEY (`fk_player_id`)
    REFERENCES `tbl_player` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION);
