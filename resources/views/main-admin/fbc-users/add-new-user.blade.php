{{-- @extends('layouts.app') --}}
@extends('layouts.admin-app-layout')
@section('content')
<div class="container-fluid">
  <!--contact us form start-->
  <section class="contact-us-form pt-60 pb-120" style="background: url('img/shape/contact-us-bg.svg')no-repeat center bottom">
    <div class="container">
        <br/><br/>
        @if (Session::has('success'))
                <div class="alert alert-info" id="al">{{ Session::get('success') }}
                  <button class="close" onclick="document.getElementById('al').style.display='none'" >&cross;</button>
                </div>
        @endif
        @if ($errors->any())
        <div class="alert alert-danger">
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
        {{-- start of contact form --}}
      @endif
        <div class="row justify-content-lg-between align-items-center">
            <div class="col-lg-6 col-md-8">
                <div class="section-heading">
                    <h2>Talk to Our Support and Customer service Department Team</h2>
                    <p>We are always available anytime for coffee, a quick chat, phone call or a meeting. just reach out to us and We will contact you.</p>
                </div>

                <form action="{{ route('contact-em') }}" method="post" class="register-form">
                    @csrf
                    <div class="row">
                        <div class="col-sm-6">
                            <label for="firstName" class="mb-1">First name <span
                                    class="text-danger">*</span></label>
                            <div class="input-group mb-3">
                                <input type="text" class="form-control" name="firstName" id="firstName" required placeholder="First name" aria-label="First name">
                                @error('firstName')
                                <span class="invalid-feedback" role="alert">
                                    <strong>{{ $message }}</strong>
                                </span>
                            @enderror
                            </div>
                        </div>
                        <div class="col-sm-6 ">
                            <label for="lastName" class="mb-1">Last name</label>
                            <div class="input-group mb-3">
                                <input type="text" class="form-control" name="lastName" id="lastName" required placeholder="Last name" aria-label="Last name">
                            </div>
                        </div>
                        <div class="col-sm-6">
                            <label for="phone" class="mb-1">Phone <span class="text-danger">*</span></label>
                            <div class="input-group mb-3">
                                <input type="text" class="form-control" name="phone" id="phone" required placeholder="Phone" aria-label="Phone">
                                @error('phone')
                                <span class="invalid-feedback" role="alert">
                                    <strong>{{ $message }}</strong>
                                </span>
                            @enderror
                            </div>
                        </div>
                       <div class="row">
                        <div class="col-sm-6 ">
                            <label for="subject" class="mb-1">Subject</label>
                            <div class="input-group mb-3">
                                <input type="text" class="form-control"  id="subject" name="subject" placeholder="Subject" aria-label="Subject">
                                @error('subject')
                                <span class="invalid-feedback" role="alert">
                                    <strong>{{ $message }}</strong>
                                </span>
                            @enderror
                            </div>
                        </div>
                    </div>
                        <div class="col-sm-6">
                            <label for="contactemail" class="mb-1">Email
                                @error('contactemail')
                                <span class="invalid-feedback" role="alert">
                                    <span class="text-danger">*</span>
                                </span>
                            @enderror
                            </label>
                            <div class="input-group mb-3">
                                <input type="email" class="form-control" name="contactemail" id="contactemail" @error('contactemail') is-invalid @enderror required placeholder="Email" aria-label="Email">
                            </div>
                        </div>
                        <div class="col-12">
                            <label for="yourMessage" class="mb-1">Message <span class="text-danger">*</span></label>
                            <div class="input-group mb-3">
                                <textarea class="form-control" name="message" id="message" required placeholder="How can we help you?" style="height: 160px"></textarea>
                                @error('message')
                                <span class="invalid-feedback" role="alert">
                                    <strong>{{ $message }}</strong>
                                </span>
                            @enderror
                            </div>
                        </div>

                        <div class="col-sm-6">
                            {{-- @if(config('services.recaptcha.key'))
                            <div class="g-recaptcha"
                                data-sitekey="{{config('services.recaptcha.key')}}">
                            </div>
                        @endif --}}
                        {{-- <div class="form-group">
                            <strong>Just making sure you are not a robot :</strong>
                            {!! NoCaptcha::renderJs() !!}
                            {!! NoCaptcha::display() !!}
                         </div>
                        </div> --}}
                        <div class="form-group{{ $errors->has('g-recaptcha-response') ? ' has-error' : '' }}">
                            <div class="col-md-6">
                                {!! RecaptchaV3::field('contactfbc') !!}
                                @if ($errors->has('g-recaptcha-response'))
                                    <span class="help-block">
                                        <strong>{{ $errors->first('g-recaptcha-response') }}</strong>
                                    </span>
                                @endif
                            </div>
                        </div>
                    </div>
                        <div class="col-sm-6">
                            <div class="form-group" style="display: none;">
                                <label for="simpfill">not to fill
                                 <input type="checkbox" name="simpfill" id="simpfill" />
                                </label>
                               </div>
                        </div>
                    </div>
                    <button type="submit" name="submit" value="submit" class="btn btn-primary mt-4">Get in Touch</button>
                </form>
            </div>
            <div class="col-lg-5 col-md-10">
                {{-- <div class="contact-us-img">
                    <img src="img/contact-us-img-2.svg" alt="contact us" class="img-fluid">
                </div> --}}
            </div>
        </div>
    </div>
</section>
<!--contact us form end-->
@endsection
