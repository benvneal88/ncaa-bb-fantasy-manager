CREATE TABLE IF NOT EXISTS `tbl_game` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `event_date` date DEFAULT NULL,
  `event_start` datetime DEFAULT NULL,
  `event_end` datetime DEFAULT NULL,
  `tournament_round` int DEFAULT NULL,
  `fk_ball_team_id_home` int DEFAULT NULL,
  `fk_ball_team_id_away` int DEFAULT NULL,
  `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_ball_team_home_idx` (`fk_ball_team_id_home`),
  KEY `fk_ball_team_away_idx` (`fk_ball_team_id_away`),
  CONSTRAINT `fk_ball_team_away` FOREIGN KEY (`fk_ball_team_id_away`) REFERENCES `tbl_ball_team` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_ball_team_home` FOREIGN KEY (`fk_ball_team_id_home`) REFERENCES `tbl_ball_team` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
