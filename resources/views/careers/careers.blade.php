<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">

<head>

    <!--required meta tags-->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">

    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

    <!--twitter og-->
    <meta name="twitter:site" content="@themetags">
    <meta name="twitter:creator" content="@themetags">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Future Basics - Creators of livestoka, radarmile and avorra.">
    <meta name="twitter:description" content="Future Basics is a digital company bringing simplified digital solution into complex Development Spaces.">
    <meta name="twitter:image" content="#">

    <!--facebook og-->
    <meta property="og:url" content="#">
    <meta name="twitter:title" content="Future Basics - Creators of livestoka, radarmile and avorra">
    <meta property="og:description" content="Future Basics is a digital company bringing simplified digital solution into complex Development Spaces.">
    <meta property="og:image" content="#">
    <meta property="og:image:secure_url" content="#">
    <meta property="og:image:type" content="image/png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="600">

    <!--meta-->
    <meta name="description" content="=Basics is a digital company bringing simplified digital solution into complex Development Spaces.">
    <meta name="author" content="ThemeTags">
    <!--favicon icon-->
    <link rel="icon" href="{{ asset('img/fbicon.png') }}" type="image/png" sizes="16x16">

    <!--title-->
    <title>{{ config('app.name', 'Careers With Us - FutureBasics') }}</title>

    <!--google fonts-->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">

    <!--build:css-->
    <link href="{{ asset('css/main.css') }}" rel="stylesheet">
    <!-- endbuild -->

    <!--custom css start-->
    <link href="{{ asset('css/custom.css') }}" rel="stylesheet">
    <!--custom css end-->

</head>

