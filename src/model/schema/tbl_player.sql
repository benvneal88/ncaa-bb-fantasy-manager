CREATE TABLE IF NOT EXISTS `tbl_player` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(80) NOT NULL,
  `last_name` varchar(80) NOT NULL,
  `ppg` decimal(4,2) DEFAULT NULL,
  `fk_ball_team_id` int DEFAULT NULL,
  `fk_fantasy_team_id` int DEFAULT NULL,
  `drafted_round` int DEFAULT NULL,
  `drafted_number` int DEFAULT NULL,
  `drafted_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_fantasy_team_idx` (`fk_fantasy_team_id`),
  KEY `fk_ball_team_id_idx` (`fk_ball_team_id`),
  CONSTRAINT `fk_ball_team_id` FOREIGN KEY (`fk_ball_team_id`) REFERENCES `tbl_ball_team` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_fantasy_team` FOREIGN KEY (`fk_fantasy_team_id`) REFERENCES `tbl_fantasy_team` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb3;
