DROP TABLE IF EXISTS `mtaa`.`activations`;
CREATE TABLE `mtaa`.`activations` (
  `id` SERIAL NOT NULL,
  `user` VARCHAR(36) NOT NULL REFERENCES users(uuid) ON DELETE CASCADE,
  `seed` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`)
);