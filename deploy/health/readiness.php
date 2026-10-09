<?php

declare(strict_types=1);

use Illuminate\Contracts\Console\Kernel;
use Illuminate\Support\Facades\DB;

try {
    require __DIR__ . '/../../vendor/autoload.php';

    $app = require __DIR__ . '/../../bootstrap/app.php';

    $app->make(Kernel::class)->bootstrap();

    DB::connection()->select('SELECT 1');

    echo "Laravel and database ready\n";
    exit(0);
} catch (Throwable $exception) {
    fwrite(STDERR, "Laravel readiness failed\n");
    exit(1);
}
