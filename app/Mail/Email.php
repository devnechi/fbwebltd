<?php

namespace App\Mail;

// use GuzzleHttp\Psr7\Request;
use Illuminate\Bus\Queueable;
use Illuminate\Http\Request;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Mail\Mailable;
use Illuminate\Queue\SerializesModels;

class Email extends Mailable
{
    use Queueable, SerializesModels;
    public $email;

    /**
     * Create a new message instance.
     *
     * @return void
     */
    public function __construct(Request $request)
    {
        //
        // $this->data = $data;
        // $this->subject = $data['subject'];
        $this->email = $request;
    }

    /**
     * Build the message.
     *
     * @return $this
     */
    public function build()
    {
        // return $this->view('view.name');
        // return $this->subject($this->subject)
        //             ->view('contact-us')
        //             ->with('email',$this->email);

        return $this->firstName($this->firstName)
                    ->lastName($this->lastName)
                    ->phone($this->phone)
                    ->from($this->email)
                    ->subject($this->subject)
                    ->to('info@futurebasics.co.tz')
                    ->view('contact-us')
                    ->with('email',$this->email);
    }
}
