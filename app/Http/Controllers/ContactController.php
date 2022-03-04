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

      /**
         * The response to always send back to the frontend
         *
         * @return \Illuminate\Http\Response
         */
        protected function formResponse()
        {

            return redirect()->back()
            ->withSuccess('Email sent');

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

         if ($request->faxonly) {
            return $this->formResponse();
        }else{

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

        Mail::send('email.email',
        [
            'fname' => $request->firstName,
            'contactemail' => $request->contactemail,
            'subject' => $request->subject,
            'phone_number' =>$request->phone,
            'user_message' =>  $request->message
        ], function($message)
          {
             $message->from('info@futurebasics.co.tz', 'Future Basics Website');
             $message->to('info@futurebasics.co.tz', 'Future Basics Company')
                     ->subject('New Contact');
          });
         return back()->with('success', 'Thank you! for contacting us, We will get back to you soon!');

        }

     }
 }
