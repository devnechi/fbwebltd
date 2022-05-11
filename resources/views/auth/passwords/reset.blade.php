@extends('layouts.acr')
@section('content')

<!--main content wrapper start-->
<div class="main-wrapper">
    <!--register section start-->
    <section class="sign-up-in-section bg-dark ptb-60" style="background: url('img/page-header-bg.svg')no-repeat right bottom">
        <div class="container">
            <div class="row align-items-center justify-content-center">
                <div class="col-lg-5 col-md-8 col-12">
                    <a href="{{ url('/') }}" class="mb-4 d-block text-center"><img src="img/fb_og_logo.png" alt="logo" class="img-fluid"></a>
                    <div class="register-wrap p-5 bg-light shadow rounded-custom">
                        <h1 class="fw-bold h3">Forgot your Password?</h1>
                        <p class="text-muted">Don't worry. Type your email and we will send a password recovery link to
                            your email..</p>

                            @if (Session::has('message'))
                            <div class="alert alert-success" role="alert">
                               {{ Session::get('message') }}
                           </div>
                       @endif

                        <form action="{{ route('forget.password.post') }}" class="mt-5 register-form" method="POST">
                            @csrf
                            <div class="row">
                                <div class="col-sm-12">
                                    <label for="email" class="col-md-4 col-form-label text-md-right">{{ __('E-Mail Address') }}</label>
                                    <div class="col-lg-12">
                                        <input id="email" type="email" name="email" class="form-control @error('email') is-invalid @enderror" value="{{ old('email') }}" required autocomplete="email" autofocus>
                                        @error('email')
                                            <span class="invalid-feedback" role="alert">
                                                <strong>{{ $message }}</strong>
                                            </span>
                                        @enderror
                                    </div>
                                </div>
                                <div class="col-12">
                                    <button type="submit" class="btn btn-primary mt-3 d-block w-100">
                                        {{ __('Send Password reset link') }}
                                    </button>
                                </div>
                            </div>
                            <p class="font-monospace fw-medium text-center mt-3 pt-4 mb-0">
                                <a href="{{ route('login') }}" class="text-decoration-none">Back to login page</a>
                            </p>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!--register section end-->
</div>
@endsection



