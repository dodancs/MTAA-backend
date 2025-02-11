DROP TABLE IF EXISTS `mtaa`.`cats`;
CREATE TABLE `mtaa`.`cats` (
  `id` SERIAL NOT NULL,
  `uuid` VARCHAR(36) NOT NULL,
  `name` VARCHAR(256) NOT NULL,
  `age` SMALLINT NOT NULL,
  `sex` BOOLEAN NOT NULL,
  `breed` bigint(20) NOT NULL REFERENCES breeds(id) ON DELETE RESTRICT,
  `health_status` bigint(20) NOT NULL REFERENCES health_status(id) ON DELETE RESTRICT,
  `castrated` BOOLEAN NOT NULL,
  `vaccinated` BOOLEAN NOT NULL,
  `dewormed` BOOLEAN NOT NULL,
  `colour` bigint(20) NOT NULL REFERENCES colour(id) ON DELETE RESTRICT,
  `description` LONGTEXT NOT NULL,
  `health_log` LONGTEXT DEFAULT NULL,
  `adoptive` BOOLEAN NOT NULL DEFAULT TRUE,
  `adopted_by` VARCHAR(36) NULL DEFAULT NULL REFERENCES users(uuid) ON DELETE CASCADE,
  `pictures` LONGTEXT NOT NULL DEFAULT '[]',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE `cats_uuid` (`uuid`),
  INDEX `cats_name` (`name`),
  INDEX `cats_age` (`age`),
  INDEX `cats_sex` (`sex`),
  INDEX `cats_breed` (`breed`),
  INDEX `cats_health_status` (`health_status`),
  INDEX `cats_castrated` (`castrated`),
  INDEX `cats_vaccinated` (`vaccinated`),
  INDEX `cats_dewormed` (`dewormed`),
  INDEX `cats_colour` (`colour`),
  INDEX `cats_adoptive` (`adoptive`)
);