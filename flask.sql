-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 25, 2023 at 10:31 AM
-- Server version: 8.0.31
-- PHP Version: 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `flask`
--

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
CREATE TABLE IF NOT EXISTS `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `category_name`, `created_at`, `status`) VALUES
(1, 'Videos', '2023-03-25 05:20:46', 1),
(2, 'Exam Papers', '2023-03-25 05:20:54', 1),
(3, 'Books', '2023-03-25 05:21:00', 1),
(4, 'Notes', '2023-03-25 05:57:30', 1);

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
CREATE TABLE IF NOT EXISTS `courses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`id`, `course_name`, `created_at`, `status`) VALUES
(1, 'Mechanical Engineering', '2023-03-25 05:21:10', 1),
(2, 'Computer Engineering', '2023-03-25 05:21:19', 1),
(3, 'Information Technology', '2023-03-25 05:21:28', 1),
(4, 'Civil Engineering', '2023-03-25 07:59:06', 1);

-- --------------------------------------------------------

--
-- Table structure for table `materials`
--

DROP TABLE IF EXISTS `materials`;
CREATE TABLE IF NOT EXISTS `materials` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `type` tinyint(1) NOT NULL DEFAULT '1',
  `ext` varchar(10) DEFAULT NULL,
  `pickup` text,
  `category_id` int NOT NULL,
  `course_id` int NOT NULL,
  `user_id` int NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `fk_category` (`category_id`),
  KEY `fk_course` (`course_id`),
  KEY `fk_user` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `materials`
--

INSERT INTO `materials` (`id`, `title`, `description`, `type`, `ext`, `pickup`, `category_id`, `course_id`, `user_id`, `created_at`, `status`) VALUES
(11, 'Basic Of Operating System', 'pdf of Basic of Operating system by Carriage Margs', 1, 'pdf', '', 3, 2, 11, '2023-03-25 06:53:24', 1),
(2, 'Programming in C', 'Programming in C by E Balagurusamy', 2, '', 'Student of 6th sem of Computer Dept. (GIA) of BBIT college is having book of \r\nProgramming in C  by E Balagurusamy Edition : 2016, those who want can meet him in regular college hours in room no 210.', 3, 2, 11, '2023-03-25 06:25:57', 1),
(12, 'Relational Database Management System', 'Relational Database Management System Old Paper...', 1, 'pdf', '', 2, 2, 11, '2023-03-25 07:17:02', 1),
(8, ' Scripting Language - Python (Course Code- 43307010)', 'Course Title: Scripting Language - Python\r\n(Course Code: 4330701)\r\nDetailed Syllabus', 1, 'pdf', '', 4, 2, 11, '2023-03-25 06:38:33', 1),
(10, 'Last 4 years Mechanical Dept Paper', 'Last 4 years Mechanical Dept Paper of Thermodynamics (1213321) :)', 1, 'pdf', '', 2, 1, 11, '2023-03-25 06:47:07', 1),
(13, 'Basics of Operating System', 'Detailed syllabus of basic operating system ', 1, 'pdf', '', 4, 2, 11, '2023-03-25 07:22:03', 1),
(16, 'Data Structures and Algorithms', 'Course Code: 4330704\r\nName: Data Structure and Algorithms ', 2, '', 'Course Code: 4330704', 4, 3, 11, '2023-03-25 07:37:55', 0),
(15, 'Database Management System', 'Exam Paper of Database Management System ', 1, 'pdf', '', 2, 3, 11, '2023-03-25 07:32:55', 1),
(17, 'Basics of Operating System', 'Exam Paper of Operating System\r\ncourse code:3330701', 2, '', 'DIPLOMA ENGINEERING – SEMESTER – III • EXAMINATION – SUMMER 16', 4, 3, 11, '2023-03-25 07:45:43', 1),
(18, 'Project Report', 'Cab Management System Using Python\r\n#file handling #python', 1, 'pdf', '', 4, 3, 11, '2023-03-25 07:53:44', 1),
(19, 'SSIP Project', 'This project is basically describing how the water which is wasted during washbasin activities can be reused by some process or treatment through which we can clean the water and make it useful for \r\nother purposes.', 1, 'docx', '', 4, 4, 11, '2023-03-25 08:00:14', 1),
(20, 'Computer Networking', 'The Reference modal for Network Communication (Unit 1)', 1, 'pdf', '', 4, 2, 11, '2023-03-25 08:22:28', 1),
(21, 'Object Oriented Programming Language', 'Inheritance notes for OOPS', 1, 'pdf', '', 4, 2, 11, '2023-03-25 08:24:12', 1),
(22, 'Java Sem 4', 'Programming in Java Book By E Balagurusamy', 2, '', 'Programming in Java Book By E Balagurusamy book available at library of BBIT college, those who want\'s can go and collect book from there :)', 3, 3, 11, '2023-03-25 08:26:51', 1),
(23, 'Fundamental of Electrical and Electronics', 'Power Point Presentation Fundamental of Electrical and Electronics :)', 1, 'pptx', '', 4, 3, 11, '2023-03-25 08:35:42', 1),
(24, 'Data Structure And Algorithms', 'DSA Practice Problems...', 1, 'xlsx', '', 2, 2, 11, '2023-03-25 08:48:20', 1),
(25, 'Relational Database Management System', 'Set of old question papers of Relational Database Management System', 1, 'zip', '', 2, 3, 11, '2023-03-25 08:50:37', 1),
(26, 'Working of Machines', 'A small demonstration of how machine works.', 1, 'mp4', '', 1, 1, 2, '2023-03-25 09:04:12', 1);

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
CREATE TABLE IF NOT EXISTS `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `message` text,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `messages`
--

INSERT INTO `messages` (`id`, `user_id`, `message`, `created_at`) VALUES
(1, 16, 'Hi', '2023-03-25 15:52:58'),
(2, 11, 'hiii', '2023-03-25 15:53:01');

-- --------------------------------------------------------

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
CREATE TABLE IF NOT EXISTS `settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `material_per_page` int NOT NULL,
  `approval_required` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `settings`
--

INSERT INTO `settings` (`id`, `material_per_page`, `approval_required`) VALUES
(1, 8, 1);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mobile` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'user',
  `mailverified` tinyint(1) NOT NULL DEFAULT '0',
  `status` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `first_name`, `last_name`, `username`, `email`, `mobile`, `password`, `role`, `mailverified`, `status`, `created_at`) VALUES
(16, 'Manav', 'Manav', 'Manav', 'manav.guru2005@gmail.com', '9898756948', 'manav2005', 'user', 0, 0, '2023-03-25 15:05:27'),
(11, 'Milan', 'Sagar', 'Milan01', 'sagarsagar51009@gmail.com', '8866995547', 'Alves123', 'faculty', 0, 1, '2023-03-25 15:03:09'),
(2, 'Aatish', 'Kumar', 'aatish124', 'aatishk60@gmail.com', '8866726322', 'aatishk60', 'admin', 0, 1, '2023-03-25 15:01:50');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
