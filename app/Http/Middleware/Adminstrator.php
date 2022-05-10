<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class Adminstrator
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */

    public function handle($request, Closure $next)
    {
        if (!Auth::check()) {
            return redirect()->route('login');
        }

        if (Auth::user()->role_id == 1) {
            //to superadmin
            return redirect()->route('main-admin');
        }

        if (Auth::user()->role_id == 2) {
            //to admin
            return $next($request);
        }

        if (Auth::user()->role_id == 3) {
            return redirect()->route('fbc-user');
        }
    }

}
