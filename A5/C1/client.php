<?php
if (!isset($_POST['submitok'])){
?>
	<form action="<?=$_SERVER['PHP_SELF']?>" method="post">
		Name: <input type="text" name="name"><br>
		Age: <input type="text" name="age"><br>
		<input type="submit" name="submitok">
	</form>
<?php
}else{
	if ($_POST['name']=='' or $_POST['age']==''){
        print('One or more required fields were left blank.\n'.'Please fill them in and try again.');
    	return;
    }
    if (!is_numeric($_POST['age'])){
    	print('Please make sure the age is an integer');
    	return;
    }
    $name = $_POST['name'];
    $age = intval($_POST['age']);
	$wsdl = "http://localhost/A5/C1/pfService.wsdl";
	$client = new SoapClient($wsdl);
	$response = $client->__soapCall("predictFuture", 
		array("age" => $age,"name" => $name));
	print($response);
}
?>