<?php

namespace App\Providers;
use App\Validators\ReCaptcha;

use Illuminate\Support\ServiceProvider;
use Illuminate\Support\Facades\Validator;
use Auth;


class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        //
        Validator::extend('recaptcha', 'App\\Validators\\ReCaptcha@validate');
        // if(Auth::check() && Auth::user()->email == "devnechi@gmail.com" ){
        //   \Debugbar::enable();
        // }else{
        //   \Debugbar::disable();
        // }
    }
}
