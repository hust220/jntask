<?php
error_reporting(E_ALL);

$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
if ($socket === false) {
   echo "socket_create() failed: reason: " . socket_strerror(socket_last_error()) . "\n";
}

$result = socket_connect($socket, '127.0.0.1', 8888);
if ($result === false) {
   echo "socket_connect() failed.\nReason: ($result) " . socket_strerror(socket_last_error($socket)) . "\n";
}

$in = 'S{"cmd":"ls"}';
$out = '';

socket_write($socket, $in, strlen($in));
while ($out = socket_read($socket, 2048)) {
   echo $out;
}
socket_close($socket);
?>

