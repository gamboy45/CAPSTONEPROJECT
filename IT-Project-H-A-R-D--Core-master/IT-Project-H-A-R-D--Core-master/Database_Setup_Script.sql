-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`FamilyMember`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`FamilyMember` (
  `FamilyMemberID` INT NOT NULL AUTO_INCREMENT,
  `Firstname` VARCHAR(45) NULL,
  `Lastname` VARCHAR(45) NULL,
  `MaidenName` VARCHAR(45) NULL,
  `DODYear` INT NULL,
  `DODMonth` INT NULL,
  `DODDay` INT NULL,
  `DOBYear` INT NULL,
  `DOBMonth` INT NULL,
  `DOBDay` INT NULL,
  `gender` ENUM('m','f') NULL,
  `userProfilePic` BLOB NULL,
  `AccuracyDOD` ENUM('documented', 'accurate', 'likely') NULL,
  `AccuracyDOB` ENUM('documented', 'likely', 'accurate') NULL,
  PRIMARY KEY (`FamilyMemberID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Artifact`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Artifact` (
  `ArtifactID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(999) NULL,
  `Geotag` VARCHAR(45) NULL,
  `Tags` LONGTEXT NULL,
  `DateAddedYear` INT NULL,
  `DateAddedMonth` INT NULL,
  `DateAddedDay` INT NULL,
  `DateAcquireYear` INT NULL,
  `DateAcquireMonth` INT NULL,
  `DateAcquireDay` INT NULL,
  `AccuracyAcquire` ENUM('documented', 'accurate', 'likely') NULL,
  `description` LONGTEXT NULL,
  `Heir` INT NULL,
  `CurrentOwner` INT NOT NULL,
  `Type` ENUM('physical', 'letter', 'postcard', 'photo') NOT NULL,
  PRIMARY KEY (`ArtifactID`),
  INDEX `fk_Artifact_User1_idx` (`Heir` ASC),
  INDEX `fk_Artifact_User2_idx` (`CurrentOwner` ASC),
  CONSTRAINT `fk_Artifact_User1`
    FOREIGN KEY (`Heir`)
    REFERENCES `mydb`.`FamilyMember` (`FamilyMemberID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Artifact_User2`
    FOREIGN KEY (`CurrentOwner`)
    REFERENCES `mydb`.`FamilyMember` (`FamilyMemberID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ArtifactImage`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ArtifactImage` (
  `ArtifactImageID` INT NOT NULL AUTO_INCREMENT,
  `Image` BLOB NOT NULL,
  `Caption` LONGTEXT NULL,
  `Artifact_ArtifactID` INT NOT NULL,
  PRIMARY KEY (`ArtifactImageID`),
  INDEX `fk_ArtifcatImage_Artifact1_idx` (`Artifact_ArtifactID` ASC),
  CONSTRAINT `fk_ArtifcatImage_Artifact1`
    FOREIGN KEY (`Artifact_ArtifactID`)
    REFERENCES `mydb`.`Artifact` (`ArtifactID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`PhysicalObjects`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`PhysicalObjects` (
  `ObjectID` INT NOT NULL AUTO_INCREMENT,
  `Type` ENUM('bigobject', 'smallobject', 'document', 'artwork', 'miscellanious') NOT NULL,
  `SpecialAttributes` LONGTEXT NULL,
  `Artifact_ArtifactID` INT NOT NULL,
  PRIMARY KEY (`ObjectID`, `Artifact_ArtifactID`),
  INDEX `fk_PhysicalObjects_Artifact1_idx` (`Artifact_ArtifactID` ASC),
  CONSTRAINT `fk_PhysicalObjects_Artifact1`
    FOREIGN KEY (`Artifact_ArtifactID`)
    REFERENCES `mydb`.`Artifact` (`ArtifactID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Photo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Photo` (
  `PhotoID` INT NOT NULL AUTO_INCREMENT,
  `Postmark` VARCHAR(45) BINARY NULL,
  `Artifact_ArtifactID` INT NOT NULL,
  PRIMARY KEY (`PhotoID`, `Artifact_ArtifactID`),
  INDEX `fk_Photo_Artifact1_idx` (`Artifact_ArtifactID` ASC),
  CONSTRAINT `fk_Photo_Artifact1`
    FOREIGN KEY (`Artifact_ArtifactID`)
    REFERENCES `mydb`.`Artifact` (`ArtifactID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`PostCard`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`PostCard` (
  `PostCardID` INT NOT NULL AUTO_INCREMENT,
  `SenderAddress` VARCHAR(100) NULL,
  `ReceiverAddress` VARCHAR(100) NULL,
  `Sender` VARCHAR(45) NULL,
  `Receiver` VARCHAR(45) NULL,
  `CoverPicture` BLOB NULL,
  `Artifact_ArtifactID` INT NOT NULL,
  PRIMARY KEY (`PostCardID`, `Artifact_ArtifactID`),
  INDEX `fk_PostCard_Artifact1_idx` (`Artifact_ArtifactID` ASC),
  CONSTRAINT `fk_PostCard_Artifact1`
    FOREIGN KEY (`Artifact_ArtifactID`)
    REFERENCES `mydb`.`Artifact` (`ArtifactID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Letter`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Letter` (
  `LetterID` INT NOT NULL AUTO_INCREMENT,
  `Aerogramme` TINYINT(1) NOT NULL,
  `Telegram` TINYINT(1) NOT NULL,
  `SenderAddress` VARCHAR(100) NULL,
  `ReceiverAddress` VARCHAR(100) NULL,
  `Sender` VARCHAR(45) NULL,
  `Receiver` VARCHAR(45) NULL,
  `Envelope` BLOB NULL,
  `Artifact_ArtifactID` INT NOT NULL,
  PRIMARY KEY (`LetterID`, `Artifact_ArtifactID`),
  INDEX `fk_Letter_Artifact1_idx` (`Artifact_ArtifactID` ASC),
  CONSTRAINT `fk_Letter_Artifact1`
    FOREIGN KEY (`Artifact_ArtifactID`)
    REFERENCES `mydb`.`Artifact` (`ArtifactID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Comment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Comment` (
  `CommentID` INT NOT NULL AUTO_INCREMENT,
  `Comment` LONGTEXT NULL,
  `Artifact_ArtifactID` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`CommentID`),
  INDEX `fk_Comment_Artifact1_idx` (`Artifact_ArtifactID` ASC),
  CONSTRAINT `fk_Comment_Artifact1`
    FOREIGN KEY (`Artifact_ArtifactID`)
    REFERENCES `mydb`.`Artifact` (`ArtifactID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Relationship`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Relationship` (
  `RelationshipID` INT NOT NULL AUTO_INCREMENT,
  `Individual1` INT NOT NULL,
  `Individual2` INT NOT NULL,
  `RelationshipType` ENUM('child', 'parent', 'spouse', 'grandchild', 'brother', 'sister', 'cousin', 'uncle', 'aunt') NOT NULL,
  PRIMARY KEY (`RelationshipID`),
  INDEX `fk_Relationship_User1_idx` (`Individual1` ASC),
  INDEX `fk_Relationship_User2_idx` (`Individual2` ASC),
  CONSTRAINT `fk_Relationship_User1`
    FOREIGN KEY (`Individual1`)
    REFERENCES `mydb`.`FamilyMember` (`FamilyMemberID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Relationship_User2`
    FOREIGN KEY (`Individual2`)
    REFERENCES `mydb`.`FamilyMember` (`FamilyMemberID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Entity`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Entity` (
  `EntityID` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  `type` VARCHAR(45) NULL,
  `tag` VARCHAR(45) NULL,
  `Artifact_ArtifactID` INT NOT NULL,
  PRIMARY KEY (`EntityID`),
  INDEX `fk_Entity_Artifact1_idx` (`Artifact_ArtifactID` ASC),
  CONSTRAINT `fk_Entity_Artifact1`
    FOREIGN KEY (`Artifact_ArtifactID`)
    REFERENCES `mydb`.`Artifact` (`ArtifactID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Entity_has_FamilyMember`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Entity_has_FamilyMember` (
  `Entity_EntityID` INT NULL,
  `FamilyMember_FamilyMemberID` INT NULL,
  PRIMARY KEY (`Entity_EntityID`, `FamilyMember_FamilyMemberID`),
  INDEX `fk_Entity_has_FamilyMember_FamilyMember1_idx` (`FamilyMember_FamilyMemberID` ASC),
  INDEX `fk_Entity_has_FamilyMember_Entity1_idx` (`Entity_EntityID` ASC),
  CONSTRAINT `fk_Entity_has_FamilyMember_Entity1`
    FOREIGN KEY (`Entity_EntityID`)
    REFERENCES `mydb`.`Entity` (`EntityID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Entity_has_FamilyMember_FamilyMember1`
    FOREIGN KEY (`FamilyMember_FamilyMemberID`)
    REFERENCES `mydb`.`FamilyMember` (`FamilyMemberID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
