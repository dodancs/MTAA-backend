DROP TABLE IF EXISTS `mtaa`.`favourites`;
CREATE TABLE `mtaa`.`favourites` (
  `id` SERIAL NOT NULL,
  `user` VARCHAR(36) NOT NULL REFERENCES users(uuid) ON DELETE CASCADE,
  `cat` VARCHAR(36) NOT NULL REFERENCES cats(uuid) ON DELETE CASCADE,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `favourites_user` (`user`)
);