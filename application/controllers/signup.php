<?php if( ! defined('BASEPATH')) exit('No direct script access allowed');
class Signup extends CI_Controller{
	public function __construct()
	{
		parent::__construct();
		$this->load->model('user_model');
	}
	public function index()
	{
		if(($this->session->userdata('user_regno')!=""))
		{
			$this->welcome();
		}
		else
		{
			$data['title']='Home';
			$this->load->view("signup_view.php",$data);
			
		}
	}
	public function welcome()
	{
		$data['title']='Welcome';
		echo "<br>welcome<br>";
		$this->load->view('header_view',$data);
		$this->load->view('welcome_view.php',$data);
		$this->load->view('footer_view',$data);
	}
	public function login()
	{
		$regno=$this->$input->post('regno');
		$pwd=md5($this->input->post('pwd'));
		echo "$regno    $pwd";
		$result=$this->user_model->login($regno,$pwd);
		echo "$regno  $pwd";
		if($result) $this->welcome();
		else 		$this->index();
	}
	public function thank()
	{
		$data['title']='Thank';
		$this->load->view('header_view',$data);
		$this->load->view('thank_view',$data);
		$this->load->view('footer_view',$data);
	}
	public function signup()
	{	
		echo "Signup";
		$this->load->library('form_validation');
		$this->form_validation->set_rules('regno','Registration Number','required');
		$this->form_validation->set_rules('pwd','Password','required');
		$this->form_validation->set_rules('con_password','Password Confirmation','required|matches[pwd]');
		$wru = $this->input->post('choice');
		$regno = $this->input->post('regno');
		$fname = $this->input->post('fname');
		$mname = $this->input->post('mname');
		$lname = $this->input->post('lname');
		$gender = $this->input->post('sex');
		$pwd = $this->input->post('pwd');
		$bgroup = $this->input->post('bgroup');
		$adrs = $this->input->post('address');
		$dob = $this->input->post('dateofbirth');
		$phno = $this->input->post('phno');
		$emailid = $this->input->post('emailid');
		$sendarr=[
		"regno"=> $regno,
		"fname"=> $fname,
		"mname"=> $mname,
		"lname"=> $lname,
		"gender"=>$gender,
		"bgroup"=>$bgroup,
		"dob"=>$dob,
		"wru"=>$wru,
		"pwd"=>$pwd,
		"phone"=>$phno,
		"address"=>$adrs,
		"email"=>$emailid,
		];
		
	
		if($this->form_validation->run() == FALSE)
		{
			$this->index();
		}		
		else
		{
			$this->user_model->add_user($sendarr);
			$this->thank();
		}
	}
	public function logout()
	{
		$newdata= array
		( 
		'user_regno'=>'',
		'user_empid'=>'',
		'user_type'=>'',
		'logged_in'=>FALSE,
		);
		$this->session->unset_userdata($newdata);
		$this->session->session_destroy();
		$this->index();
	}
}
?>