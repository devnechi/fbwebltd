<?php

namespace Tests\Feature;

use Illuminate\Support\Facades\DB;
use Tests\TestCase;

class HealthEndpointTest extends TestCase
{
    public function test_health_endpoint_returns_healthy_when_database_is_available()
    {
        DB::shouldReceive('connection->select')
            ->once()
            ->with('SELECT 1')
            ->andReturn([(object) ['1' => 1]]);

        $response = $this->getJson('/api/health');

        $response->assertStatus(200)
            ->assertExactJson(['status' => 'healthy']);
    }

    public function test_health_endpoint_returns_unhealthy_when_database_is_unavailable()
    {
        DB::shouldReceive('connection->select')
            ->once()
            ->with('SELECT 1')
            ->andThrow(new \RuntimeException('Database unavailable'));

        $response = $this->getJson('/api/health');

        $response->assertStatus(503)
            ->assertExactJson(['status' => 'unhealthy']);
    }
}
