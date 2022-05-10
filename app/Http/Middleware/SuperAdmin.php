<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class SuperAdmin
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle(Request $request, Closure $next)
    {
        if (!Auth::check()) {
            return redirect()->route('login');
        }

        if (Auth::user()->role_id == 1) {
            //to superadmin
            return $next($request);

        }

        if (Auth::user()->role_id == 2) {
            //to admin
            return redirect()->route('fbc-admin');
        }

        if (Auth::user()->role_id == 3) {
            return redirect()->route('fbc-user');
        }
    }
}
