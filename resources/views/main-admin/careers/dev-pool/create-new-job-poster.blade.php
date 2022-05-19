{{-- @extends('layouts.app') --}}
@extends('layouts.admin-app-layout')
@section('content')
<div class="container-fluid">
    <!--contact us form start-->
    <section class="contact-us-form pt-60 pb-120"
        style="background: url('img/shape/contact-us-bg.svg')no-repeat center bottom">
        <div class="container">
            <br /><br />
            @if (Session::has('success'))
            <div class="alert alert-info" id="alert">{{ Session::get('success') }}
                <button class="close" onclick="document.getElementById('al').style.display='none'">&cross;</button>
            </div>
            @endif
            {{-- @if ($errors->any())
            <div class="alert alert-danger">
                <ul>
                    @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                    @endforeach
                </ul>
            </div>
            @endif --}}

            {{-- start of contact form --}}
            <div class="row justify-content-lg-between align-items-center">
                <div class="col-lg-4 col-lg-8">
                    <div class="section-heading">
                        <h2>Add A New Career Opportunity</h2>
                        <p>We are always available anytime for coffee, a quick chat, phone call or a meeting. just reach
                            out to us and We will contact you.</p>
                    </div>

                    <form action="{{ route('create-new-user') }}" method="POST"  enctype="multipart/form-data" class="register-form">
                        @csrf
                        <div class="row">
                            <div class="col-sm-6">
                                <input type="hidden" value="{{ Auth::user()->user_id }}" id="addedby" name="added_by">

                                <label for="lblfirstName" class="mb-1">First name <span
                                        class="text-danger">*</span></label>
                                <div class="input-group mb-3">
                                    <input type="text" class="form-control" name="fname" id="fname" required
                                    value="{{ old('fname') }}" placeholder="First name" aria-label="First name">
                                    @error('firstName')
                                    <span class="invalid-feedback" role="alert">
                                        <strong>{{ $message }}</strong>
                                    </span>
                                    @enderror
                                </div>
                            </div>
                            <div class="col-sm-6">
                                <label for="lblmiddleName" class="mb-1">Middle name <span
                                        class="text-danger">*</span></label>
                                <div class="input-group mb-3">
                                    <input type="text" class="form-control" name="mname" id="mname" required
                                    value="{{ old('mname') }}" placeholder="Middle name" aria-label="Middle name">
                                    @error('mname')
                                    <span class="invalid-feedback" role="alert">
                                        <strong>{{ $message }}</strong>
                                    </span>
                                    @enderror
                                </div>
                            </div>
                            <div class="col-sm-6 ">
                                <label for="lbllastName" class="mb-1">Last name</label>
                                <div class="input-group mb-3">
                                    <input type="text" class="form-control" name="lname" id="lname" required
                                    value="{{ old('lname') }}" placeholder="Last name" aria-label="Last name">
                                </div>
                            </div>
                            <div class="col-sm-6">
                                <label for="lblphone" class="mb-1">Phone Number <span class="text-danger">*</span></label>
                                <div class="input-group mb-3">
                                    <input type="text" class="form-control" name="phonenumber" id="phonenumber" required
                                    value="{{ old('phonenumber') }}" placeholder="Phone Number" aria-label="Phone">
                                    @error('phonenumber')
                                    <span class="invalid-feedback" role="alert">
                                        <strong>{{ $message }}</strong>
                                    </span>
                                    @enderror
                                </div>
                             </div>
                           </div>

                            <div class="row">
                            <div class="col-sm-6">
                                <label for="email" class="mb-1">Email
                                </label>
                                <div class="input-group mb-3">
                                    <input type="email" class="form-control" name="email" id="email"
                                        @error('email') is-invalid @enderror required value="{{ old('email') }}" placeholder="Email"
                                        aria-label="Email"> @error('email')
                                        <span class="invalid-feedback" role="alert">
                                            <span class="text-danger">*</span>
                                        </span>
                                        @enderror
                                </div>
                            </div>
                          </div>
                          <div class="row">
                            <div class="col-sm-6">
                                <label for="lblpassword" class="mb-1">Password<span class="text-danger">*</span></label>
                                <div class="input-group mb-3">
                                    <input type="text" class="form-control" name="password" id="password" required
                                        placeholder="Password" aria-label="Password">
                                    @error('password')
                                    <span class="invalid-feedback" role="alert">
                                        <strong>{{ $message }}</strong>
                                    </span>
                                    @enderror
                                </div>
                            </div>
                        </div>

                            <div class="row">
                                <div class="col-sm-6">
                                    <button type="submit" name="submit" value="submit"
                                        class="btn btn-primary mt-4">Create New User</button>
                                </div>

                            </div>

                        </div>
                    </form>
                </div>
            </div>
        </div>
    </section>
    <!--contact us form end-->

</div>
    @endsection
