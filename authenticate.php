<?php
$username = $_POST['uname'];
$password = $_POST['pwd'];
$id= $_POST['empid'];
$occup=$_POST['occupation'];
$host='localhost';
$port=3306;
$user='root';
$password='kiran123';
$dbname='dispensary';
$con=new mysqli($host,$user,$password,$dbname,$port)
or die('Could not connect to db server'.mysqli_connect_error());
$flag=0;
$encrypted = encryptIt( $password );
/*echo $username."</br> password:".$password."</br>";
echo $encrypted . '<br />';*/

$query="select * from login";
$result=(@mysqli_query($con,$query));
while($row = mysqli_fetch_array($result,MYSQLI_ASSOC)){
	if(($row['EmpID']===$id) && ($row['Occupation']===$occup) && ($row['UserName']===$username)){
		if(encryptIt($row['Password'])===encryptIt($password)){
			$flag=1;
			break;
		}
	}
}
if($flag===1){
Redirect('http://localhost/DispensaryMS/index.php', false);
//change the redirect address here
}
function Redirect($url, $permanent = false){
    if (headers_sent() === false)
    	header('Location: ' . $url, true, ($permanent === true) ? 301 : 302);
    exit();
}

function encryptIt( $q ) {
    $cryptKey  = '5745b2d9552457192ccbfe3ebc53d491';
    $qEncoded      = base64_encode( mcrypt_encrypt( MCRYPT_RIJNDAEL_256, md5( $cryptKey ), $q, MCRYPT_MODE_CBC, md5( md5( $cryptKey ) ) ) );
    return( $qEncoded );
}

function decryptIt( $q ) {
    $cryptKey  = '5745b2d9552457192ccbfe3ebc53d491';
    $qDecoded      = rtrim( mcrypt_decrypt( MCRYPT_RIJNDAEL_256, md5( $cryptKey ), base64_decode( $q ), MCRYPT_MODE_CBC, md5( md5( $cryptKey ) ) ), "\0");
    return( $qDecoded );
}
?>