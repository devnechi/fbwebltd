<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use App\Providers\RouteServiceProvider;
use Illuminate\Foundation\Auth\ResetsPasswords;
use Illuminate\Http\Request;
use DB;
use Carbon\Carbon;
use App\Models\User;
use Mail;
use Hash;
use Illuminate\Support\Str;
use Illuminate\Support\Facades\Input;


use Auth;

class ResetPasswordController extends Controller
{
    /*
    |--------------------------------------------------------------------------
    | Password Reset Controller
    |--------------------------------------------------------------------------
    |
    | This controller is responsible for handling password reset requests
    | and uses a simple trait to include this behavior. You're free to
    | explore this trait and override any methods you wish to tweak.
    |
    */

    use ResetsPasswords;

    /**
     * Where to redirect users after resetting their password.
     *
     * @var string
     */
    protected $redirectTo = RouteServiceProvider::HOME;
    /**
       * Write code on Method
       *
       * @return response()
       */
      public function submitForgetPasswordForm(Request $request)
      {
          $request->validate([
              'email' => 'required|email|exists:users',
          ]);

           $token = Str::random(64);

          DB::table('password_reset')->insert([
              'email' => $request->email,
              'token' => $token,
              'created_at' => Now()
            ]);

            // send email link
          Mail::send('email.forgetPassword', ['token' => $token], function($message) use($request){
              $message->to($request->email);
              $message->subject('Reset Password');
          });

           return back()->with('message', 'We have e-mailed your password a reset link!');
        //dd(Auth::user()->role_id);
      }

      /**
       * Write code on Method to submit new password
       *
       * @return response()
       */
      public function submitResetPasswordForm(Request $request)
      {
          $request->validate([
              'email' => 'required|email|exists:users',
              'password' => 'required|string|min:6|confirmed',
              'password_confirmation' => 'required'
          ]);

          $updatePassword = DB::table('password_reset')
                              ->where([
                                'email' => $request->email,
                                'token' => $request->token
                              ])
                              ->first();

          if(!$updatePassword){
              return back()->withInput()->with('error', 'Invalid token!');
          }

          $user = User::where('email', $request->email)
                      ->update(['password' => Hash::make($request->password),
                                'email_verified_at' => Now(),
                                'updated_at' => Now()]);

          DB::table('password_reset')->where(['email'=> $request->email])->delete();

          return redirect('/login')->with('message', 'Your password has been changed!');
      }

      /**
       * Write code on Method to submit new password
       *
       * @return response()
       */
      public function submitChangePasswordForm(Request $request)
      {
          $request->validate([
              'email' => 'required|email|exists:users',
              'current_password' => 'required',
              'password' => 'required|string|min:6|confirmed',
              'password_confirmation' => 'required'
          ]);

          $updatePassword = DB::table('password_reset')
                              ->where([
                                'email' => $request->email,
                                'token' => $request->token
                              ])
                              ->first();

          if(!$updatePassword){
              return back()->withInput()->with('error', 'Invalid token!');
          }

          $user = User::where('email', $request->email)
                      ->update([
                      'password' => Hash::make($request->password),
                      'email_verified_at' => Now(),
                      'updated_at' => Now()
                    ]);

          DB::table('password_reset')->where(['email'=> $request->email])->delete();

          return redirect('/login')->with('message', 'Your password has been changed!');
      }

       /**
       * Write code on Method to submit new password
       *
       * @return response()
       */
      public function showChangePasswordGet() {
        return view('auth.passwords.change-password');
    }

    public function changePasswordPost(Request $request) {
        // if (!(Hash::check($request->get('current_password'), Auth::user()->password))) {
            // if (!(Hash::check(User::where('password', '=', $request->current_password))->exists())) {

        $validatedData = $request->validate([
            'current_password' => 'required',
            'password' => 'required|string|min:8|confirmed',
        ]);
        $pass = $request->get('password');

        //dd($pass);

        if (password_verify('password', $request->current_password)) {
                //User::where('email', '=', Input::get('email'))->exists()
            // The passwords matches
            return redirect()->back()->with("error","Your current password does not matches with the registered password.");
        }

        if(strcmp($request->get('current_password'), $request->get('password')) == 0){
            // Current password and new password same
            return redirect()->back()->with("error","New Password cannot be same as your current password.");
        }

        //Change Password
        $user = Auth::user();
        // $user->password = bcrypt($pass);
        $user = User::where('email', $request->email)
        ->update([
        'password' => Hash::make($request->password),
        'email_verified_at' => Now(),
        'updated_at' => Now()
      ]);
       // $user->save();
        DB::table('password_reset')->where(['email'=> $request->email])->delete();
        // return redirect()->back()->with("success","Password successfully changed!");
        return redirect('/login')->with('message', 'Your account has been verified!');
    }


}
