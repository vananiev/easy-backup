<?php
	require_once dirname( __FILE__ ) . '/include/config.php';
	require_once ROOT . '/include/class-index-page.php';
?>
<html>
<head>
	<title>Менеджер VM</title>
	<meta charset="utf-8">
	<link rel="stylesheet" type="text/css" href="css/switch.css">
	<link rel="stylesheet" type="text/css" href="css/button.css">
	<link rel="stylesheet" type="text/css" href="css/main.css">
	<script src="js/jquery-1.11.2.js"></script>
	<script src="js/ajaxUpdater.js"></script>
	<link rel="stylesheet" type="text/css" href="//cdnjs.cloudflare.com/ajax/libs/jquery-jgrowl/1.4.1/jquery.jgrowl.min.css" />
	<script src="//cdnjs.cloudflare.com/ajax/libs/jquery-jgrowl/1.4.1/jquery.jgrowl.min.js"></script>
</head>
<body>
<h1>Виртуальные сервера</h1>
<?php

$index = new IndexPage();

$index->vmInfoTable();

?>
<p>
<b>HA (High Availability)</b> - функция периодически (раз в 2 мин) отслеживает состояние сервера (включен/выключен) и
автоматически запускает сервер, если он выключен.
Единственное принудительное исключение: High Availability не стартует сервер, когда он находится
в состоянии бекапа (не важно ручного или запущенного автоматически по расписанию).
Если необходимо произвести работу на выключенном сервере, функцию High Availability необходимо выключить на время проведения работ.
</p>
<script>
	setTimeout(function(){ document.location.reload1();} , 60000);
</script>
</body>
</html>