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
