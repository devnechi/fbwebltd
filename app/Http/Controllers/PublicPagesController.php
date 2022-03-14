<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Mapper;

class PublicPagesController extends Controller
{

    /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Contracts\Support\Renderable
     */
    public function about()
    {
        // Mapper::map(-6.782482, 39.263381);
        Mapper::map(-6.782482, 39.263381, ['zoom' => 18]);
        return view('about-us');
    }

    /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Contracts\Support\Renderable
     */
    public function business()
    {
        return view('services');
    }


      /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Contracts\Support\Renderable
     */
    public function generalServices()
    {
        return view('services');
    }

      /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Contracts\Support\Renderable
     */
    public function singelservice()
    {
        return view('service-single');
    }

          /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Contracts\Support\Renderable
     */
    public function contactus()
    {
        return view('contact-us');
    }


         /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Contracts\Support\Renderable
     */
    public function comingsoon()
    {
        return view('coming-soon');
    }



}
