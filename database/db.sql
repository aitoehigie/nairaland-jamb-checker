CREATE TABLE `students` (
`id` INTEGER NOT NULL AUTO_INCREMENT ,
`student name` VARCHAR(100) NOT NULL ,
`age` INTEGER NOT NULL DEFAULT 16 ,
`sex` VARCHAR NOT NULL ,
`registration number` VARCHAR(14) NOT NULL ,
`pin` VARCHAR(4) NOT NULL ,
PRIMARY KEY (`id`)
) COMMENT 'this table contains the vital information of candidates.';


