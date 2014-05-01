<?php
$host="localhost:3306";
$user="root";
$pswrd="kiran123"; // password for logging into mysql
$dbname="dispensary";
$con=new mysqli($host,$user,$pswrd,$dbname)
or die("Could not connect to db server".mysqli_connect_error());
$wru=$_POST['choice'];
$fname=$_POST['fname'];
$mname=$_POST['mname'];
$lname=$_POST['lname'];
$bgroup=$_POST['bgroup'];
$adrs=$_POST['address'];
$dob=$_POST['dateofbirth'];
$phno=$_POST['phno'];
$emailid=$_POST['emailid'];
$gender=$_POST['sex'];
echo "$fname $mname $lname bloodgroup: $bgroup is a $gender $wru born on $dob Phone: $phno Email $emailid </br>
		<h1>Residence address:</h1> $adrs";
?>