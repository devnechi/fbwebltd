<?php

namespace App\Http\Controllers;


use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Validator;
use App\Http\Controllers\Exception;
use Illuminate\Support\Str;
use Illuminate\Support\Facades\Storage;
use App\Providers\RouteServiceProvider;
use Illuminate\Foundation\Auth\AuthenticatesUsers;
use Illuminate\Http\Request;
use App\Models\Role;
use App\Models\Gender;
use App\Models\User;
use DB;

use Carbon\Carbon;
use Mail;
use Hash;



use Auth;

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
    }

    // super admin manage users
    public function navManageUsers(){
        $fbcusers = User::all();

        return view('main-admin.fbc-users.user-management', compact('fbcusers'));
    }

    // super admin add new users
    public function navCreateNewUser(){

        $roles = Role::all();
        $genders = Gender::all();
        return view('main-admin.fbc-users.add-new-user',  compact('roles', 'genders'));
    }

      /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function storeNewUser(Request $request)
    {
        $dt = new \Carbon\Carbon();

            $legal_date = $request->get('dob');
            $before = $dt->subYears(20)->format('Y-m-d');

                $request->validate([
                    'email'=>'required|email|unique:users,email',
                    'password'=>'required|min:8',
                    'fname'=>'required',
                    'mname'=>'required',
                    'lname'=>'required',
                    'dob'=>'required|date|before:' . $before,
                    'gender_id'=>'required',
                    'role_id'=>'required',
                    'job_title'=>'required|unique:users,job_title',
                    'job_desc'=>'required',
                    'phonenumber'=>'required|regex:/^([0-9\s\-\+\(\)]*)$/|min:10',
                    'type_of_employee'=>'required',
                    'acc_status'=>'required',
                    'userPhoto' => 'required|image|mimes:jpg,png,jpeg,gif,svg|min:1|max:2048'
                ],
                [
                    'email.required'    => 'Please Provide an Email Address For the user, Thank You.',
                    'email.unique'      => 'Denied, This emails is already in use, Provide another.',
                    'password.required' => 'Password is Required, Thank You.',
                    'password.min'      => 'Please select a Strong Password, Thank You.',
                    'dob.before'      => 'User should be atleast 20 years of age.',
                    'userPhoto.image'      => 'User Photo should be an image.',
                    'userPhoto.mimes'      => 'File exestion is not supported.',
                    'userPhoto.max'      => 'User photo should be less than 25MB.'


                ]);

                $image_name = Str::random(20);;
                $ext = strtolower($request->file('userPhoto')->getClientOriginalExtension()); // You can use also getClientOriginalName()
                $image_full_name = $image_name.'.'.$ext;
                $upload_path = 'public/img/user-photos/';    //Creating Sub directory in Public folder to put image
                $image_url = $upload_path.$image_full_name;
                $success = $request->file('userPhoto')->move($upload_path,$image_full_name);

                if($success){
                   try {
                    $filePath = $image_url; //Passing $data->image as parameter to our created method
                    $request->userPhoto = $filePath;

                 //dd($request->userPhoto);
                $newuser = new User([
                    'fname' => $request-> get('fname'),
                    'mname' => $request-> get('fname'),
                    'lname' => $request-> get('lname'),
                    'email' => $request-> get('email'),
                    'password' => $request-> get('password'),
                    'dob' => $request-> get('dob'),
                    'gender_id' => $request-> get('gender_id'),
                    'role_id' => $request-> get('role_id'),
                    'job_title' => $request-> get('job_title'),
                    'job_desc' => $request-> get('job_desc'),
                    'phonenumber' => $request-> get('phonenumber'),
                    'type_of_employee' => $request-> get('type_of_employee'),
                    'acc_status' => $request-> get('acc_status'),
                    'created_by' => $request->input('added_by'),
                    'user_photo_id'=>$filePath,
                    'created_at' => \Carbon\Carbon::now(),
                    'last_active'=> \Carbon\Carbon::now()
                ]);

                $newuser->save();
                //send email to user
                $token = Str::random(64);

                DB::table('password_reset')->insert([
                    'email' => $request->email,
                    'token' => $token,
                    'created_at' => Now()
                  ]);

                  // send email link
                Mail::send('email.changePassword', ['token' => $token], function($message) use($request){
                    $message->to($request->email);
                    $message->subject('Reset Password');
                });

                return back()->with('message')->with('success', 'A new user was successfully added!');

               } catch (Exception $e) {
                   //Write your error message here
                   return back()->with('message')->with('failed', 'Missing values!');

               }
            }
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

    public function navManageDevPool(){
        return view('main-admin.careers.dev-pool.manage-engineers');
    }


    public function navCreateDevPoolOppo(){

        return view('main-admin.careers.dev-pool.create-new-job-poster');
    }

    public function storeNewDevPoolOppo(Request $request)
    {
        $dt = new \Carbon\Carbon();
        $request->validate([
            'addedby',
            'category-type',
            'title',
            'company',
            'job-icon',
            'job_desc']);

    }


    public function navManageCareerOppo(){
        return view('main-admin.careers.oppo.manage-careers');
    }
    public function navCreateCareerOppo(){
        return view('main-admin.careers.oppo.create-new-opportunity');
    }

    public function navManageApplicants(){
        return view('main-admin.careers.oppo.applicants.manage-applicants');
    }

    public function navViewFullDetails(){
        return view('main-admin.careers.oppo.applicants.view-applicants-full-details');
    }

}

