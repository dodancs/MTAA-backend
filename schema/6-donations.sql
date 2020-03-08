DROP TABLE IF EXISTS `mtaa`.`donations`;
CREATE TABLE `mtaa`.`donations` (
  `id` SERIAL NOT NULL,
  `donator` VARCHAR(36) NULL DEFAULT NULL REFERENCES users(uuid) ON DELETE RESTRICT,
  `amount` DOUBLE(5, 2) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE `donations_donator` (`donator`)
);