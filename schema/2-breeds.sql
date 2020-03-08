DROP TABLE IF EXISTS `mtaa`.`breeds`;
CREATE TABLE `mtaa`.`breeds` (
  `id` SERIAL NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE `breeds_name` (`name`)
);