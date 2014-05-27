-- phpMyAdmin SQL Dump
-- version 4.1.12
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: May 19, 2014 at 02:26 PM
-- Server version: 5.5.37-0ubuntu0.14.04.1
-- PHP Version: 5.5.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `Dispensary`
--

-- --------------------------------------------------------
create table `entries` (
  `id` integer primary key AUTO_INCREMENT,
  `title` text not null,
  `text` text not null
);
--
-- Table structure for table `Employee`
--
CREATE TABLE IF NOT EXISTS `Employee` (
  `RegNo` text NOT NULL,
  `Occupation` text NOT NULL,
  `EmergencyContact` text NOT NULL,
  `Location` text NOT NULL,
  `NoOfDependencies` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
--
-- Dumping data for table `Employee`
--

INSERT INTO `Employee` (`RegNo`, `Occupation`, `Location`, `NoOfDependencies`) VALUES
('127223', 'emp', 'secunderabad', 4);

-- --------------------------------------------------------

--
-- Table structure for table `HostelWorker`
--

CREATE TABLE IF NOT EXISTS `HostelWorker` (
  `RegNo` text NOT NULL,
  `Occupation` text NOT NULL,
  `Location` text NOT NULL,
  `NoOfDependencies` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Login`
--

CREATE TABLE IF NOT EXISTS `Login` (
  `EmpID` text NOT NULL,
  `UserName` text NOT NULL,
  `Password` text NOT NULL,
  `Occupation` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

-- --------------------------------------------------------

--
-- Table structure for table `Bills` to keep track of uploads
--

CREATE TABLE IF NOT EXISTS `Bills` (
  `FileName` text NOT NULL,
  `Date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Pharmacy`
--

CREATE TABLE IF NOT EXISTS `Pharmacy` (
  `Sno` int(11) NOT NULL,
  `Name` text NOT NULL,
  `Quantity` int(11) NOT NULL,
  `Batchno` int(11) NOT NULL,
  `ManufactureDate` date NOT NULL,
  `ExpiryDate` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Prescription`
--

CREATE TABLE IF NOT EXISTS `Prescription` (
  `DoctorNo` int(11) NOT NULL,
  `RegNo` text NOT NULL,
  `Cause` text NOT NULL,
  `Medicine` text NOT NULL,
  `Quantity` int(11) NOT NULL,
  `Remarks` text NOT NULL,
  `Date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Student`
--


CREATE TABLE IF NOT EXISTS `Student` (
  `Year` int(11) NOT NULL,
  `Section` text NOT NULL,
  `Branch` text NOT NULL,
  `Degree` text NOT NULL,
  `RegNo` text NOT NULL,
  `RollNo` text NOT NULL,
  `Emergencyphone` text NOT NULL,
  `Hostel` text,
  `HostelRoomNo` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- --------------------------------------------------------

--
-- Table structure for table `Users`
--

CREATE TABLE IF NOT EXISTS `Users` (
  `Sno` int(11) NOT NULL AUTO_INCREMENT,
  `RegNo` text NOT NULL,
  `FirstName` text NOT NULL,
  `MiddleName` text,
  `LastName` text NOT NULL,
  `BloodGroup` text NOT NULL,
  `DateofBirth` date NOT NULL,
  `Age` int(11) NOT NULL,
  `Type` int(11) NOT NULL,
  `Phonenumber` text NOT NULL,
  `Address` text NOT NULL,
  `email` text NOT NULL,
  `gender` text NOT NULL,
  PRIMARY KEY (Sno)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `Dependencies` (
  `Regno` int(11) NOT NULL,
  `Name` text NOT NULL,
  `DateofBirth` datetime NOT NULL,
  `Sex` text NOT NULL,
  `Relation` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Table structure for table `Letters` to keep track of uploads
--

CREATE TABLE IF NOT EXISTS `Letters` (
  `RegNo` text NOT NULL,
  `Date` datetime NOT NULL,
  `Days` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
