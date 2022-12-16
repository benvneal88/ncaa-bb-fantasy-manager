CREATE TABLE `fantasy_mgr`.`tbl_box_score_line_item` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `fk_game_id` INT NOT NULL,
  `fk_player_id` INT NOT NULL,
  `points` INT NOT NULL,
  `created_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_game_idx` (`fk_game_id` ASC) VISIBLE,
  INDEX `fk_player_idx` (`fk_player_id` ASC) VISIBLE,
  CONSTRAINT `fk_game`
    FOREIGN KEY (`fk_game_id`)
    REFERENCES `fantasy_mgr`.`tbl_game` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_player`
    FOREIGN KEY (`fk_player_id`)
    REFERENCES `fantasy_mgr`.`tbl_player` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION);
