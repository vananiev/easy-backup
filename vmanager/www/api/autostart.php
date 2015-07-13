<?php
/**
* On/off autostart function (high availability function).
* When VM is down and 'virsh autostart' is set by this api
* Vm is started by watchdog script in cron
*
* GET:
*	action 	- enable/disable
*	vmname
**/

require_once  dirname(__FILE__) . '/../include/config.php';
require ROOT . '/include/api-conf.php';

$valid_values  = array('enable', 'disable');
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
	case 'enable':
		$result = $vmanager->autostartOn( $vmName, $stdout );
		break;
	case 'disable':
		$result = $vmanager->autostartOff( $vmName, $stdout );
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