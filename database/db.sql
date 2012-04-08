DROP TABLE IF EXISTS nairaland;
CREATE DATABASE nairaland;
USE nairaland;

CREATE TABLE `students` (
`id` INTEGER NOT NULL AUTO_INCREMENT ,
`student name` VARCHAR(50) NOT NULL ,
`age` INTEGER NOT NULL,
`sex` VARCHAR(10) NOT NULL ,
`registration number` VARCHAR(14) NOT NULL ,
`pin` VARCHAR(4) NOT NULL ,
PRIMARY KEY (`id`)
) COMMENT 'this table contains the vital information of candidates.';

CREATE TABLE `subjects` (
`id` INTEGER NOT NULL AUTO_INCREMENT ,
`id_students` INTEGER NOT NULL ,
`subject 1` VARCHAR(32) NOT NULL ,
`subject 2` VARCHAR(32) NOT NULL ,
`subject 3` VARCHAR(32) NOT NULL ,
`subject 4` VARCHAR(32) NOT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (id_students) REFERENCES `students` (`id`)
) COMMENT 'This contains the 4 subjects taken by the jamb candidate.';

CREATE TABLE `scores` (
`id` INTEGER NOT NULL AUTO_INCREMENT ,
`id_students` INTEGER NOT NULL ,
`subject 1 score` INTEGER NOT NULL ,
`subject 2 score` INTEGER NOT NULL ,
`subject 3 score` INTEGER NOT NULL ,
`subject 4 score` INTEGER NOT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (id_students) REFERENCES `students` (`id`)
) COMMENT 'this is the candidate scores';


