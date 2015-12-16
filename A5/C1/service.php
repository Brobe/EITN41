<?php
	function getRandom($min,$max){
		//code for RNG
		return 10;
	}
	$server = new SoapServer("rngService.wsdl");
	$server->addFunction("getRandom");
	$server->handle();
?>