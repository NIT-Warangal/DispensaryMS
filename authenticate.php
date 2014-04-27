<?php
$username = $_POST['uname'];
$password = $_POST['pwd'];
$id="123456";//$_POST['empid'];                // "123456";
$occup=1;//$_POST['occupation'];        //1;
$host="localhost:3306";
$user="root";
$pswrd="kiran123";
$dbname="dispensary";
$con=new mysqli($host,$user,$pswrd,$dbname)
or die("Could not connect to db server".mysqli_connect_error());

$flag=0;
$encrypted = encryption( $password );

$query="select * from login";
$result=(@mysqli_query($con,$query));
while($row = mysqli_fetch_array($result,MYSQLI_ASSOC)){

    if((strcmp($row['EmpID'],$id)==0) && 
        ($row['Occupation']==$occup) && 
        (strcmp($row['UserName'],$username)==0)){
        if(strcmp($row['Password'],$encrypted)==0){
            $flag=1;
            break;
        }
    }

}
if($flag==1){
    echo "<br><h1> You have successfully logged in!
    You will now be redirected in a moment</h1>";   
    $url="http://localhost/DispensaryMS/index.php";
    //change the redirect address here
    Redirect($url, false);
    echo "If you are not redirected then click this 
    <a href='".$url."'>link</a>";

}
else{
    echo "<h2>Username or password entered is invalid!<br>
    You are not authorised to view this page.Access Denied</h2>";
}

function Redirect($url, $permanent = false){
    if (headers_sent() === false)
        header('Location: ' . $url, true, ($permanent === true) ? 301 : 302);
    exit();
}

function encryption( $key ) {
    $cryptKey  = '5745b2d9552457192ccbfe3ebc53d491';
    $EncodedKey      = base64_encode( mcrypt_encrypt( MCRYPT_RIJNDAEL_256, md5( $cryptKey ), $key, MCRYPT_MODE_CBC, md5( md5( $cryptKey ) ) ) );
    return( $EncodedKey );
}

function decryption( $key ) {
    $cryptKey  = '5745b2d9552457192ccbfe3ebc53d491';//double hashed value of key="kiran123"
    $DecodedKey      = rtrim( mcrypt_decrypt( MCRYPT_RIJNDAEL_256, md5( $cryptKey ), base64_decode( $key ), MCRYPT_MODE_CBC, md5( md5( $cryptKey ) ) ), "\0");
    return( $DecodedKey );
}
?>