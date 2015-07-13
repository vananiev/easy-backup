<?php

require_once ROOT . '/include/class-auth.php';

try{
	if( ! $auth->isAdmin() )
		throw new Exception("You should be 'admin' to call api");
}catch(Exception $e){
	header("HTTP/1.1 400 Bad Request");
	die( $e->getMessage() );
}
?>