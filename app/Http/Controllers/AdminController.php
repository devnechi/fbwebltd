<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class AdminController extends Controller
{
   /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Contracts\Support\Renderable
     */
    public function index()
    {
        return view('admin.admin-dashboard');
    }



    public function addnewproject(){
        return view('admin.projects.add-new-project');
    }

    public function manageprojects()
    {
        return view('admin.projects.manage-projects');
    }



    public function toregisternewuser(){
        return view('admin.users.register-new-user');
    }

    public function tousermanagement(){
        return view('admin.users.user-management');
    }
}
