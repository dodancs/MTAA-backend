DROP TABLE IF EXISTS `mtaa`.`health_status`;
CREATE TABLE `mtaa`.`health_status` (
  `id` SERIAL NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE `health_status_name` (`name`)
);