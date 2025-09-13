/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.13-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: qr_alco
-- ------------------------------------------------------
-- Server version	10.11.13-MariaDB-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `choferes_prohibidos`
--

DROP TABLE IF EXISTS `choferes_prohibidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `choferes_prohibidos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `curp` varchar(18) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `empresa` varchar(100) NOT NULL,
  `observacion` text NOT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  `ine_foto` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `curp` (`curp`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `choferes_prohibidos`
--

LOCK TABLES `choferes_prohibidos` WRITE;
/*!40000 ALTER TABLE `choferes_prohibidos` DISABLE KEYS */;
INSERT INTO `choferes_prohibidos` VALUES
(1,'Majito Morales','MJM001','2000-06-08','ALCORH','Exceso de bullying a compañeros \"Denunciela si la ven\"','2025-08-22 21:34:35',NULL),
(2,'Emmanuel Salcido ','SAMJ002','2000-01-22','ALCOSISTEMAS','Se desmayo en sábado ','2025-08-23 13:22:34',NULL),
(4,'Jesus M','jfuiefew','2025-08-23','fewg','gweg','2025-08-23 13:47:44','firma_correos.jpg');
/*!40000 ALTER TABLE `choferes_prohibidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registros`
--

DROP TABLE IF EXISTS `registros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `registros` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `qr_id` varchar(10) DEFAULT NULL,
  `folio` varchar(50) DEFAULT NULL,
  `chofer` varchar(100) DEFAULT NULL,
  `licencia` varchar(50) DEFAULT NULL,
  `empresa` varchar(100) DEFAULT NULL,
  `tipo_carga` varchar(50) DEFAULT NULL,
  `estacion` varchar(50) DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  `activo` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registros`
--

LOCK TABLES `registros` WRITE;
/*!40000 ALTER TABLE `registros` DISABLE KEYS */;
INSERT INTO `registros` VALUES
(1,'12','3213','rwf','fwef','fewf','fwfw','caseta','2025-08-02 15:43:30',0),
(2,'13','gerg','gweg','gwg','gweg','gweg','wg','2025-08-02 15:50:53',0),
(3,'3','fef','gewg','gewg','wgwe','gweg','gwe','2025-08-02 16:20:28',0),
(4,'2','959','goku','uihiujijiokj9809','coca','melaza','caseta','2025-08-02 17:27:06',0),
(5,'23','fadecad-200','emmauel salcido','a23403-treff','alco','pc gamers','caseta','2025-08-02 17:34:01',0),
(6,'1','fadecad-300','yisus','jfdewifjowqie','fjweiofjweof','fewoifjweo','caseta','2025-08-05 17:08:17',0),
(7,'2','hrethrthr','hrthrth','htrhrth','alcodesa prueba','algo','caseta','2025-08-05 17:34:14',0),
(8,'6','6hrhrth','hshr','hrsh','hrhr','hrht','caseta','2025-08-06 18:38:50',0),
(9,'55','45yh','pepe','A','big cola','refreco ','caseta','2025-08-09 20:01:00',0),
(10,'7','5yh4hrt','herhrte','ehetrheh','ehhe','eheh','Caseta','2025-08-16 12:46:38',0),
(28,'QRN3','greg','greg','gerg','gerg','gerg','caseta','2025-08-16 14:52:57',0),
(29,'QRN3','gtrh','hrth','hhrth','hrth','hrth','caseta','2025-08-16 14:55:52',0),
(30,'QRN3','hj6y5tj','k687ik','k87k','k78k','k87k','caseta','2025-08-16 14:56:20',0),
(31,'QRN3','test 1','test 1','test 1','test 1','test 1','caseta','2025-08-16 15:04:32',0),
(32,'QRN1','regber','greg','regreg','rgreg','gerg','Caseta','2025-08-16 15:20:18',0),
(33,'QRN4','fadecad-500','Vegeta','A01-4545434-40','Famsa','Gold','caseta','2025-08-16 20:07:12',0),
(34,'QRN2','g56y','y45y','y54y','y45y','y54y4','caseta','2025-08-16 20:11:11',0),
(35,'QRN3','rw3gf','ergg','gerg','ger','ggreg','Caseta','2025-08-16 20:11:43',0),
(36,'QRN4','FEWFNEW','FNWEKJFN','FNWEKJFN','FKENFWEKJ','FEKNWFW','caseta','2025-08-22 15:32:06',1),
(37,'QRN1','001','REWR','EWT','TWT','TGWTG','caseta','2025-08-22 16:50:53',0),
(38,'QRN5','00','RAUL JUAREZ','12345678','FORAJES GUTIERREZ','SEMILLA DE ALGODON ','caseta','2025-08-22 16:53:54',1),
(39,'QRN20','gfcvgf','tygty','gygyu','yu7ghu','ghy7g','caseta','2025-08-22 21:46:00',1),
(40,'QRN19','001','EMMANUEL SALCIDO','AA01','FORD','TECLADOS','caseta','2025-08-22 22:24:32',1),
(41,'QRN17','001','Jesus Emm','AA02','FORD','mouse','Caseta','2025-08-23 17:24:49',1),
(42,'QRN13','005','YISUS M','AA03','SOPHOS','SO','Caseta','2025-08-27 13:52:55',1),
(43,'QRN11','002','gbregh','herh','herh','erherh','Bascula','2025-08-29 21:53:22',1);
/*!40000 ALTER TABLE `registros` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seguimiento`
--

DROP TABLE IF EXISTS `seguimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `seguimiento` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `qr_id` varchar(10) DEFAULT NULL,
  `registro_id` int(11) DEFAULT NULL,
  `estacion` varchar(100) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seguimiento`
--

LOCK TABLES `seguimiento` WRITE;
/*!40000 ALTER TABLE `seguimiento` DISABLE KEYS */;
INSERT INTO `seguimiento` VALUES
(1,'12',NULL,'bascula','2025-08-02 15:36:42'),
(2,'12',NULL,'mp','2025-08-02 15:44:52'),
(3,'12',NULL,'salida','2025-08-02 15:45:09'),
(4,'13',NULL,'mp','2025-08-02 15:51:15'),
(5,'13',NULL,'bascula','2025-08-02 15:51:25'),
(6,'13',NULL,'salida','2025-08-02 15:51:42'),
(7,'12',NULL,'salida','2025-08-02 16:20:05'),
(8,'3',NULL,'mp','2025-08-02 16:20:50'),
(9,'3',NULL,'mp','2025-08-02 17:27:36'),
(10,'23',NULL,'sistemas','2025-08-02 17:34:30'),
(11,'334',NULL,'434','2025-08-02 17:34:35'),
(12,'23',NULL,'comedor','2025-08-02 17:42:21'),
(13,'23',NULL,'bascula','2025-08-05 17:36:11'),
(14,'23',NULL,'salida','2025-08-05 17:36:42'),
(15,'6',NULL,'caseta','2025-08-06 18:39:17'),
(16,'1',NULL,'caseta','2025-08-06 20:09:32'),
(17,'1',NULL,'caseta','2025-08-06 20:09:37'),
(18,'1',NULL,'caseta','2025-08-06 20:10:09'),
(19,'1',NULL,'caseta','2025-08-06 20:10:15'),
(20,'1',NULL,'caseta','2025-08-06 20:11:07'),
(21,'1',NULL,'bascula','2025-08-06 20:11:57'),
(22,'1',NULL,'bascula','2025-08-06 20:12:05'),
(23,'1',NULL,'caseta','2025-08-06 20:13:34'),
(24,'1',NULL,'caseta','2025-08-06 20:13:40'),
(25,'1',NULL,'caseta','2025-08-06 20:14:37'),
(26,'1',NULL,'caseta','2025-08-06 20:14:44'),
(27,'1',NULL,'caseta','2025-08-09 14:03:47'),
(28,'1',NULL,'caseta','2025-08-09 14:03:52'),
(29,'1',NULL,'SALIDA','2025-08-09 14:31:22'),
(30,'2',NULL,'SALIDA','2025-08-09 19:59:07'),
(31,'3',NULL,'caseta','2025-08-09 19:59:41'),
(32,'55',NULL,'bascula','2025-08-09 20:02:40'),
(33,'55',NULL,'mp','2025-08-09 20:03:20'),
(34,'3',NULL,'SALIDA','2025-08-09 20:04:36'),
(35,'55',NULL,'SALIDA','2025-08-09 20:04:51'),
(36,'6',NULL,'caseta','2025-08-12 14:49:43'),
(37,'6',NULL,'bascula','2025-08-12 14:49:59'),
(38,'7',NULL,'Bascula','2025-08-16 12:55:34'),
(39,'7',NULL,'bascula','2025-08-16 12:56:07'),
(40,'QRN1',NULL,'SALIDA','2025-08-16 14:07:09'),
(41,'QRN2',NULL,'caseta','2025-08-16 14:12:46'),
(42,'QRN2',NULL,'SALIDA','2025-08-16 14:18:37'),
(43,'QRN3',NULL,'caseta','2025-08-16 14:40:40'),
(44,'QRN3',NULL,'SALIDA','2025-08-16 14:40:58'),
(45,'QRN3',NULL,'caseta','2025-08-16 14:55:52'),
(46,'QRN3',NULL,'SALIDA','2025-08-16 14:55:59'),
(47,'QRN3',NULL,'caseta','2025-08-16 14:56:20'),
(48,'QRN3',30,'SALIDA','2025-08-16 15:04:12'),
(49,'QRN3',29,'SALIDA','2025-08-16 15:04:13'),
(50,'QRN3',28,'SALIDA','2025-08-16 15:04:14'),
(51,'12',1,'SALIDA','2025-08-16 15:04:36'),
(52,'7',10,'SALIDA','2025-08-16 15:04:37'),
(53,'55',9,'SALIDA','2025-08-16 15:04:38'),
(54,'6',8,'SALIDA','2025-08-16 15:04:38'),
(55,'2',7,'SALIDA','2025-08-16 15:04:39'),
(56,'1',6,'SALIDA','2025-08-16 15:04:39'),
(57,'23',5,'SALIDA','2025-08-16 15:04:39'),
(58,'2',4,'SALIDA','2025-08-16 15:04:39'),
(59,'3',3,'SALIDA','2025-08-16 15:04:39'),
(60,'13',2,'SALIDA','2025-08-16 15:04:40'),
(61,'QRN3',31,'caseta','2025-08-16 15:04:47'),
(62,'QRN3',31,'Bascula','2025-08-16 15:05:45'),
(63,'QRN3',31,'SALIDA','2025-08-16 15:19:55'),
(64,'QRN1',32,'Patio','2025-08-16 15:20:27'),
(65,'QRN1',32,'Bascula','2025-08-16 15:20:32'),
(66,'QRN1',32,'bascula','2025-08-16 20:05:23'),
(67,'QRN1',32,'SALIDA','2025-08-16 20:05:48'),
(68,'QRN4',33,'bascula','2025-08-16 20:08:21'),
(69,'QRN4',33,'mp','2025-08-16 20:08:54'),
(70,'QRN4',33,'SALIDA','2025-08-16 20:09:30'),
(71,'QRN2',34,'Caseta','2025-08-16 20:11:26'),
(72,'QRN2',34,'Patio','2025-08-16 20:11:27'),
(73,'QRN2',34,'Bascula','2025-08-16 20:11:29'),
(74,'QRN4',36,'caseta','2025-08-22 15:32:15'),
(75,'QRN4',36,'bascula','2025-08-22 15:32:32'),
(76,'QRN4',36,'bascula','2025-08-22 16:40:31'),
(77,'QRN4',36,'bascula','2025-08-22 16:40:44'),
(78,'QRN2',34,'SALIDA','2025-08-22 16:47:23'),
(79,'QRN1',37,'SALIDA','2025-08-22 16:51:04'),
(80,'QRN19',40,'mp','2025-08-22 22:25:00'),
(81,'QRN19',40,'bascula','2025-08-22 22:25:51'),
(82,'qrn19',40,'Brazo','2025-08-22 22:26:47'),
(83,'QRN19',40,'Patio','2025-08-22 22:32:50'),
(84,'QRN3',35,'SALIDA','2025-08-23 17:12:13'),
(85,'QRN13',42,'Patio','2025-08-27 13:53:11'),
(86,'QRN13',42,'Bascula','2025-08-27 13:53:14'),
(87,'QRN17',41,'Patio','2025-08-29 21:53:01');
/*!40000 ALTER TABLE `seguimiento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `rol` varchar(20) NOT NULL,
  `estacion_asignada` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES
(6,'admin','admin123','admin',NULL),
(7,'caseta','caseta','normal','caseta'),
(9,'Bascula Principal','123','normal','bascula'),
(11,'mp','mp','normal','mp'),
(12,'Elisa','Karro$04812','supervisor',NULL),
(13,'BRAZO','123','normal','Brazo'),
(14,'caseta2','1','Encargado','Caseta'),
(15,'sadmin','123','supervisor',NULL);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-08  2:00:01
