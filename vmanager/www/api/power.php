<?php
/**
* VM power managment API
*
* GET:
*	action 	- start/shutdown/destroy/reset
*	vmname
**/

require_once  dirname(__FILE__) . '/../include/config.php';
require ROOT . '/include/api-conf.php';

$valid_values  = array('start', 'shutdown', 'destroy', 'reset');
if( empty($_GET['action']) or !in_array($_GET['action'], $valid_values) or
	empty($_GET['vmname'])
){
	header("HTTP/1.1 400 Bad Request");
	die ('invalid request');
}
$vmName = $_GET['vmname'];

require_once dirname(__FILE__) .'/../include/config.php';
$vmanager = new Vmanager();

$stdout='';
switch ($_GET['action']) {
	case 'start':
		$result = $vmanager->start( $vmName, $stdout );
		break;
	case 'shutdown':
		$result = $vmanager->shutdown( $vmName, $stdout );
		break;
	case 'destroy':
		$result = $vmanager->destroy( $vmName, $stdout );
		break;
	case 'reset':
		$result = $vmanager->reset( $vmName, $stdout );
		break;
	default:
		header("HTTP/1.1 501 Not Implemented");
		die('invalid action');
}

if( 0 === $result)
	echo "ok\n";
else
	header("HTTP/1.1 456 Unrecoverable Error");
echo $stdout;
?>