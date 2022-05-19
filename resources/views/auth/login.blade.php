@extends('layouts.acr')
@section('content')

        <!--register section start-->
        <section class="sign-up-in-section bg-dark ptb-60" style="background: url('img/page-header-bg.svg')no-repeat right bottom">
            <div class="container">
                <div class="row align-items-center justify-content-center">
                    <div class="col-lg-5 col-md-8 col-12">
                        <a href="{{ url('/') }}" class="mb-4 d-block text-center">
                            <img src="img/fb_og_logo.png" alt="Future Basics" class="img-fluid"></a>
                        <div class="register-wrap p-5 bg-light shadow rounded-custom">
                            <h1 class="h3">Nice to Seeing You Again</h1>
                            <p class="text-muted">Please log in to gain access.</p>

                            {{-- <div class="action-btns">
                                <a href="#" class="btn google-btn bg-white shadow-sm mt-4 d-block d-flex align-items-center text-decoration-none justify-content-center">
                                    <img src="img/google-icon.svg" alt="google" class="me-3">
                                    <span>Connect with Google</span>
                                </a>
                            </div> --}}
                            {{-- <div class="position-relative d-flex align-items-center justify-content-center mt-4 py-4">
                                <span class="divider-bar"></span>
                                <h6 class="position-absolute text-center divider-text bg-light mb-0">Or</h6>
                            </div> --}}
                            <form method="POST" action="{{ route('login') }}" class="mt-4 register-form">
                                @csrf

                                <div class="form-group row">
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
                                <div class="row">

                                    <div class="col-sm-12">
                                        <label for="password" class="mb-1">Password <span
                                                class="text-danger">*</span></label>
                                        <div class="input-group mb-3">
                                            <input id="password" type="password" class="form-control" aria-label="Password" @error('password') is-invalid @enderror" name="password" required autocomplete="current-password">
                                            @error('password')
                                            <span class="invalid-feedback" role="alert">
                                                <strong>{{ $message }}</strong>
                                            </span>
                                           @enderror
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <div class="col-md-6 offset-md-4">
                                            <div class="form-check">
                                                <input class="form-check-input" type="checkbox" name="remember" id="remember" {{ old('remember') ? 'checked' : '' }}>

                                                <label class="form-check-label" for="remember">
                                                    {{ __('Remember Me') }}
                                                </label>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-12">
                                        <button type="submit" class="btn btn-primary mt-3 d-block w-100">
                                            {{ __('Login') }}
                                        </button>
                                    </div>
                                </div>
                                <p class="font-monospace fw-medium text-center text-muted mt-3 pt-4 mb-0">Don’t have an
                                    account? <a href="{{ route('contact-us') }}" class="text-decoration-none">Contact Us</a>
                                    <br>

                                    @if (Route::has('password.request'))
                                    {{-- <a class="btn btn-link" href="{{ route('password.request') }}">
                                        {{ __('Forgot Your Password?') }}
                                    </a> --}}
                                    {{-- <a href="{{ route('password.request') }}" class="text-decoration-none">
                                        Forgot password
                                    </a>
                                     <a class="dropdown-item" href="{{ route('changePasswordGet') }}">Change Password </a>

                                       --}}
                                    @endif
                                </p>
                                <p class="font-monospace fw-medium text-center text-muted mt-3 pt-4 mb-0">Did you forget your password?
                                     <a href="{{ route('forget.password.get') }}" class="text-decoration-none">click here</a>
                                    <br>
                                </p>
                                <p class="font-monospace fw-medium text-center text-muted mt-3 pt-4 mb-0">Did you forget your password?
                                    <a href="{{ route('changePasswordGet') }}" class="text-decoration-none">click here</a>
                                   <br>
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
{{--
@section('content')
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">{{ __('Login') }}</div>

                <div class="card-body">
                    <form method="POST" action="{{ route('login') }}">
                        @csrf

                        <div class="form-group row">
                            <label for="email" class="col-md-4 col-form-label text-md-right">{{ __('E-Mail Address') }}</label>

                            <div class="col-md-6">
                                <input id="email" type="email" class="form-control @error('email') is-invalid @enderror" name="email" value="{{ old('email') }}" required autocomplete="email" autofocus>

                                @error('email')
                                    <span class="invalid-feedback" role="alert">
                                        <strong>{{ $message }}</strong>
                                    </span>
                                @enderror
                            </div>
                        </div>

                        <div class="form-group row">
                            <label for="password" class="col-md-4 col-form-label text-md-right">{{ __('Password') }}</label>

                            <div class="col-md-6">
                                <input id="password" type="password" class="form-control @error('password') is-invalid @enderror" name="password" required autocomplete="current-password">

                                @error('password')
                                    <span class="invalid-feedback" role="alert">
                                        <strong>{{ $message }}</strong>
                                    </span>
                                @enderror
                            </div>
                        </div>

                        <div class="form-group row">
                            <div class="col-md-6 offset-md-4">
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" name="remember" id="remember" {{ old('remember') ? 'checked' : '' }}>

                                    <label class="form-check-label" for="remember">
                                        {{ __('Remember Me') }}
                                    </label>
                                </div>
                            </div>
                        </div>

                        <div class="form-group row mb-0">
                            <div class="col-md-8 offset-md-4">
                                <button type="submit" class="btn btn-primary">
                                    {{ __('Login') }}
                                </button>

                                @if (Route::has('password.request'))
                                    <a class="btn btn-link" href="{{ route('password.request') }}">
                                        {{ __('Forgot Your Password?') }}
                                    </a>
                                @endif
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection --}}
