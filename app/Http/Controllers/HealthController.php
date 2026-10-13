<?php

namespace App\Http\Controllers;

use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\DB;

class HealthController extends Controller
{
    public function index(): JsonResponse
    {
        try {
            DB::connection()->select('SELECT 1');

            return response()->json([
                'status' => 'healthy',
            ], 200);
        } catch (\Throwable $exception) {
            return response()->json([
                'status' => 'unhealthy',
            ], 503);
        }
    }
}
