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
             'email' => 'required|email',
             'subject' => 'required',
             'phone' => 'required',
             'message' => 'required'
         ]);

        //  $contact = new Contact;
        //  $contact->fname = $request->firstName;
        //  $contact->lname = $request->lastName;
        //  $contact->email = $request->email;
        //  $contact->subject = $request->subject;
        //  $contact->phone_number = $request->phone;
        //  $contact->message = $request->message;


         $contact = new Contact([
            'fname' => $request->firstName,
            'lname' => $request->lastName,
            'email'=>$request->email,
            'subject' => $request->subject,
            'phone_number' => $request->phone,
            'message' => $request->message
        ]);
         $contact->save();

        Mail::send('contact-us',
        array(
            'fname' => $request->firstName,
            'email' => $request->email,
            'subject' => $request->subject,
            'phone_number' =>$request->phone,
            'user_message' =>  $request->message
        ), function($message) use ($request)
          {
             $message->from($request->email);
             $message->to('info@futurebasics.co.tz');
          });
         return back()->with('success', 'Thank you for contacting us!');

     }
 }
