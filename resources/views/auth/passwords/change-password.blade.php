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
                          {{-- <input type="hidden" name="token" value="{{ $token }}"> --}}

                            <div class="row">
                                <div class="col-sm-12">
                                    <label for="current-password" class="mb-1">Enter Current Password <span
                                            class="text-danger">*</span></label>
                                    <div class="input-group mb-3">
                                        <input id="current-password" type="current-password" class="form-control {{ $errors->has('new-password') ? ' has-error' : '' }}" aria-label="cureent password" @error('current-password') is-invalid @enderror" name="current-password" required autocomplete="current-password">
                                        @error('current-password')
                                        <span class="invalid-feedback" role="alert">
                                            <strong>{{ $message }}</strong>
                                        </span>
                                       @enderror
                                       @if ($errors->has('current-password'))
                                       <span class="text-danger">{{ $errors->first('current-password') }}</span>
                                   @endif
                                    </div>
                                </div>
                                <div class="col-sm-12">
                                    <label for="password" class="mb-1">New Password <span
                                            class="text-danger">*</span></label>
                                    <div class="input-group mb-3">
                                        <input id="password" type="new-password" class="form-control" aria-label="Password" @error('new-password') is-invalid @enderror" name="new-password" required autocomplete="new-password">
                                        @error('new-password')
                                        <span class="invalid-feedback" role="alert">
                                            <strong>{{ $message }}</strong>
                                        </span>
                                       @enderror
                                       @if ($errors->has('new-password'))
                                       <span class="text-danger">{{ $errors->first('new-password') }}</span>
                                   @endif
                                    </div>
                                </div>
                                <div class="col-sm-12">
                                    <label for="new-confirm-password" class="mb-1">Confirm New Password <span
                                            class="text-danger">*</span></label>
                                    <div class="input-group mb-3">
                                        <input type="password" id="new-password-confirm" class="form-control" aria-label="new-password-confirm" @error('new-password-confirm') is-invalid @enderror" name="new-password-confirmation" required autocomplete>

                                       @if ($errors->has('new-password-confirmation'))
                                       <span class="text-danger">{{ $errors->first('new-password-confirmation') }}</span>
                                       @endif
                                    </div>
                                </div>

                                <div class="col-12">
                                    <button type="submit" class="btn btn-primary mt-3 d-block w-100">
                                        {{ __('change password') }}
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



