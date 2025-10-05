<?php
$bytes = random_bytes(8);
$key = bin2hex($bytes);
echo $key;  
?>
