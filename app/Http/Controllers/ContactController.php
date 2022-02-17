<?php

namespace App\Http\Controllers;
use Illuminate\Http\Request;
use App\Models\Contact;
use Mail;


class ContactController extends Controller
{
    public function getContact() {

        return view('contact-us');
      }

       public function saveContact(Request $request) {

         $this->validate($request, [
             'firstName' => 'required',
             'lastName' => 'required',
             'contactemail' => 'required|email',
             'subject' => 'required',
             'phone' => 'required',
             'message' => 'required'
         ]);

        //  save contact to db
         $contact = new Contact([
            'fname' => $request->firstName,
            'lname' => $request->lastName,
            'contactemail'=>$request->contactemail,
            'subject' => $request->subject,
            'phone_number' => $request->phone,
            'message' => $request->message
        ]);
         $contact->save();

        Mail::send('contact-us',
        array(
            'fname' => $request->firstName,
            'email' => $request->contactemail,
            'subject' => $request->subject,
            'phone_number' =>$request->phone,
            'user_message' =>  $request->message
        ), function($message) use ($request)
          {
             $message->from($request->contactemail);
             $message->to('info@futurebasics.co.tz');
          });
         return back()->with('success', 'Thank you for contacting us!');

     }
 }
