CREATE DATABASE  IF NOT EXISTS `databaseproject` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `databaseproject`;
-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: databaseproject
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `application`
--

DROP TABLE IF EXISTS `application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `application` (
  `ApplicationID` int NOT NULL AUTO_INCREMENT,
  `RequestID` int DEFAULT NULL,
  `ContractorID` int DEFAULT NULL,
  `ProposedPrice` int NOT NULL,
  `Comment` text NOT NULL,
  `ApplicationDate` timestamp NOT NULL,
  PRIMARY KEY (`ApplicationID`),
  KEY `App_SRID` (`RequestID`),
  KEY `App_ConID` (`ContractorID`),
  CONSTRAINT `App_ConID` FOREIGN KEY (`ContractorID`) REFERENCES `contractor` (`ContractorID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `App_SRID` FOREIGN KEY (`RequestID`) REFERENCES `servicerequest` (`RequestID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `application`
--

LOCK TABLES `application` WRITE;
/*!40000 ALTER TABLE `application` DISABLE KEYS */;
INSERT INTO `application` VALUES (1,3,1,10,'I can sew the hole back on easily.','2026-04-23 06:44:52'),(3,1,1,15,'I can patch up that hole for you!','2026-04-23 11:54:09'),(5,2,2,10,'I could work on this poncho for you!','2026-04-23 12:17:57'),(7,5,1,20,'I can totally help you resize that T-Shirt','2026-05-03 01:33:41'),(8,5,1,20,'I can totally help you resize that T-Shirt','2026-05-03 02:01:07'),(9,7,1,20,'I will make some interesting shoelaces for you!','2026-05-03 02:55:48'),(10,9,2,7,'I can very easily alter your tie for you.','2026-05-03 06:53:34'),(11,8,1,25,'I have many years of experience tailoring shirts, I will do a good job for you.','2026-05-03 07:09:41'),(12,8,3,15,'I\'m confident I can do a good job.','2026-05-03 07:20:18'),(13,8,2,9,'I may not have a lot of experience, but I\'ll do it for a cheap price!','2026-05-03 07:22:39'),(14,10,2,15,'I can do it! You can count on me!','2026-05-03 07:27:53'),(17,11,1,20,'I have lots of expererience with trousers, I can do this!','2026-05-03 08:39:04');
/*!40000 ALTER TABLE `application` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contractor`
--

DROP TABLE IF EXISTS `contractor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contractor` (
  `ContractorID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `PhoneNum` char(10) NOT NULL,
  PRIMARY KEY (`ContractorID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contractor`
--

LOCK TABLES `contractor` WRITE;
/*!40000 ALTER TABLE `contractor` DISABLE KEYS */;
INSERT INTO `contractor` VALUES (1,'John Tailor','js65914@georgiasouthern.edu','5557771980'),(2,'Tas Man','taskmancsci3432@gmail.com','4443332211'),(3,'Jacob Schmidt','schmidtjacob920@gmail.com','9127591863');
/*!40000 ALTER TABLE `contractor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `CustomerID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `PhoneNum` char(10) NOT NULL,
  PRIMARY KEY (`CustomerID`),
  UNIQUE KEY `Email_UNIQUE` (`Email`),
  UNIQUE KEY `PhoneNum_UNIQUE` (`PhoneNum`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'Jacob Schmidt','schmidtjacob920@gmail.com','9127591863'),(3,'Robert Sewman','taskmancsci3432@gmail.com','1234567890'),(4,'Weitian Tong','wtong@georgiasouthern.edu','9124788752');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job`
--

DROP TABLE IF EXISTS `job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job` (
  `JobID` int NOT NULL AUTO_INCREMENT,
  `RequestID` int DEFAULT NULL,
  `ContractorID` int DEFAULT NULL,
  `ApplicationID` int DEFAULT NULL,
  `StartDate` date NOT NULL,
  `FinishDate` date NOT NULL,
  `Status` varchar(30) NOT NULL,
  PRIMARY KEY (`JobID`),
  KEY `Job_AppID` (`ApplicationID`),
  KEY `App_SRID` (`RequestID`),
  KEY `App_ConID` (`ContractorID`),
  CONSTRAINT `Job_AppID` FOREIGN KEY (`ApplicationID`) REFERENCES `application` (`ApplicationID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Job_ConID` FOREIGN KEY (`ContractorID`) REFERENCES `contractor` (`ContractorID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Job_SRID` FOREIGN KEY (`RequestID`) REFERENCES `servicerequest` (`RequestID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job`
--

LOCK TABLES `job` WRITE;
/*!40000 ALTER TABLE `job` DISABLE KEYS */;
INSERT INTO `job` VALUES (1,3,1,1,'2026-04-23','2026-04-30','finished'),(2,1,1,3,'2026-04-23','2026-04-30','finished'),(4,2,2,5,'2026-05-02','2026-05-09','in progress'),(5,9,2,10,'2026-05-03','2026-05-09','in progress'),(6,10,2,14,'2026-05-03','2026-05-09','finished'),(7,11,1,17,'2026-05-03','2026-05-16','finished');
/*!40000 ALTER TABLE `job` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `review` (
  `ReviewID` int NOT NULL AUTO_INCREMENT,
  `JobID` int DEFAULT NULL,
  `ReviewRating` int NOT NULL,
  `ReviewComment` text NOT NULL,
  `ReviewDate` date NOT NULL,
  PRIMARY KEY (`ReviewID`),
  KEY `Review_JobID` (`JobID`),
  CONSTRAINT `Review_JobID` FOREIGN KEY (`JobID`) REFERENCES `job` (`JobID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
INSERT INTO `review` VALUES (1,1,4,'Very quick service','2026-04-23'),(2,2,4,'Amazing job!','2026-05-02'),(3,6,4,'Very good job','2026-05-03');
/*!40000 ALTER TABLE `review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicerequest`
--

DROP TABLE IF EXISTS `servicerequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicerequest` (
  `RequestID` int NOT NULL AUTO_INCREMENT,
  `CustomerID` int DEFAULT NULL,
  `Status` varchar(30) DEFAULT NULL,
  `Description` text NOT NULL,
  `ClothingType` varchar(50) NOT NULL,
  PRIMARY KEY (`RequestID`),
  KEY `SR_CustomerID` (`CustomerID`),
  CONSTRAINT `SR_CustomerID` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicerequest`
--

LOCK TABLES `servicerequest` WRITE;
/*!40000 ALTER TABLE `servicerequest` DISABLE KEYS */;
INSERT INTO `servicerequest` VALUES (1,1,'unstarted','The knee on my jeans has ripped. Need to get it patched.','Jeans'),(2,1,'unstarted','Alas, my pncho has a hole in it. My only souvenir from my last vacation! Would love to have it repaired.','Poncho'),(3,1,'unstarted','The button on my dress shirt popped out! Need it sewn back on.','Dress Shirt'),(4,1,'unstarted','I\'d like some back pockets added to my trousers','Trousers'),(5,1,'unstarted','I need my band tee to be sized down, the arms are too big','T Shirt'),(6,1,'unstarted','I need my t shirt sleeves resized, they are too small on me','T Shirt'),(7,1,'unstarted','I would like someone to make some custom shoelaces for me!','Shoes'),(8,4,'unstarted','I would like for my dress shirt to be tailored to my measurements.','Dress Shirt'),(9,4,'unstarted','I would like my tie slimmed','Neck Tie'),(10,4,'unstarted','I need my suit jacket tailored to fit me.','Suit Jacket'),(11,4,'unstarted','I need my trousers to be hemmed.','Trousers');
/*!40000 ALTER TABLE `servicerequest` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-03 13:32:40
