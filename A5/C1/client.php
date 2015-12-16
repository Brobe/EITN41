<?php
	$wsdl = "http://localhost/A5/C1/rngService.wsdl";
	$client = new SoapClient($wsdl);
	$response = $client->__soapCall("getRandom", 
		array("min" => 1,"max" => 100));
	print($response);
?>