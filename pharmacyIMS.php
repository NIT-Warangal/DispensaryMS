<?php
$host="localhost";
$port=3306;
$socket="";
$user="root";
$password="";
$dbname="dispensary";

$con = new mysqli($host, $user, $password, $dbname, $port, $socket)
or die ('Could not connect to the database server' . mysqli_connect_error());

$query = "SELECT * FROM `pharmacy` WHERE 1";
$result = mysqli_query($con,$query);

$prev=array();refre($result,$prev);
function refre($result,$prev)
{   echo "<table border='1'>";$id=0;
    global $prev;$prev=array();
    while($row = mysqli_fetch_array($result)) {
    echo "<tr>";
    forma($row,$id);$prev[]=$row['Sno'];
    echo "</tr>";$id++;}
    $row = 0;adem($id);
    echo "</table>";
}

function adem($id)
{
    echo "<tr>". forma(0,$id) ."</tr>";
}
function forma($row,$id){
    $sti = "disabled";$str="";
    if($row){$sti = "";$str="disabled";}
    echo "<form action=''  method='post'>
    <td><input type='text' name='Sno' value='" . $row['Sno'] . "'></td>";
    echo "<td><input type='text' name='Name' value='" . $row['Name'] . "'></td>";
    echo "<input type='hidden' name='jaf' value=".$id.">";
    echo "<td><input type='text' name='Quantity' value='" . $row['Quantity'] . "'></td>";
    echo "<td><input type='text' name='Batch' value='" . $row['Batch no'] . "'></td>";
    echo "<td><input type='date' name='ManufactureDate' value='" . $row['ManufactureDate'] . "'></td>";
    echo "<td><input type='date' name='ExpiryDate' value='" . $row['ExpiryDate'] . "'></td>";
    echo "<td><input name='inser' ".$str." type='submit' value='insert'></td>";
    echo "<td><input name='updat' ".$sti." type='submit' value='update'></td>";
    echo "<td><input name='delet' ".$sti." type='submit' value='delete'></form></td>";
}

if(isset($_POST['inser']))
{   $var = array($_POST['Sno'],$_POST['Name'],$_POST['Quantity'],$_POST['Batch'],$_POST['ManufactureDate'],$_POST['ExpiryDate']);
    $query="INSERT INTO `pharmacy`(`Sno`, `Name`, `Quantity`, `Batch no`, `ManufactureDate`, `ExpiryDate`) VALUES
    ($var[0], $var[1],$var[2] ,$var[3],$var[4],$var[5])";
    $result = (@mysqli_query($con,$query));
    $query = "SELECT * FROM `pharmacy` WHERE 1";
    $result = mysqli_query($con,$query);
    ob_end_clean();
   refre($result,$prev);}
elseif(isset($_POST['updat']))
{   $var = array($_POST['Sno'],$_POST['Name'],$_POST['Quantity'],$_POST['Batch'],$_POST['ManufactureDate'],$_POST['ExpiryDate']);
    $id=(int)$_POST['jaf'];
    $query="UPDATE `pharmacy` SET `Sno`=$var[0],`Name`=$var[1],`Quantity`=$var[2],`Batch no`=$var[3],
    `ManufactureDate`=$var[4],`ExpiryDate`=$var[5] WHERE `Sno`=$prev[$id]";
    $result = (@mysqli_query($con,$query));
    $query = "SELECT * FROM `pharmacy` WHERE 1";
    $result = mysqli_query($con,$query);
    ob_end_clean();
    refre($result,$prev);}
elseif(isset($_POST['delet']))
{    $id=(int)$_POST['jaf'];
    $query="DELETE FROM `dispensary`.`pharmacy` WHERE `pharmacy`.`Sno` = $prev[$id]";
    $result = (@mysqli_query($con,$query));
    $query = "SELECT * FROM `pharmacy` WHERE 1";
    $result = mysqli_query($con,$query);
    ob_end_clean();
    refre($result,$prev);}