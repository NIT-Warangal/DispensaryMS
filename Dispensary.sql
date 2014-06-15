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
  `Date` date NOT NULL,
  `Time` text NOT NULL
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
  `IndexStart` int(11) NOT NULL,
  `IndexEnd` int(11) NOT NULL,
  `Remarks` text NOT NULL,
  `Date` date NOT NULL,
  `Pending` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



--
-- Table structure for table `PrescriptionIndex`
--

CREATE TABLE IF NOT EXISTS `PrescriptionIndex` (
  `Sno` int NOT NULL AUTO_INCREMENT,
  `Medicine` text NOT NULL,
  `Quantity` text NOT NULL,
  PRIMARY KEY (Sno)
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

--
-- Table structure for table `ResetPassword` to keep track of uploads
--

CREATE TABLE IF NOT EXISTS `ResetPassword` (
  `RegNo` text NOT NULL,
  `Date` datetime NOT NULL,
  `Password` text NOT NULL, -- store MD5 of new genereated password here, push this to Login.Password where ResetPassword.RegNo = Login.RegNo
  `PlainKeyHash` text NOT NULL -- store password as text directly here, use this column to send new password
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Table structure for table `CheckPassword` to keep track of uploads
--

CREATE TABLE IF NOT EXISTS `CheckPassword` (
  `RegNo` text NOT NULL,
  `Password` text NOT NULL 
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `ChatSessionHistory`
--

CREATE TABLE IF NOT EXISTS `ChatSessionHistory` (
  `DoctorNo` text NOT NULL, -- Doctor Employee No.
  `RegNo` text NOT NULL, -- Student Registration No.
  `Date` datetime NOT NULL, -- Date of chat
  `StartTime` time NOT NULL,
  `EndTime` time NOT NULL, -- Calculate this by using StartTime+Duration
  `Duration` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `ChatTransactions`
--

-- Link will be <url>?regno, Once the camera and audio have been shared, thats when it enters
-- the database, The list is stored ordered by the number of people who wish to go online.

CREATE TABLE IF NOT EXISTS `ChatQueue` (
  `Sno` int AUTO_INCREMENT,
  `RegNo` text NOT NULL,
  `Date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

----------------------------------------------------
----Tried to use prescription with dependency name column....complexity increased.....keeping it simple
CREATE TABLE IF NOT EXISTS `DependencyPrescription` (
  `DoctorNo` text NOT NULL,
  `Regno` text NOT NULL,
  `DependencyName` text NOT NULL,
  `Cause` text NOT NULL,
  `IndexStart` int(11) NOT NULL,
  `IndexEnd` int(11) NOT NULL,
  `Remarks` text NOT NULL,
  `Date` date NOT NULL,
  `Pending` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
