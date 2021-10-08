<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Notifications\Notifiable;

class UserType
{
    // use Notifiables;


    // protected $primaryKey = "user_id";
    // protected $table = 'users';
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle(Request $request, Closure $next)
    {

        if(auth()->user()->usertype_id == 1){
            return $next($request);
        }

        return redirect('home')->with('error',"You don't have admin access.");

    }
}
