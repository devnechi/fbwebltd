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
                        <h1 class="fw-bold h3">Create New Password</h1>
                        <p class="text-muted">Enter your new password..</p>

                            @if (Session::has('message'))
                            <div class="alert alert-success" role="alert">
                               {{ Session::get('message') }}
                           </div>
                       @endif

                        <form action="{{ route('reset.password.post') }}" class="mt-5 register-form" method="POST">
                            @csrf
                          <input type="hidden" name="token" value="{{ $token }}">

                            <div class="row">
                                <div class="col-sm-12">
                                    <label for="email" class="mb-1">Email <span class="text-danger">*</span></label>
                                    <div class="input-group mb-3">
                                        <input type="email" class="form-control @error('email') is-invalid @enderror" placeholder="Email" id="email" required aria-label="email" value="{{ old('email') }}" required autocomplete="email" autofocus>
                                        @error('email')
                                        <span class="invalid-feedback" role="alert">
                                            <strong>{{ $message }}</strong>
                                        </span>
                                    @enderror
                                    </div>
                                </div>
                                <div class="col-sm-12">
                                    <label for="password" class="mb-1">Password <span
                                            class="text-danger">*</span></label>
                                    <div class="input-group mb-3">
                                        <input type="password" class="form-control" aria-label="Password" @error('password') is-invalid @enderror" name="password" required autocomplete="current-password">
                                        @error('password')
                                        <span class="invalid-feedback" role="alert">
                                            <strong>{{ $message }}</strong>
                                        </span>
                                       @enderror
                                    </div>
                                </div>
                                <div class="col-sm-12">
                                    <label for="password" class="mb-1">Confirm password <span
                                            class="text-danger">*</span></label>
                                    <div class="input-group mb-3">
                                        <input type="password" id="password-confirm" class="form-control" aria-label="Password-confirm" @error('password-confirm') is-invalid @enderror" name="password-confirm" required autocomplete>
                                        @error('password')
                                        <span class="invalid-feedback" role="alert">
                                            <strong>{{ $message }}</strong>
                                        </span>
                                       @enderror
                                    </div>
                                </div>

                                <div class="col-12">
                                    <button type="submit" class="btn btn-primary mt-3 d-block w-100">
                                        {{ __('Reset password') }}
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



