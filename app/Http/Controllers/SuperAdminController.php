<?php

namespace App\Http\Controllers;


use App\Http\Controllers\Controller;
use App\Providers\RouteServiceProvider;
use Illuminate\Foundation\Auth\AuthenticatesUsers;
use Illuminate\Http\Request;

class SuperAdminController extends Controller
{
    /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Contracts\Support\Renderable
     */
    public function index()
    {
        //to super admin dashboard
         return view('main-admin.sadmin-dashboard');

       //return dd(Auth::user()->role_id);
    }

    // super admin manage users
    public function navManageUsers(){
        return view('main-admin.fbc-users.user-management');

    }

    // super admin add new users
    public function navCreateNewUser(){
        return view('main-admin.fbc-users.add-new-user');
    }

    // manage fbc-projects
    public function navManageProjects(){
        return view('main-admin.fbc-projects.fbc-projects-management');
    }

    // create new fbc-project
    public function navCreateNewProject(){

        return view('main-admin.fbc-projects.add-new-project');
    }

    public function navManageHRactivities(){
        return view('main-admin.fbc-hr.hr-management');
    }

    public function navManageFMactivities(){
        return view('main-admin.fbc-fm.fbc-management');
    }

    public function navCreateNewPV(){
        return view('main-admin.fbc-fm.create-new-pv');
    }
}

