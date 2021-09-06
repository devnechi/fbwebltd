@extends('layouts.public_layout')
@section('content')
    <div class="view"
        style="background-image: url('../img/businesss.jpg'); background-repeat: no-repeat; background-size: cover; background-position: center center; height: 740px;">
        <!-- Mask & flexbox options-->
        <div class="mask rgba-gradient align-items-center">
            <!-- Content -->
            <div class="container">
                <!--Grid row-->
                <div class="row">
                    <!--Grid column-->
                    <div class="col-md-6 white-text text-center text-md-left mt-xl-5 mb-5 wow fadeInLeft"
                        data-wow-delay="0.3s">
                        <h1 class="h1-responsive font-weight-bold mt-sm-5"
                            style="color:rgb(216, 216, 29);  padding-top: 40px;">Simplified</h1>
                        <h1 class="h1-responsive font-weight-bold mt-sm-5" style="margin-top: 0rem !important;">Business & Enterprise
                            Solutions</h1>
                    </div>
                    <!--Grid column-->
                    <!--Grid column-->
                    <div class="col-md-6 white-text text-center text-md-left mt-xl-5 mb-5 wow fadeInRight"
                        data-wow-delay="0.3s" style="padding-top: 40px;">
                    </div>
                    <!--Grid column-->
                </div>
                <!--Grid row-->
            </div>
            <!-- Content -->
        </div>
        <!-- Mask & flexbox options-->
    </div>

    <section id="except-intro">
        <div class="container">
            <div class="row">
                <div class="heading titleintro wow fadeInUp">
                    <h2>Find Better Solutions: Build A Better Future</h2>
                    <p style="font-size: 24px;">We venture in areas that show great potential and extract value from
                        them. Our mission is to blend creativity with technology excellence to bring value and meaning
                        to life endevours. We make our customers' steps to the future easier, smarter and valuable. </p>
                </div>
            </div>

        </div>
    </section>
    <section id="business-panels">
        <div class="container">
            <br />
            <br />
             <div class="row">
                 <div class="col-lg-12">
                    <ul class="nav nav-tabs" id="myTab" role="tablist">
                        <li class="nav-item">
                          <a class="nav-link active" id="home-tab" data-toggle="tab" href="#home" role="tab" aria-controls="home"
                            aria-selected="true">Business</a>
                        </li>
                        <li class="nav-item">
                          <a class="nav-link" id="profile-tab" data-toggle="tab" href="#profile" role="tab" aria-controls="profile"
                            aria-selected="false">Enterprises</a>
                        </li>
                      </ul>
                      <div class="tab-content" id="myTabContent">
                            <div class="tab-pane show active" id="home" role="tabpanel" aria-labelledby="home-tab">
                                <br />
                                <br />
                                <div class="row">
                                    <div class="col-md-4 ">
                                        <div class="card">
                                            <img src="https://mdbootstrap.com/img/Mockups/Lightbox/Thumbnail/img%20(67).jpg" alt="Avatar" style="width:100%">

                                        </div>
                                    </div>
                                    <div class="col-md-8">
                                        <h2 class="h1-responsive font-weight-bold mt-sm-5">Wakala +</h2>
                                        <br />
                                        <p style="font-size: 24px;">We venture in areas that show great potential and extract value from
                                            them. Our mission is</p>
                                    </div>
                                </div>
                            </div>
                            <div class="tab-pane fade" id="profile" role="tabpanel" aria-labelledby="profile-tab">
                                <br />
                                <br />
                                <div class="row">
                                    <div class="col-md-4 ">
                                        <div class="card">
                                            <img src="https://mdbootstrap.com/img/Mockups/Lightbox/Thumbnail/img%20(67).jpg" alt="Avatar" style="width:100%">

                                        </div>
                                    </div>
                                    <div class="col-md-8">
                                        <h2 class="h1-responsive font-weight-bold mt-sm-5">Smart Risiti</h2>
                                        <br />
                                        <p style="font-size: 24px;">We venture in areas that show great potential and extract value from
                                            them. Our mission is</p>
                                    </div>
                                </div>
                            </div>
                      </div>
                </div>
             </div>

        </div>
    </section>
    @endsection
