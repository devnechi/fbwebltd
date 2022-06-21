{{-- @extends('layouts.app') --}}
@extends('layouts.admin-app-layout')
@section('content')
<div class="container">
  <!--contact us form start-->
  <section class="contact-us-form pt-60 pb-120" style="background: url('img/shape/contact-us-bg.svg')no-repeat center bottom">
    <div class="container">


  <!--feature tab section start-->
  <section class="feature-tab-section bg-light">
    <div class="container">

        <div class="row">
            <div class="col-12">
                <ul class="nav feature-tab-list-2 mt-4" id="nav-tab-2" role="tablist">
                    <li class="nav-item">
                        <a class="nav-link active" href="#tab-2-1" data-bs-toggle="tab" data-bs-target="#tab-2-1" role="tab" aria-selected="false">
                          applicants
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#tab-2-2" data-bs-toggle="tab" data-bs-target="#tab-2-2" role="tab" aria-selected="false">
                           pool categories
                        </a>
                    </li>
                    {{-- <li class="nav-item">
                        <a class="nav-link" href="#tab-2-3" data-bs-toggle="tab" data-bs-target="#tab-2-3" role="tab" aria-selected="false">
                            Data Mining and Analytics
                        </a>
                    </li> --}}
                </ul>
                <div class="tab-content" id="nav-tabContent-2">
                    <div class="tab-pane fade pt-60 active show" id="tab-2-1" role="tabpanel">
                        <div class="row justify-content-center align-items-center justify-content-around">
                            <div class="col-lg-12">
                                <div class="row justify-content-lg-between align-items-center">
                                    <div class="col-lg-12 col-md-8">
                                        <div class="section-heading">
                                            <h2>Potential applicants</h2>
                                            <p>Applicants who might be shortlisted foe future FBC projects.</p>
                                        </div>

                                          <h1>developers</h1>
                                          <table class="table">
                                            <thead>
                                              <tr>
                                                <th scope="col">#</th>
                                                <th scope="col">First</th>
                                                <th scope="col">Last</th>
                                                <th scope="col">Handle</th>
                                              </tr>
                                            </thead>
                                            <tbody>
                                              <tr>
                                                <th scope="row">1</th>
                                                <td>Mark</td>
                                                <td>Otto</td>
                                                <td>@mdo</td>
                                              </tr>
                                              <tr>
                                                <th scope="row">2</th>
                                                <td>Jacob</td>
                                                <td>Thornton</td>
                                                <td>@fat</td>
                                              </tr>
                                              <tr>
                                                <th scope="row">3</th>
                                                <td colspan="2">Larry the Bird</td>
                                                <td>@twitter</td>
                                              </tr>
                                            </tbody>
                                          </table>
                                    </div>
                                </div>
                            </div>

                        </div>
                    </div>
                    <div class="tab-pane fade pt-60" id="tab-2-2" role="tabpanel">
                        <div class="row justify-content-center align-items-center justify-content-around">

                            <div class="col-lg-12">
                                <div class="col-lg-12 col-md-8">
                                    <div class="section-heading">
                                        <h2>pool categories</h2>
                                        <p>We are always available anytime for coffee, a quick chat, phone call or a meeting. just reach out to us and We will contact you.</p>
                                    </div>

                                    <a href="{{ route('create-new-dev-pool-opportunity') }}" class="btn btn-primary">Add </a>
                                    </div>
                                    <br />
                                    {{-- <div class="clearfix"></div> --}}
                                    <table class="table">
                                        <thead>
                                          <tr>
                                            <th scope="col">#</th>
                                            <th scope="col">Image</th>
                                            <th scope="col">Title</th>
                                            <th scope="col">Category</th>
                                            <th scope="col">Short Description</th>
                                            <th scope="col">Date created</th>
                                            <th scope="col">Date updated</th>
                                          </tr>
                                        </thead>
                                        <tbody>
                                          <tr>
                                            <th scope="row">1</th>
                                            <td>Mark</td>
                                            <td>Otto</td>
                                            <td>Mark</td>
                                            <td>Otto</td>
                                            <td>@mdo</td>
                                          </tr>
                                          <tr>
                                            <th scope="row">2</th>
                                            <td>Jacob</td>
                                            <td>Thornton</td>
                                            <td>Mark</td>
                                            <td>Otto</td>
                                            <td>@fat</td>
                                          </tr>
                                          <tr>
                                            <th scope="row">3</th>
                                            <td colspan="2">Larry the Bird</td>
                                            <td>Mark</td>
                                            <td>Otto</td>
                                            <td>@twitter</td>
                                          </tr>
                                        </tbody>
                                      </table>
                                </div>
                            </div>
                        </div>
                    </div>
                    {{-- <div class="tab-pane fade pt-60" id="tab-2-3" role="tabpanel">
                        <div class="row justify-content-center align-items-center justify-content-around">
                            <div class="col-lg-12">
                                <div class="feature-tab-info">
                                    <div class="container">
                                        <div class="row align-items-center justify-content-between">
                                            <div class="col-lg-4 col-md-12">
                                                <div class="section-heading">
                                                    <h5 class="h6 text-primary">Developers</h5>
                                                    <h2>Opportunities for Developers, programmers and Software Engineers</h2>
                                                </div>
                                            </div>
                                            <div class="col-lg-7 col-md-12">
                                                <div class="text-end">
                                                    <a href="{{ route('developers-info-entery-form') }}" class="btn btn-primary">Join Our Developer Pool</a>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-lg-4 col-md-6">
                                                <a href="{{ route('developers-info-entery-form') }}" class="position-relative text-decoration-none connected-app-single bg-white border border-2 promo-border-hover bg-white mt-4 transition-base rounded-custom d-block overflow-hidden p-5">
                                                    <div class="position-relative connected-app-content">
                                                        <div class="integration-logo bg-white rounded-circle shadow-lg p-2 d-inline-block">
                                                            <img src="img/integations/1.png" width="40" alt="integration" class="img-fluid">
                                                        </div>
                                                        <h5>Data Science</h5>
                                                        <p class="mb-0 text-muted">Be shortlisted for data science opportunities with us.</p>
                                                    </div>
                                                </a>
                                            </div>


                                        </div>
                                    </div>
                                </div>
                            </div>

                        </div>
                    </div> --}}
                </div>
            </div>
        </div>
    </div>
</section>
<!--feature tab section end-->

    </div>
</section>
<!--contact us form end-->
@endsection
