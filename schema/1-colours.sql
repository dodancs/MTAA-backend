DROP TABLE IF EXISTS `mtaa`.`colours`;
CREATE TABLE `mtaa`.`colours` (
  `id` SERIAL NOT NULL,
  `name` VARCHAR(256) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE `colours_name` (`name`)
);