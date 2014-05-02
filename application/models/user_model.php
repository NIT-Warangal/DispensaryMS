<?php if( !defined('BASEPATH')) exit('No direct script access allowed');
class User_model extends CI_Model {
	public function __construct()
	{
		parent::__construct();
	}
	function login($regno,$pwd){
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
		}
		return false;
	}
	public function add_user(){
		$regno=$this->input->post('regno');
		$pwd=$this->input->post('pwd');
		$uname=$this->input->post('uname');
		$datas = array('EmpID' => $regno ,
					  'UserName' => $uname,
					  'Password' => md5($pwd),
					  'Occupation'=>$this->input->post('choice'),
		 );
		$this->db->insert('login',$datas);
		$sno=0;
		$query=$this->db->query("select max(Sno) as B from Users");
		$temp=0;
		foreach ($query->result() as $row) {
			$temp=$row->B;
		}
		if($temp==0){
			$sno=1;
		}
		else{
			$sno=$temp+1;
		}
		$db=$this->input->post('dateofbirth');
		$do=date_create($db);
		$datetime1=date_create($db);
		$datetime2=date_create('today');
		$interval=$datetime1->diff($datetime2);
		$age=$interval->y;
		$data=array(
		'Sno' =>$sno ,
		'RegNo'=>$this->input->post('regno'),
		'FirstName'=>$this->input->post('fname'),
		'MiddleName'=>$this->input->post('mname'),
		'LastName'=>$this->input->post('lname'),
		'Gender'=>$this->input->post('sex'),
		'BloodGroup'=>$this->input->post('bgroup'),
		'DateofBirth'=>date_format($do,'Y-m-d'),
		'Age'=>$age,
		'Type'=>$this->input->post('choice'),
		'PhoneNumber'=>$this->input->post('phno'),
		'Address'=>$this->input->post('address'),
		'email'=>$this->input->post('emailid'),
		 );
		$this->db->insert('Users',$data);
		
	}
}
?>