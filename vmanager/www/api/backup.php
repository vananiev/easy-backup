<?php
/**
* VM power managment API
*
* GET:
*	vmname
**/

require_once  dirname(__FILE__) . '/../include/config.php';
require ROOT . '/include/api-conf.php';

if( empty($_GET['vmname'])
){
	header("HTTP/1.1 400 Bad Request");
	die ('invalid request');
}
$vmName = $_GET['vmname'];

require_once dirname(__FILE__) .'/../include/config.php';
$vmanager = new Vmanager();

$stdout='';
if( 0 === $vmanager->backup( $vmName, $stdout ))
	echo "ok\n";
else
	header("HTTP/1.1 456 Unrecoverable Error");
echo $stdout;
?>