<body>

    <!--preloader start-->
    <div id="preloader">
        <div class="preloader-wrap">
            <img src="{{ asset('img/fbicon.png') }}" alt="logo" class="img-fluid preloader-icon" />
            <div class="loading-bar"></div>
        </div>
    </div>
    <!--preloader end-->
    <!--main content wrapper start-->
    <div class="main-wrapper">

        <!--header section start-->
        @include('partials.public-navigation', ['navVariant' => 'light'])
        <!--header section end-->

        <!--page header section start-->
        <section class="page-header position-relative overflow-hidden ptb-120 bg-dark" style="background: url('img/page-header-bg.svg')no-repeat bottom left">
            <div class="container">
                <div class="row">
                    <div class="col-lg-8 col-md-12">
                        <h1 class="display-5 fw-bold">Careers</h1>
                        <p class="lead">
                            We are always looking for new individuals who will revolutionize how we approach and interact in our daily lives with the use of technology.
                        </p>
                    </div>
                </div>
                <div class="bg-circle rounded-circle circle-shape-3 position-absolute bg-dark-light right-5"></div>
            </div>
        </section>
        <!--page header section end-->

        <!--open jobs section start-->
        <section id="open-positions" class="open-jobs ptb-120">
            <div class="container">
                <div class="row align-items-center justify-content-between">
                    <div class="col-lg-4 col-md-12">
                        <div class="section-heading">
                            <h4 class="h5 text-primary">Available Opportunities</h4>
                            <h2>Current Available Positions at Future Basics</h2>
                        </div>
                    </div>
                    <div class="col-lg-7 col-md-12">
                        <p>
                            If you are passionate with technology as much as we are,
                            we would like to have you in our team. We understand in order to build
                            sophisticated tools that help communities and businesses we need creative, ambitious,
                            talented and impactful team players to work with us.
                        </p>
                    </div>
                </div>
                <div class="row justify-content-center">
                    {{-- <div class="col-lg-6 col-md-12">
                        <a href="{{ route('career-details') }}" class="text-decoration-none mt-4 mt-xl-0 mt-lg-0 single-open-job p-5 bg-dark text-white d-block rounded-custom">
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="job-time h-6 mb-2"><i class="far fa-briefcase me-2"></i> <strong>Remote - Full Time</strong></span>
                                <span class="badge px-3 py-2 bg-custom-light rounded-pill small">Developer</span>
                            </div>
                            <h3 class="h5">Jr Frontend Developer</h3>
                            <ul class="job-info-list list-inline list-unstyled text-muted">
                                <li class="list-inline-item"><span class="far fa-house-building me-1"></span> Future Basiscs</li>
                                <li class="list-inline-item"><span class="far fa-map-marker-alt me-1"></span> Dar es salaam, TZ</li>
                                <li class="list-inline-item"><span class="far fa-wallet me-1"></span> TZS 500K - 700K</li>
                            </ul>
                            <div class="btn btn-outline-light btn-sm d-inline-block mt-4">Apply Now</div>

                        </a>
                    </div>
                    <div class="col-lg-6 col-md-12">
                        <a href="{{ route('career-details') }}" class="text-decoration-none mt-4 mt-xl-0 mt-lg-0 single-open-job p-5 bg-dark text-white d-block rounded-custom">
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="job-time h-6 mb-2"><i class="far fa-briefcase me-2"></i> <strong>Remote - Full Time</strong></span>
                                <span class="badge px-3 py-2 bg-custom-light rounded-pill small">Designer</span>
                            </div>
                            <h3 class="h5">UI/UX and Product Designer</h3>
                            <ul class="job-info-list list-inline list-unstyled text-muted">
                                <li class="list-inline-item"><span class="far fa-house-building me-1"></span> Future Basiscs</li>
                                <li class="list-inline-item"><span class="far fa-map-marker-alt me-1"></span> Dar es salaam, TZ</li>
                                <li class="list-inline-item"><span class="far fa-wallet me-1"></span> TZS 500K - 700K</li>
                            </ul>
                            <div class="btn btn-outline-light btn-sm d-inline-block mt-4">Apply Now</div>
                        </a>
                    </div>
                    <div class="col-lg-6 col-md-12">
                        <a href="{{ route('career-details') }}" class="text-decoration-none mt-4 single-open-job p-5 bg-dark text-white d-block rounded-custom">
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="job-time h-6 mb-2"><i class="far fa-briefcase me-2"></i> <strong>Full Time</strong></span>
                                <span class="badge px-3 py-2 bg-custom-light rounded-pill small">Manager</span>
                            </div>
                            <h3 class="h5">Senior Office Manager</h3>
                            <ul class="job-info-list list-inline list-unstyled text-muted">
                                <li class="list-inline-item"><span class="far fa-house-building me-1"></span> Future Basiscs</li>
                                <li class="list-inline-item"><span class="far fa-map-marker-alt me-1"></span> Dar es salaam, TZ</li>
                                <li class="list-inline-item"><span class="far fa-wallet me-1"></span> TZS 500K - 700K</li>
                            </ul>
                            <div class="btn btn-outline-light btn-sm d-inline-block mt-4">Apply Now</div>
                        </a>
                    </div>
                    <div class="col-lg-6 col-md-12">
                        <a href="{{ route('career-details') }}" class="text-decoration-none mt-4 single-open-job p-5 bg-dark text-white d-block rounded-custom">
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="job-time h-6 mb-2"><i class="far fa-briefcase me-2"></i> <strong>Remote</strong></span>
                                <span class="badge px-3 py-2 bg-custom-light rounded-pill small">Developer</span>
                            </div>
                            <h3 class="h5">Senior Backend Developer</h3>
                            <ul class="job-info-list list-inline list-unstyled text-muted">
                                <li class="list-inline-item"><span class="far fa-house-building me-1"></span> Future Basiscs</li>
                                <li class="list-inline-item"><span class="far fa-map-marker-alt me-1"></span> Dar es salaam, TZ</li>
                                <li class="list-inline-item"><span class="far fa-wallet me-1"></span> TZS 500K - 700K</li>
                            </ul>
                            <div class="btn btn-outline-light btn-sm d-inline-block mt-4">Apply Now</div>
                        </a>
                    </div> --}}
                </div>
            </div>
        </section>
        <!--open jobs section end-->

        <!--career promo start-->
        <section class="career-promo ptb-120 bg-light">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-6 col-md-12">
                        <div class="section-heading text-center">
                            <h4 class="h5 text-primary">Why Join Us</h4>
                            <h2>Join Our Great Working Environment</h2>
                            <p>
                                Here at FBC we offer more than Jobs - We offer Careers. We look out for our own, the makers and builder of FBC vision, Our people, are considered our greatest resource who enable us to innovate, develop and generate long-term value.
                            </p>
                            </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6 col-lg-6">
                        <div class="single-feature d-flex mt-0 p-5 bg-white rounded-custom">
                            <span class="fas fa-house-user fa-2x text-primary"></span>
                            <div class="ms-4 mt-2">
                                <h5>A Culture of collaboration</h5>
                                <p class="mb-0">
                                    We value teamwork incredibly, as this is the only way to solve societal and business problems,
                                     while creating tomorrow's solutions and innovations.
                                     We are an all inclusive company with a large supportive culture that also recognizes,
                                     rewards and values outstanding individual contributions.
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 col-lg-6">
                        <div class="single-feature d-flex mt-4 mt-xl-0 mt-lg-0 mt-md-0 p-5 bg-white rounded-custom">
                            <span class="fas fa-clock fa-2x text-primary"></span>
                            <div class="ms-4 mt-2">
                                <h5>Flexible Working Hours</h5>
                                <p class="mb-0">
                                    In FBC we encourage and support that our team have flexible working hours and
                                    flexible work that can help you find the best balance between work and lifestyle.
                                    This is but not limited to flexible working hours, remote working and paint internship other benefits available if you are part of our growing team.
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 col-lg-6">
                        <div class="single-feature d-flex mt-4 p-5 bg-white rounded-custom">
                            <span class="fas fa-user-friends fa-2x text-primary"></span>
                            <div class="ms-4 mt-2">
                                <h5>Supporting our communities</h5>
                                <p class="mb-0">
                                    We at FBC have history of giving back, our business practice are aligned
                                     with protecting the environment and producing sustainable products that not only are good for
                                     the environment that are also efficient built with intention of reducing carbon emissions and protecting our plant for the next generation.
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 col-lg-6">
                        <div class="single-feature d-flex mt-4 p-5 bg-white rounded-custom">
                            <span class="fas fa-briefcase-medical fa-2x text-primary"></span>
                            <div class="ms-4 mt-2">
                                <h5>Unlimited Potential</h5>
                                <p class="mb-0">
                                    Our company understand the need of people to grow and pursue
                                     a career that is both fulfilling and that a paves a way to higher leadership positions that's
                                      why we have invested in career building initiatives, provided comprehensive learning
                                     resources and provide ongoing support to encourage and inspire you in every possible way.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <!--career promo end-->


        <!--cat subscribe start-->
        <section class="cta-subscribe bg-dark text-white ptb-120 position-relative overflow-hidden">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-8 col-md-10">
                        <div class="subscribe-info-wrap text-center position-relative z-2">
                            <div class="section-heading" data-aos="fade-up">
                                <h4 class="h5 text-warning">Lets Build Your Solution Get Free Support.</h4>
                                <h2>Start Your Development Journey With Us.</h2>
                                <p>We can assist you in building a tailored digital solutions for your business.</p>
                            </div>
                            <div class="form-block-banner mw-60 m-auto mt-5" data-aos="fade-up" data-aos-delay="50">
                                <a href="{{ route('contact-us') }}" class="btn btn-primary">Contact Us</a>
                                {{-- <a href="http://www.youtube.com/watch?v=hAP2QF--2Dg" class="text-decoration-none popup-youtube d-inline-flex align-items-center watch-now-btn ms-lg-3 ms-md-3 mt-3 mt-lg-0"> <i
                                        class="fas fa-play"></i> Watch Demo </a> --}}
                            </div>
                            {{-- <ul class="nav justify-content-center subscribe-feature-list mt-4" data-aos="fade-up" data-aos-delay="100">
                                <li class="nav-item">
                                    <span><i class="far fa-check-circle text-primary me-2"></i>No hidden charges</span>
                                </li>
                                <li class="nav-item">
                                    <span><i class="far fa-check-circle text-primary me-2"></i>No credit card required</span>
                                </li>
                                <li class="nav-item">
                                    <span><i class="far fa-check-circle text-primary me-2"></i>Support 24/7</span>
                                </li>
                                <li class="nav-item">
                                    <span><i class="far fa-check-circle text-primary me-2"></i>Be part of the development</span>
                                </li>
                            </ul> --}}
                        </div>
                    </div>
                </div>
                <div class="bg-circle rounded-circle circle-shape-3 position-absolute bg-dark-light left-5"></div>
                <div class="bg-circle rounded-circle circle-shape-1 position-absolute bg-warning right-5"></div>
            </div>
        </section>
        <!--cat subscribe end-->

             <!--footer section start-->
             <footer class="footer-section">
                <!--footer top start-->
                <!--for light footer add .footer-light class and for dark footer add .bg-dark .text-white class-->
                <div class="footer-top footer-light ptb-120">
                    <div class="container">
                        <div class="row justify-content-between">
                            <div class="col-md-8 col-lg-4 mb-md-4 mb-lg-0">
                                <div class="footer-single-col">
                                    <div class="footer-single-col mb-4">
                                        <img src="{{ asset('img/fb_og_logo.png') }}" alt="logo" class="img-fluid logo-white">
                                        <img src="{{ asset('img/fb_og_logo_drk.png') }}" alt="logo" class="img-fluid logo-color">
                                    </div>
                                    {{-- <p>Our latest news, articles, and resources, we will sent to
                                        your inbox weekly.</p>

                                    <form class="newsletter-form position-relative d-block d-lg-flex d-md-flex">
                                        <input type="text" class="input-newsletter form-control me-2" placeholder="Enter your email" name="email" required="" autocomplete="off">
                                        <input type="submit" value="Subscribe" data-wait="Please wait..." class="btn btn-primary mt-3 mt-lg-0 mt-md-0">
                                    </form> --}}
                                    <div class="ratting-wrap mt-4">
                                        <h6 class="mb-0">10/10 Overall rating</h6>
                                        <ul class="list-unstyled rating-list list-inline mb-0">
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12 col-lg-7 mt-4 mt-md-0 mt-lg-0">
                                <div class="row">
                                    <div class="col-md-4 col-lg-4 mt-4 mt-md-0 mt-lg-0">
                                        <div class="footer-single-col">
                                            <h3>Navigation</h3>
                                            <ul class="list-unstyled footer-nav-list mb-lg-0">
                                                <li><a href="{{ url('/') }}" class="text-decoration-none">Home</a></li>
                                                <li><a href="{{ route('about') }}" class="text-decoration-none">About Us</a></li>
                                                {{-- <li><a href="{{ route('business') }}" class="text-decoration-none">Services</a></li> --}}
                                                <li><a href="{{ route('careers-with-us') }}" class="text-decoration-none">Join Us</a></li>
                                            </ul>
                                        </div>
                                    </div>
                                    <div style="display: none;" class="col-md-4 col-lg-4 mt-4 mt-md-0 mt-lg-0">
                                        <div class="footer-single-col">
                                            <h3>Information</h3>
                                            <ul class="list-unstyled footer-nav-list mb-lg-0">
                                                <li><a href="{{ route('coming-soon') }}" class="text-decoration-none">Latest news</a></li>
                                                <li><a href="{{ route('coming-soon') }}" class="text-decoration-none">Blog</a></li>
                                                {{-- <li><a href="blog.html" class="text-decoration-none">Career</a></li> --}}

                                            </ul>
                                        </div>
                                    </div>
                                    <div class="col-md-4 col-lg-4 mt-4 mt-md-0 mt-lg-0">
                                        <div class="footer-single-col">
                                            <h3>Quick access</h3>
                                            <ul class="list-unstyled footer-nav-list mb-lg-0">
                                                <li><a href="{{ route('contact-us') }}" class="text-decoration-none">Contact us</a></li>
                                                {{-- <li><a href="support.html" class="text-decoration-none">Support</a></li>
                                                <li><a href="support-single.html" class="text-decoration-none">Support center</a></li>
                                                <li><a href="team.html" class="text-decoration-none">Our Team</a></li> --}}
                                                <li><a href="{{ route('careers-with-us') }}" class="text-decoration-none">Careers</a>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>
                <!--footer top end-->

                <!--footer bottom start-->
                <div class="footer-bottom footer-light py-4">
                    <div class="container">
                        <div class="row justify-content-between align-items-center">
                            <div class="col-md-7 col-lg-7">
                                <div class="copyright-text">
                                    {{-- <p class="mb-lg-0 mb-md-0">&copy; 2021 Future Basics Rights Reserved. Designed By <a href="https://futurebasics.co.tz" class="text-decoration-none">Future </a></p> --}}
                                    <p class="mb-lg-0 mb-md-0">&copy; 2022 Future Basics Rights Reserved.</a></p>

                                </div>
                            </div>
                            <div class="col-md-4 col-lg-4">
                                <div class="footer-single-col text-start text-lg-end text-md-end">
                                    <ul class="list-unstyled list-inline footer-social-list mb-0">
                                        {{-- <li class="list-inline-item"><a href="#"><i class="fab fa-facebook-f"></i></a></li> --}}
                                        <li class="list-inline-item"><a href="https://wa.me/message/YD7YWU6AS55ZN1"><i class="fab fa-whatsapp"></i></a></li>
                                        <li class="list-inline-item"><a href="https://www.instagram.com/futurebasicsltd/"><i class="fab fa-instagram"></i></a></li>
                                        <li class="list-inline-item"><a href="https://twitter.com/futurebasicsltd"><i class="fab fa-twitter"></i></a></li>
                                        <li class="list-inline-item"><a href="https://github.com/devnechi/fbwebltd.git"><i class="fab fa-github"></i></a></li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <!--footer bottom end-->
            </footer>
            <!--footer section end-->


        </div>

        <!--build:js-->
        <script src="{{ asset('js/vendors/jquery-3.6.0.min.js') }}"></script>
        <script src="{{ asset('js/vendors/bootstrap.bundle.min.js') }}"></script>
        <script src="{{ asset('js/vendors/swiper-bundle.min.js') }}"></script>
        <script src="{{ asset('js/vendors/jquery.magnific-popup.min.js') }}"></script>
        <script src="{{ asset('js/vendors/parallax.min.js') }}"></script>
        <script src="{{ asset('js/vendors/aos.js') }}"></script>
        <script src="{{ asset('js/app.js') }}"></script>
        <!--endbuild-->
    </body>

    </html>

