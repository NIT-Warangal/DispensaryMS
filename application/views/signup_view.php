<!doctype html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>SignUp Page</title>
	<link rel="stylesheet" href="assets/css/signup.css">
	<link href="assets/css/bootstrap.css" rel="stylesheet">

</head>
<body>
		<?php echo validation_errors('<p style="color:#F00">'); ?>
    <?php echo form_open('Signup/signup'); ?>
    <!--equivalent to <form method="post" action="http://localhost/DispensaryMS/application/controllers/signup"> -->
	<div class="signup-page">
		<div class="header-section">
			<a href="#"><img src="assets/images/loginlogo.png" alt=""></a>
			<ul class="menu">
<!--
				<li><a href="index.html">Home</a></li>
				<li><a href="register.html">Sign up</a></li>
-->
			</ul>
		</div><!--end of header -section-->
	
<div class="row">
          <div class="col-lg-10 col-lg-offset-1">
            <div class="well bs-component col-lg-offset-1">
              <div class="form-horizontal" >
                <fieldset>
                  <legend>Registration Form</legend>
                  <div class="form-group">
                  	<label for="select" class="col-lg-2 col-lg-offset-1 control-label"  >Who are you?</label>
                  	<div class="col-lg-4">
                      <select class="form-control" name="choice" >
                      	<option value="0">Select One Option</option>
                        <option value="1">Student</option>
                        <option value="2">Employee</option>
                        <option value="3">Guest</option>
                      </select>
                  	</div>
                  </div>
                  <div class="form-group">
                    <label for="regNumber"  style="text-align:center;font-size:96.3%;"class="col-lg-2 col-lg-offset-1">Registration Number/Employee ID</label>
                    <div class="col-lg-4">
                      <input type="text" class="form-control"  required name="regno" placeholder="Enter your Reg. Number/Employee ID">
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="firstname" class="col-lg-2 col-lg-offset-1 control-label">First Name</label>
                    <div class="col-lg-6">
                      <input type="text" class="form-control"  required name="fname" placeholder="Enter your First Name">
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="middlename" class="col-lg-2 col-lg-offset-1 control-label">Middle Name</label>
                    <div class="col-lg-6">
                      <input type="text" class="form-control" name="mname" placeholder="Enter your Middle Name">
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="lastname" class="col-lg-2 col-lg-offset-1 control-label">Last Name</label>
                    <div class="col-lg-6">
                      <input type="text" class="form-control" name="lname" placeholder="Enter your Last Name">
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="gender" class="col-lg-2 col-lg-offset-1 control-label">Gender</label>
                    <div class="col-lg-3">
                      <select class="form-control" name="sex">
                        <option>Select Gender</option>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                      </select>
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="username" class="col-lg-2 col-lg-offset-1 control-label">UserName</label>
                    <div class="col-lg-5">
                      <input type="text" class="form-control" name="uname"  required placeholder="UserName">
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="password" class="col-lg-2 col-lg-offset-1 control-label">Password</label>
                    <div class="col-lg-5">
                      <input type="password" class="form-control" name="pwd"  required placeholder="Password">
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="confirmPassword" class="col-lg-2 col-lg-offset-1 control-label">Confirm Password</label>
                    <div class="col-lg-5">
                      <input type="password"  required class="form-control" name="con_password" placeholder="Confirm Password" onchange="check();">
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="bloodGroup" class="col-lg-2 col-lg-offset-1 control-label">Blood Group</label>
                    <div class="col-lg-3">
                      <select class="form-control" name="bgroup"  required>
                        <option value="0">Select One Option</option>
                        <option value="A+">A+</option>
                        <option value="A-">A-</option>
                        <option value="B+">B+</option>
                        <option value="B-">B-</option>
                        <option value="AB+">AB+</option>
                        <option value="AB-">AB-</option>
                        <option value="O+">O+</option>
                        <option value="O-">O-</option>
                      </select>
                    </div>
                  </div>
                  <div class="form-group">
                      <label for="dateofBirth" class="col-lg-2 col-lg-offset-1 control-label">Date Of Birth</label>
                      <div class="col-lg-3">
                      <input type="date" class="form-control" name="dateofbirth"  placeholder="dd/mm/yyyy">
                    </div>
                  </div>
                  <div class="form-group">
                      <label for="phoneNumber" class="col-lg-2 col-lg-offset-1 control-label">Phone Number</label>
                      <div class="col-lg-4">
                      <input type='tel' pattern='[\+]\d{2}[\-]\d{10}'  required  class="form-control" name="phno" placeholder="Phone/mobile Number(Format: +91-9999999999)">
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="textArea" class="col-lg-2 col-lg-offset-1 control-label">Address</label>
                    <div class="col-lg-6">
                      <textarea class="form-control" rows="3" name="address"></textarea>
                      <span class="help-block">Enter your address here!</span>
                    </div>
                  </div>
                  <div class="form-group">
                      <label for="mail" class="col-lg-2 col-lg-offset-1 control-label">Email address</label>
                      <div class="col-lg-8">
                      <input type="email" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$" class="form-control" name="emailid" placeholder="Enter Email address (example: abcdef@abcd.com)"  >
                    </div>
                  </div>
                  <div class="form-group">
                    <div class="col-lg-10 col-lg-offset-2">
                      <button class="btn btn-default">Cancel</button>
                      <button type="submit" class="btn btn-primary">Submit</button>
                    </div>
                  </div>
                </fieldset>
              </div>
            </div>
          </div>
          </div>
        </div>
    </div>
  </div><!--end of signup-page-->
              <?php echo form_close(); ?>
</body>
</html>