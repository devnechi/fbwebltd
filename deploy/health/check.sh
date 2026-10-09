#!/bin/sh
set -eu

cd /var/www/html

# Check PHP-FPM's listening socket.
php -r '
$socket = @fsockopen("127.0.0.1", 9000, $errno, $errstr, 2);
if (!$socket) {
    fwrite(STDERR, "PHP-FPM is not accepting connections\n");
    exit(1);
}
fclose($socket);
'

# Check Laravel bootstrap and database connectivity.
php deploy/health/readiness.php
