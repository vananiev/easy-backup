<?php

class Auth{

	private $user = null;

	function __construct(){
		$this->login();
	}

	public function isAdmin(){
		if( $this->user == 'admin' ){
			/* user is login using valid password */
			/* password is contained in $_SERVER['PHP_AUTH_PW'] */
			return true;
		}else
			return false;
	}

	private function isLogined(){
		if ( isset($_SERVER['PHP_AUTH_USER']) ){
			$this->user = $_SERVER['PHP_AUTH_USER'];
		    return true;
		}
		else 
			return false;
	}

	public function login(){
		if( !$this->isLogined() ){
			header('WWW-Authenticate: Basic realm="My Realm"');
		    header('HTTP/1.0 401 Unauthorized');
		    echo 'You hits Cancel button'; //Text to send if user hits Cancel button
		    exit;
		}
	}
}

/* Если не залогинены - требуем логин */
$auth = new Auth();

?>