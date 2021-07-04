<?php
$data = $_POST["data"];
// the directory "consent" must be writable by the server
$name = "consent.txt"; 
// write the file to disk
file_put_contents($name, $data, FILE_APPEND);
?>
