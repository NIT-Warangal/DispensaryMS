drop table if exists entries;
create table `entries` (
  `id` integer primary key autoincrement,
  `title` text not null,
  `text` text not null
);

----
BEGIN TRANSACTION;

----
-- Table structure for Employee
----
CREATE TABLE `Employee` (
  `RegNo` text NOT NULL,
  `Occupation` text NOT NULL,
  `Location` text NOT NULL,
  `NoOfDependencies` integer NOT NULL
);

----
-- Data dump for Employee, a total of 0 rows
----

----
-- Table structure for HostelWorker
----
CREATE TABLE `HostelWorker` (
  `RegNo` text NOT NULL,
  `Occupation` text NOT NULL,
  `Location` text NOT NULL,
  `NoOfDependencies` integer NOT NULL
);

----
-- Data dump for HostelWorker, a total of 0 rows
----

----
-- Table structure for Login
----
CREATE TABLE `Login` (
  `EmpID` text NOT NULL,
  `UserName` text NOT NULL,
  `Password` text NOT NULL,
  `Occupation` integer NOT NULL
);

----
-- Data dump for Login, a total of 0 rows
----

----
-- Table structure for Pharmacy
----
CREATE TABLE `Pharmacy` (
  `Sno` integer NOT NULL,
  `Name` text NOT NULL,
  `Quantity` integer NOT NULL,
  `Batch no` integer NOT NULL,
  `ManufactureDate` date NOT NULL,
  `ExpiryDate` date NOT NULL
);

----
-- Data dump for Pharmacy, a total of 0 rows
----

----
-- Table structure for Prescription
----
CREATE TABLE `Prescription` (
  `DoctorNo` integer NOT NULL,
  `RegNo` text NOT NULL,
  `Cause` text NOT NULL,
  `Medicine` text NOT NULL,
  `Quantity` integer NOT NULL,
  `Remarks` text NOT NULL
);

----
-- Data dump for Prescription, a total of 0 rows
----

----
-- Table structure for Student
----
CREATE TABLE `Student` (
  `Year` integer NOT NULL,
  `Section` text NOT NULL,
  `Branch` text NOT NULL,
  `Degree` text NOT NULL,
  `RegNo` text NOT NULL,
  `Roll No` text NOT NULL,
  `Hostel` text DEFAULT NULL
);

----
-- Data dump for Student, a total of 0 rows
----

----
-- Table structure for Users
----
CREATE TABLE `Users` (
  `Sno` integer NOT NULL,
  `RegNo` text NOT NULL,
  `First Name` text NOT NULL,
  `Middle Name` text DEFAULT NULL,
  `Last Name` integer NOT NULL,
  `Blood Group` text NOT NULL,
  `Date of Birth` date NOT NULL,
  `Age` integer NOT NULL,
  `Type` integer NOT NULL,
  `Phone number` text NOT NULL,
  `Address` text NOT NULL,
  `email` text NOT NULL
);

----
-- Data dump for Users, a total of 0 rows
----

----
-- Table structure for usersTEST
----
CREATE TABLE `usersTEST` (
  `id` integer NOT NULL,
  `username` text NOT NULL,
  `password` text NOT NULL,
  PRIMARY KEY (`id`)
);

----
-- Data dump for usersTEST, a total of 0 rows
----

----
-- Table structure for user
----
CREATE TABLE `user` (
  `id` integer NOT NULL,
  `username` text NOT NULL,
  `email` text NOT NULL,
  `password` text NOT NULL,
  PRIMARY KEY (`id`)
);

----
-- Data dump for user, a total of 0 rows
----

----
-- structure for index sqlite_autoindex_usersTEST_1 on table usersTEST
----
;

----
-- structure for index sqlite_autoindex_user_1 on table user
----
;
COMMIT;
