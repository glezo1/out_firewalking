<?php
	$server	=	$_REQUEST['server'];
	$socket	=	socket_create(AF_INET,SOCK_STREAM,SOL_TCP);
	for($i=1;$i<=65535;$i++)
	{
		socket_connect($socket,$server,$i);
	}
	echo "DONE";
?>
