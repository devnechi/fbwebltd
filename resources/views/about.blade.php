@extends('layouts.public_layout')

@section('content')
    <!-- https://mdbootstrap.com/img/Photos/Others/architecture.jpg -->
    <!-- Full Page Intro -->
    <div class="view"
        style="background-image: url('images/africa_people.jpg'); background-repeat: no-repeat; background-size: cover; background-position: center center; height: 740px;">
        <!-- Mask & flexbox options-->
        <div class="mask rgba-gradient align-items-center">
            <!-- Content -->
            <div class="container">
                <!--Grid row-->
                <div class="row">
                    <!--Grid column-->
                    <div class="col-md-6 white-text text-center text-md-left mt-xl-5 mb-5 wow fadeInLeft"
                        data-wow-delay="0.3s">
                        <h1 class="h1-responsive font-weight-bold mt-sm-5" style="color:rgb(216, 216, 29);  padding-top: 40px;">Simplified</h1>
                        <h1 class="h1-responsive font-weight-bold mt-sm-5" style="margin-top: 0rem !important;">Digital Solutions</h1>
                    </div>
                    <!--Grid column-->
                    <!--Grid column-->
                    <div class="col-md-6 white-text text-center text-md-left mt-xl-5 mb-5 wow fadeInRight"
                        data-wow-delay="0.3s" style="padding-top: 40px;">

                        {{-- <img class="spin icon-size" src="images/fbicon.png" alt="" class="img-fluid"> --}}
                        {{-- <img src="images/fbholo.png" alt="" class="img-fluid"> --}}

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
    <section id="about-panels">
        <div class="container">
            <br />
            <br />
             <div class="row">
                 <div class="col-lg-12">
                    <ul class="nav nav-tabs about-nav" id="myTab" role="tablist">
                        <li class="nav-item">
                          <a class="nav-link active" id="about-us-tab" data-toggle="tab" href="#about-us" role="about-us" aria-controls="about-us"
                            aria-selected="true">About us</a>
                        </li>
                        <li class="nav-item">
                          <a class="nav-link" id="vision-mission-tab" data-toggle="tab" href="#vision-mission" role="tab" aria-controls="vision-mission"
                            aria-selected="false">Vision & Mission</a>
                        </li>

                        <li class="nav-item">
                            <a class="nav-link" id="business-philosophy-tab" data-toggle="tab" href="#business-philosophy" role="tab" aria-controls="business-philosophy"
                              aria-selected="false">Business & Management Philosophy</a>
                          </li>

                        <li class="nav-item">
                            <a class="nav-link" id="our-culture-tab" data-toggle="tab" href="#our-culture" role="tab" aria-controls="our-culture"
                              aria-selected="false">Our Culture</a>
                          </li>
                      </ul>
                      <div class="tab-content" id="myTabContent">
                            <div class="tab-pane show active" id="about-us" role="tabpanel" aria-labelledby="about-us-tab">
                                <br />
                                <br />
                                <div class="row">
                                    <div class="col-md-4 ">
                                        <div class="card">
                                            <img src="https://mdbootstrap.com/img/Mockups/Lightbox/Thumbnail/img%20(67).jpg" alt="Avatar" style="width:100%">

                                        </div>
                                    </div>
                                    <div class="col-md-8">
                                        <h2 class="h1-responsive font-weight-bold mt-sm-5">Us as a Company</h2>
                                        <br />
                                        <p style="font-size: 24px;">Future Basics is a dynamic company that utilizes its out-reach and large network to create sustainable and profitable technological solutions</p>
                                        <br />
                                        <p style="font-size: 12px;">We support access to future technologies, execute large to small projects, consult MSMEs, Local Authorities, Government Agencies, Not-for-profit organisations and development programs on using technologies to build value.
                                            We are a value-oriented company, we bring creativity and excellence in everything we are involved in. We thrive in designing and developing business systems solutions with prioritised focus on developing countries. Future Basic </p>
                                        <br />
                                        </div>
                                </div>
                                <br />
                            </div>
                            <div class="tab-pane fade" id="vision-mission" role="tabpanel" aria-labelledby="vision-mission-tab">
                                <br />
                                <br />
                                <div class="row">
                                    <div class="col-md-4 ">
                                        <div class="card">
                                            <img src="https://mdbootstrap.com/img/Mockups/Lightbox/Thumbnail/img%20(67).jpg" alt="Avatar" style="width:100%">

                                        </div>
                                    </div>
                                    <div class="col-md-8">
                                        <h2 class="h1-responsive font-weight-bold mt-sm-5">Vision</h2>
                                        <br />
                                        <p style="font-size: 18px;">Our vision is to be the leading digital consulting and technology services company in Tanzania and beyond. </p>
                                    </div>
                                </div>
                                <br />
                                <br />
                                <div class="row">
                                    <div class="col-md-4 ">
                                        <div class="card">
                                            <img src="https://mdbootstrap.com/img/Mockups/Lightbox/Thumbnail/img%20(67).jpg" alt="Avatar" style="width:100%">

                                        </div>
                                    </div>
                                    <div class="col-md-8">
                                        <h2 class="h1-responsive font-weight-bold mt-sm-5">Mission</h2>
                                        <br />
                                        <p style="font-size: 18px;">
                                            Our mission is to provide superior and transformative
                                             consulting and technology services using the latest technology and
                                             top-notch consultants to make development work and business investment more efficient,
                                             profitable and impactful in an environment of honesty, integrity,
                                             fairness and courtesy towards our clients, partners, staff and society at large.
                                        </p>
                                    </div>
                                </div>
                                <br />
                                <br />

                            </div>
                            <div class="tab-pane fade" id="business-philosophy" role="tabpanel" aria-labelledby="business-philosophy-tab">
                                <br />
                                <br />
                                <div class="row">
                                    <div class="col-md-4 ">
                                        <div class="card">
                                            <img src="https://mdbootstrap.com/img/Mockups/Lightbox/Thumbnail/img%20(67).jpg" alt="Avatar" style="width:100%">

                                        </div>
                                    </div>
                                    <div class="col-md-8">
                                        <h2 class="h1-responsive font-weight-bold mt-sm-5">Our Business Philosophy</h2>
                                        <br />
                                        <p style="font-size: 24px;">Our clients must see tangible results from our work.</p>
                                    </div>
                                </div>
                                <br />
                                <br />
                                <div class="row">
                                    <div class="col-md-4 ">
                                        <div class="card">
                                            <img src="https://mdbootstrap.com/img/Mockups/Lightbox/Thumbnail/img%20(67).jpg" alt="Avatar" style="width:100%">

                                        </div>
                                    </div>
                                    <div class="col-md-8">
                                        <h2 class="h1-responsive font-weight-bold mt-sm-5">Our Management Philosophy</h2>
                                        <br />
                                        <p style="font-size: 12px;">
                                            Excellence in all we do. A commitment to strive, be innovative and to constantly improve ourselves, our teams, our services and products so as to become the best.

                                            Leadership by Example. A commitment to set standards in our business and transactions and be an exemplar for the industry and our own teams.

                                            Integrity and Transparency: A commitment to be ethical, sincere and open in our dealings.</p>
                                        <p style="font-size: 12px;">
                                            Focus on the Client: We inspire trust from our clients by being fair and acting ethically. All business decisions are designed and implemented with you in mind, the client.

                                            Employee Centered: We attract and develop the best talent for our business, share knowledge and provide them with the necessary tools and resources to keep up with today’s fast changing environment.

                                        </p>
                                    </div>
                                </div>
                                <br />
                                <br />
                            </div>
                            <div class="tab-pane fade" id="our-culture" role="tabpanel" aria-labelledby="our-culture-tab">
                                <br />
                                <br />
                                <div class="row">
                                    <div class="col-md-4 ">
                                        <div class="card">
                                            <img src="https://mdbootstrap.com/img/Mockups/Lightbox/Thumbnail/img%20(67).jpg" alt="Avatar" style="width:100%">

                                        </div>
                                    </div>
                                    <div class="col-md-8">
                                        <h2 class="h1-responsive font-weight-bold mt-sm-5">Our Culture</h2>
                                        <br />
                                        <p style="font-size: 12px;">
                                            Excellence in all we do. A commitment to strive, be innovative and to constantly improve ourselves, our teams, our services and products so as to become the best.
                                            Leadership by Example. A commitment to set standards in our business and transactions and be an exemplar for the industry and our own teams.
                                            Integrity and Transparency: A commitment to be ethical, sincere and open in our dealings.</p>
                                        <p style="font-size: 12px;">
                                            Focus on the Client: We inspire trust from our clients by being fair and acting ethically. All business decisions are designed and implemented with you in mind, the client.
                                            Employee Centered: We attract and develop the best talent for our business, share knowledge and provide them with the necessary tools and resources to keep up with today’s fast changing environment.
                                        </p>

                                    </div>
                                </div>
                                <br />
                                <br />
                            </div>
                      </div>
                </div>
             </div>

        </div>
    </section>



@endsection
