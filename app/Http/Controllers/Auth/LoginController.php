<?php

namespace App\Http\Controllers\Auth;


use App\Http\Controllers\Controller;
use App\Providers\RouteServiceProvider;
use Illuminate\Foundation\Auth\AuthenticatesUsers;
use Illuminate\Http\Request;

use Illuminate\Support\Facades\Auth;
class LoginController extends Controller
{
    /*
    |--------------------------------------------------------------------------
    | Login Controller
    |--------------------------------------------------------------------------
    |
    | This controller handles authenticating users for the application and
    | redirecting them to your home screen. The controller uses a trait
    | to conveniently provide its functionality to your applications.
    |
    */

    use AuthenticatesUsers;

    /**
     * Where to redirect users after login.
     *
     * @var string
     */
    // protected $redirectTo = RouteServiceProvider::HOME;

     protected $redirectTo;
    public function redirectTo(){

        // if (Auth::user()->usertype_id == 1){
        //     $this->redirectTo = '/admin';
        //         return $this->redirectTo;
        // }else{
        //     $this->redirectTo = '/login';
        //     return $this->redirectTo;
        // }

        // dd(Auth::user()->role_id);

        switch(Auth::user()->role_id){
            case 1:
                //to super admin
            $this->redirectTo = '/main-admin';
            return $this->redirectTo;
                break;
            case 2:
                //to future basics admin
                $this->redirectTo = '/fbc-admin';
                return $this->redirectTo;
                break;
            case 3:
                //to normal user
                $this->redirectTo = '/fbc-user';
                return $this->redirectTo;
                break;
            default:
                $this->redirectTo = '/login';
                return $this->redirectTo;
        }
    }


      /**
     * Create a new controller instance.
     *
     * @return void
     */
    public function __construct()
    {
        $this->middleware('guest')->except('logout');
    }
}
