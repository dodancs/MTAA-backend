DROP TABLE IF EXISTS `mtaa`.`users`;
CREATE TABLE `mtaa`.`users` (
  `id` SERIAL NOT NULL,
  `uuid` VARCHAR(36) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `firstname` VARCHAR(255) NOT NULL,
  `lastname` VARCHAR(255) NOT NULL,
  `activated` BOOLEAN NOT NULL DEFAULT FALSE,
  `admin` BOOLEAN NOT NULL DEFAULT FALSE,
  `donations` DOUBLE(5, 2) NOT NULL DEFAULT '0',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE `users_uuid` (`uuid`),
  UNIQUE `users_email` (`email`)
);