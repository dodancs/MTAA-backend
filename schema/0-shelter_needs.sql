DROP TABLE IF EXISTS `mtaa`.`shelter_needs`;
CREATE TABLE `mtaa`.`shelter_needs` (
  `id` SERIAL NOT NULL,
  `uuid` VARCHAR(36) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `details` LONGTEXT NOT NULL,
  `hide` BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (`id`),
  UNIQUE `shelter_needs_uuid` (`uuid`)
);