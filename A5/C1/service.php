<?php
	function predictFuture($age,$name){
		//code for RNG
		 
		$futureEvents = "Nothing out of the ordinary will happen to you";
		$futureAge = 100;
		$futurePassion = "Undecided";
		//predict the age
		if ( $age < 0 ){
			return "You are not yet born, sorry, no future can be predicted";
		}else if( $age < 20 ){
			$futureAge = $age + 80;
		}else if( $age > 100 ){
			$futureAge = $age + 1;
		}

		if ( $name == "Melinda" ){
			$futureEvents = "You will learn to sky dive";
		}else if( $name == "Steve" && $age < 80){
			$futureEvents = "You will find a passion for spring onion";
		}

		$magicVal = (hash($name) + hash($age)) % 3;
		if ( $magicVal == 0 ){
			$futurePassion = "bird watching";
		}else if( $magicVal == 1 ){
			$futurePassion = "calendar collector";
		}else if( $magicVal == 2 ){
			$futurePassion = "snake charmer";
		}

		$ageInfo = "You will live for at least a total of {$futureAge} years";
		$futurePassionInfo = "Your future passion will be {$futurePassion}";
		return "{$ageInfo}</br>{$futureEvents}<br>{$futurePassionInfo}";
	}

	$server = new SoapServer("pfService.wsdl");
	$server->addFunction("predictFuture");
	$server->handle();
?>