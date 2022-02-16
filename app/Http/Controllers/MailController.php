<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Mail\Email;
use Mail;
use File;

class MailController extends Controller
{
    public function mailsend(){

        return view('contact-us');

     }
     public function sendmail(Request $request){

       $request->validate([
                 'firstName'=> 'required',
                 'lastName'=> 'required',
                 'phone'=> 'required',
                 'subject'=> 'required',
                 'message'=>'required',
                 'email'=>'required',
                ]);
       //dd($request);
       $data = array(
         'subject' => $request->subject,
         'message'=> $request->message,
          );
         Mail::to($request->email)->send(new Email($data));
         return back()->with('success', 'Sent Successfully !');

        }
    }
