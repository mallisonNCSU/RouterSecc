<?php

$post_data = $_POST['data'];
if(!empty($post_data)){
	$filename = 'userinput.txt';
//	$filename = '/python/userinput.txt';	//uncomment this to have output go into python folder
	$handle = fopen($filename, "w");
	fwrite($handle, $post_data);
	fclose($handle);

	echo $file;
}

?>
