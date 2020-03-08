DROP TABLE IF EXISTS `mtaa`.`colours`;
CREATE TABLE `mtaa`.`colours` (
  `id` SERIAL NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE `colours_name` (`name`)
);