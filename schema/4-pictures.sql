DROP TABLE IF EXISTS `mtaa`.`pictures`;
CREATE TABLE `mtaa`.`pictures` (
  `id` SERIAL NOT NULL,
  `uuid` VARCHAR(36) NOT NULL,
  `owner` VARCHAR(36) NOT NULL REFERENCES users(uuid) ON DELETE CASCADE,
  PRIMARY KEY (`id`),
  UNIQUE `pictures_uuid` (`uuid`)
);