-- MySQL dump 10.13  Distrib 8.0.27, for Linux (x86_64)
--
-- Host: 10.12.21.200    Database: uos-sysmig
-- ------------------------------------------------------
-- Server version	8.0.27

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
-- Table structure for table `agent_info`
--

DROP TABLE IF EXISTS `agent_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `agent_info` (
  `agent_id` int NOT NULL AUTO_INCREMENT,
  `agent_ip` varchar(256) NOT NULL,
  `agent_username` varchar(256) NOT NULL,
  `agent_passwd` varbinary(256) NOT NULL,
  `hostname` varchar(256) DEFAULT NULL,
  `agent_os` varchar(256) DEFAULT NULL,
  `agent_arch` varchar(45) DEFAULT NULL,
  `agent_storage` int DEFAULT NULL,
  `agent_kernel` varchar(45) DEFAULT NULL,
  `agent_repo_kernel` varchar(256) DEFAULT NULL,
  `agent_migration_os` varchar(256) DEFAULT NULL,
  `agent_history_faild_reason` varchar(45) DEFAULT NULL,
  `agent_online_status` int DEFAULT '0',
  `repo_status` int DEFAULT NULL,
  PRIMARY KEY (`agent_id`),
  KEY `agent_ip` (`agent_ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agent_info`
--

LOCK TABLES `agent_info` WRITE;
/*!40000 ALTER TABLE `agent_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `agent_info` ENABLE KEYS */;
UNLOCK TABLES;