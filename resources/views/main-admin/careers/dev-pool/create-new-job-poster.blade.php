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
                        <h2>Add A Talent Pool Opportunity</h2>
                        <p>We are always available anytime for coffee, a quick chat, phone call or a meeting. just reach
                            out to us and We will contact you.</p>
                    </div>

                    <form action="{{ route('submit-new-career-opportunity') }}" method="POST"  enctype="multipart/form-data" class="register-form">
                        @csrf
                        <div class="row">
                            <div class="col-sm-6">
                                <input type="hidden" value="{{ Auth::user()->user_id }}" id="addedby" name="added_by">
                                <label for="category-type" class="mb-1">Talent Type <span class="text-danger">*</span></label>
                                <div class="input-group mb-3">
                                    <select class="form-select"  value="{{ old('category-type') }}" name="category-type" aria-label="Default select example">
                                        <option selected>Select Type</option>
                                        <option value="design">Designers & Digital Strategies</option>
                                        <option value="se">Engineering and Development</option>
                                        <option value="ds">Data Mining and Analytics</option></option>
                                      </select>
                                </div>
                            </div>
                        </div>
                    <div class="row">
                        <div class="col-sm-6">
                            <label for="title" class="mb-1">Title <span class="text-danger">*</span></label>
                            <div class="input-group mb-3">
                                <input type="text" class="form-control" name="title" id="title" required
                                    value="{{ old('title') }}" placeholder="Talent Pool Title"
                                    aria-label="Talent Pool Title">
                                @error('firstName')
                                <span class="invalid-feedback" role="alert">
                                    <strong>{{ $message }}</strong>
                                </span>
                                @enderror
                            </div>
                            <input type="hidden" value="Future Basics" id="company" name="fbc-company">
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-sm-6">
                            <div class="mb-3">
                                <label for="job-icon" class="form-label">Upload Job Icon</label>
                                <p>*please add a 25 mb file with extensions of .jpg, .jpeg or .png</p>
                                <input class="form-control" value="{{ old('job-icon') }}" name="job-icon" type="file"
                                    id="job-icon">
                            </div>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col-lg-12">
                            <label for="job_desc" class="mb-1">Short Description <span
                                    class="text-danger">*</span></label>
                            <div class="input-group mb-3">
                                <textarea class="form-control" value="{{ old('job_desc') }}" name="job_desc"
                                    id="job_desc" rows="4"></textarea>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-sm-6">
                            <button type="submit" name="submit" value="submit" class="btn btn-primary mt-4">create new
                                poster</button>
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
