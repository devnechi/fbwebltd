@extends('layouts.acr')
@section('content')

<!--main content wrapper start-->
<div class="main-wrapper">
    <!--register section start-->
    <section class="sign-up-in-section bg-dark ptb-60" style="background: url('img/page-header-bg.svg')no-repeat right bottom">
        <div class="container">
            <div class="row align-items-center justify-content-center">
                <div class="col-lg-5 col-md-8 col-12">
                    {{-- <a href="{{ url('/') }}" class="mb-4 d-block text-center">
                        <img src="public/img/fb_og_logo.png" alt="logo" class="img-fluid">
                    </a> --}}
                    <div class="register-wrap p-5 bg-light shadow rounded-custom">
                        <h1 class="fw-bold h3">Change Password</h1>
                        <p class="text-muted">Change your password..</p>

                            {{-- @if (Session::has('message'))
                            <div class="alert alert-success" role="alert">
                               {{ Session::get('message') }}
                           </div>
                       @endif --}}

                                @if (session('error'))
                                <div class="alert alert-danger">
                                    {{ session('error') }}
                                </div>
                            @endif
                            @if (session('success'))
                                <div class="alert alert-success">
                                    {{ session('success') }}
                                </div>
                            @endif
                            @if($errors)
                                @foreach ($errors->all() as $error)
                                    <div class="alert alert-danger">{{ $error }}</div>
                                @endforeach
                            @endif
                        <form action="{{ route('changePasswordPost') }}" class="mt-5 register-form" method="POST">
                            @csrf
                          <input type="hidden" name="token" value="{{ $token }}">

                            <div class="row">
                                <div class="col-sm-12">
                                    <label for="email" class="mb-1">Your Email <span class="text-danger">*</span></label>
                                    <div class="input-group mb-3">
                                        <input id="email" type="email" name="email" class="form-control @error('email') is-invalid @enderror" value="{{ old('email') }}" required autocomplete="email" autofocus>
                                        @error('email')
                                            <span class="invalid-feedback" role="alert">
                                                <strong>{{ $message }}</strong>
                                            </span>
                                        @enderror
                                    @if ($errors->has('email'))
                                    <span class="text-danger">{{ $errors->first('email') }}</span>
                                      @endif
                                    </div>
                                </div>
                                <div class="col-sm-12">
                                    <label for="current-password" class="mb-1">Your Enter Current Password <span
                                            class="text-danger">*</span></label>
                                    <div class="input-group mb-3">
                                        <input id="current_password" type="password" class="form-control {{ $errors->has('new-password') ? ' has-error' : '' }}" aria-label="cureent password" @error('current-password') is-invalid @enderror" name="current_password" required autocomplete="current-password">
                                        @error('current_password')
                                        <span class="invalid-feedback" role="alert">
                                            <strong>{{ $message }}</strong>
                                        </span>
                                       @enderror
                                       @if ($errors->has('current_password'))
                                       <span class="text-danger">{{ $errors->first('current_password') }}</span>
                                   @endif
                                    </div>
                                </div>
                                <div class="col-sm-12">
                                    <p>New password entry</p>
                                    <label for="password" class="mb-1">New Password <span
                                            class="text-danger">*</span></label>
                                    <div class="input-group mb-3">
                                        <input id="password" type="password" class="form-control" aria-label="Password" @error('password') is-invalid @enderror" name="password" required autocomplete="password">
                                        @error('password')
                                        <span class="invalid-feedback" role="alert">
                                            <strong>{{ $message }}</strong>
                                        </span>
                                       @enderror
                                       @if ($errors->has('password'))
                                       <span class="text-danger">{{ $errors->first('password') }}</span>
                                   @endif
                                    </div>
                                </div>
                                <div class="col-sm-12">
                                    <label for="new-confirm-password" class="mb-1">Confirm New Password <span
                                            class="text-danger">*</span></label>
                                    <div class="input-group mb-3">
                                        <input type="password" id="confirm_pass" class="form-control" aria-label="confirm_pass" @error('confirm_pass') is-invalid @enderror" name="confirm_pass" required autocomplete>

                                       @if ($errors->has('confirm_pass'))
                                       <span class="text-danger">{{ $errors->first('confirm_pass') }}</span>
                                       @endif
                                    </div>
                                </div>

                                <div class="col-12">
                                    <button type="submit" class="btn btn-primary mt-3 d-block w-100">
                                        {{ __('change password') }}
                                    </button>
                                </div>
                            </div>
                            {{-- <p class="font-monospace fw-medium text-center mt-3 pt-4 mb-0">
                                <a href="{{ route('login') }}" class="text-decoration-none">Back to login page</a>
                            </p> --}}
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!--register section end-->
</div>
@endsection



