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
        // Mapper::map(-6.782482, 39.263381, ['zoom' => 18]);
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
    public function graphicAllservices()
    {
        // return view('service-single');
        return view('services.graphics.graphics-design-services');

    }

    public function graphicServicesDetails(){
        return view('services.graphics.graphic-design-service-details');
    }


      /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Contracts\Support\Renderable
     */
    public function protoAllservices()
    {
        // return view('service-single');
        return view('services.prototyping.all-prototyping-services');

    }

    public function protoServicesDetails(){
        return view('services.graphics.graphic-design-service-details');
    }


      /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Contracts\Support\Renderable
     */
    public function softDevAllservices()
    {
        // return view('service-single');
        return view('services.development.all-software-dev-services');

    }

    public function softDevServicesDetails(){
        return view('services.development.software-dev-service-details');
    }

          /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Contracts\Support\Renderable
     */
    public function alldataScienceservices()
    {
        // return view('service-single');
        return view('services.datascience.all-data-science-services');

    }

    public function dataScienceServicesDetails(){
        return view('services.datascience.data-science-service-details');
    }



    public function careersWithUs(){
        return view('careers.careers');
    }

    public function jobDetails(){
      return view('careers.career-details');
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


    public function alldevPoolForms(){
        return view('recruit.all-coll-forms-access');

    }

    public function devRecruitForm(){
        return view('recruit.dev-pool-coll-form');
    }

    public function designersRecruitForm(){
        return view('recruit.designers-details-form');
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
