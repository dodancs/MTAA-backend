DROP TABLE IF EXISTS `mtaa`.`comments`;
CREATE TABLE `mtaa`.`comments` (
  `id` SERIAL NOT NULL,
  `uuid` VARCHAR(36) NOT NULL,
  `author` VARCHAR(36) NOT NULL REFERENCES users(uuid) ON DELETE CASCADE,
  `cat` VARCHAR(36) NOT NULL REFERENCES cats(uuid) ON DELETE CASCADE,
  `text` LONGTEXT NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE `favourites_uuid` (`uuid`),
  UNIQUE `favourites_cat` (`cat`)
);