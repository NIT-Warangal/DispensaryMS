<?php if( !defined('BASEPATH')) exit('No direct script access allowed');
class User_model extends CI_Model {
	public function __construct()
	{
		parent::__construct();
	}
	function login($regno,$pwd){
		try{
		$this->db->where("EmpID",$regno);
		$this->db->where("Password",$pwd);

		$query=$this->db->get("login");
		if($query->num_rows()>0)
		{
			foreach ($query->result() as $rows) 
			{
				$newdata = array(
								'user_id' =>$rows->EmpID , 
								'user_name' => $rows->UserName,
								'user_occupation'=>$rows->Occupation,
								'logged_in'=>TRUE,
							);	
			}
		$this->session->set_userdata($newdata);
		return true;
		}}
		catch(Exception $e){
        log_message('debug',$e->getMessage()); // use codeigniters built in logging library
        show_error($e->getMessage()); // or echo $e->getMessage()
      }
		return false;
	}
	public function adduser($sendarr){
		$regno=$sendarr['regno'];
		$pwd=$this->input->post['pwd'];
		$uname=$this->input->post['uname'];
		$datas = array('EmpID' => $regno ,
					  'UserName' => $uname,
					  'Password' => md5($pwd),
					  'Occupation'=>$sendarr['wru'],
		 );
		$this->db->insert('login',$datas);
		$sno=0;
		$query=$this->db->query("select max(sno) from Users");
		$temp=$query->result();
		if($temp==0){
			$sno=1;
		}
		else{
			$sno=$temp+1;
		}
		$age=0;
		$from=new DateTime($sendarr['dob']);
		$to=new DateTime('today');
		$from->diff($to)->$age;
		$data=array(
		'Sno' =>$sno ,
		'RegNo'=>$this->input->post('regno'),
		'First Name'=>$this->input->post('fname'),
		'Middle Name'=>$this->input->post('mname'),
		'Last Name'=>$this->input->post('lname'),
		'Gender'=>$this->input->post('sex'),
		'Blood Group'=>$this->input->post('bgroup'),
		'Date of Birth'=>$this->input->post('dob'),
		'Age'=>$age,
		'Type'=>$this->input->post('choice'),
		'Phone number'=>$this->input->post('phno'),
		'Address'=>$this->input->post('address'),
		'email'=>$this->input->post('emailid'),
		 );
		#$this->db->query("insert into Users values($sno,?,?,?,?,?,?,?,$age,?,?,?,?)",$sendarr);
		$this->db->insert('Users',$data);
		echo "inserted";
	}
}
?>