


CREATE TABLE `students` (
`id` INTEGER NOT NULL AUTO_INCREMENT ,
`student name` VARCHAR(100) NOT NULL ,
`age` INTEGER NOT NULL DEFAULT 16 ,
`sex` VARCHAR NOT NULL ,
`registration number` VARCHAR(14) NOT NULL ,
`pin` VARCHAR(4) NOT NULL ,
PRIMARY KEY (`id`)
) COMMENT 'this table contains the vital information of candidates.';

CREATE TABLE `subjects` (
`id` INTEGER NOT NULL AUTO_INCREMENT ,
`student_id` INTEGER NOT NULL ,
`subject 1` VARCHAR(32) NOT NULL ,
`subject 2` VARCHAR(32) NOT NULL ,
`subject 3` VARCHAR(32) NOT NULL ,
`subject 4` VARCHAR(32) NOT NULL ,
PRIMARY KEY (`id`)
) COMMENT 'This contains the 4 subjects taken by the jamb candidate.';

