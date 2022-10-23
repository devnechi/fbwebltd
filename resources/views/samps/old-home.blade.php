<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">

<head>
    <!--required meta tags-->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <!--twitter og-->
    <meta name="twitter:site" content="@futurebasicsltd">
    <meta name="twitter:creator" content="@futurebasicsltd">
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
    <meta name="description" content="Basics is a digital company bringing simplified digital solution into complex Development Spaces.">
    <meta name="author" content="ThemeTags">
    <!--favicon icon-->
    <link rel="icon" href="img/fbicon.png" type="image/png" sizes="16x16">
    <!--title-->
    <title>{{ config('app.name', 'FutureBasics') }}</title>
    <!--google fonts-->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">

    <!--build:css-->
    <link rel="stylesheet" href="css/main.css">
    <link href="{{ asset('css/main.css') }}" rel="stylesheet">
    <link href="{{ asset('css/app.css') }}" rel="stylesheet">
    <!-- endbuild -->
    <!--custom css start-->
    {{-- <link rel="stylesheet" href="css/custom.css"> --}}
    <link href="{{ asset('css/custom.css') }}" rel="stylesheet">
    <!--custom css end-->
    <script src="{{ asset('js/app.js') }}" defer></script>
</head>

<body>

    <!--preloader start-->
    <div id="preloader">
        <div class="preloader-wrap">
            <img src="img/fbicon.png" alt="logo" class="img-fluid preloader-icon" />
            <div class="loading-bar"></div>
        </div>
    </div>
    <!--preloader end-->
    <!--main content wrapper start-->
    <div class="main-wrapper">

        <!--header section start-->
        <!--header start-->
        <header class="main-header position-absolute w-100">
            <nav class="navbar navbar-expand-xl navbar-dark sticky-header">
                <div class="container d-flex align-items-center justify-content-lg-between position-relative">
                    <a href="{{ url('/') }}" class="navbar-brand d-flex align-items-center mb-md-0 text-decoration-none">
                        <img src="img/fb_og_logo.png" alt="logo" class="img-fluid logo-white" />
                        <img src="img/fb_og_logo_drk.png" alt="logo" class="img-fluid logo-color" />
                    </a>

                    <a class="navbar-toggler position-absolute right-0 border-0" href="#offcanvasWithBackdrop" role="button">
                        <span class="far fa-bars" data-bs-toggle="offcanvas" data-bs-target="#offcanvasWithBackdrop" aria-controls="offcanvasWithBackdrop"></span>
                    </a>
                    <div class="clearfix"></div>
                    <div class="collapse navbar-collapse justify-content-center">
                        <ul class="nav col-12 col-md-auto justify-content-center main-menu">
                            <li><a href="{{ url('/') }}" class="nav-link">Home</a></li>
                            <li><a href="{{ route('about') }}" class="nav-link">About us</a></li>

                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="{{ route('our-services') }}" role="button" data-bs-toggle="dropdown" aria-expanded="false">Services</a>
                                <div class="dropdown-menu border-0 rounded-custom shadow py-0 bg-white">
                                    <div class="dropdown-grid rounded-custom width-full-3">
                                        <div class="dropdown-grid-item">
                                            <h6 class="drop-heading">Digital Solutions</h6>
                                            <a href="{{ route('all-graphic-designs-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-eject"></i></span>
                                                <div class="drop-title">Graphics Design</div>
                                            </a>

                                            <a href="{{ route('all-data-science-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-browser"></i></span>
                                                <div class="drop-title">Data Science</div>
                                            </a>
                                            <a href="{{ route('all-web-development-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-globe"></i></span>
                                                <div class="drop-title">Website Design & Development</div>
                                            </a>

                                            <a href="{{ route('all-mobile-development-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-mobile"></i></span>
                                                <div class="drop-title">Mobile App Development</div>
                                            </a>
                                        </div>
                                        <div class="dropdown-grid-item">
                                            <h6 class="drop-heading">Business Solutions</h6>
                                            <a href="{{ route('all-prototyping-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-bolt"></i></span>
                                                <div class="drop-title">Prototyping</div>
                                            </a>
                                            <a href="{{ route('all-software-development-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-code-fork"></i></span>
                                                <div class="drop-title">Software Engineering</div>
                                            </a>
                                            <a href="{{ route('all-bus-sys-development-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-briefcase"></i></span>
                                                <div class="drop-title">Business System Development</div>
                                            </a>
                                            <a href="{{ route('all-branding-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-heartbeat"></i></span>
                                                <div class="drop-title">Branding & Digital Strategizing</div>
                                            </a>
                                            {{-- <a href="{{ route('our-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-usd-square"></i></span>
                                                <div class="drop-title">Business Systems</div>
                                            </a>
                                            <a href="{{ route('our-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-th-list"></i></span>
                                                <div class="drop-title">Digital Strategies</div>
                                            </a>
                                            <a href="{{ route('our-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-chart-network"></i></span>
                                                <div class="drop-title">Business Analytics</div>
                                            </a>
                                            <a href="{{ route('our-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-paper-plane"></i></span>
                                                <div class="drop-title">Augumented Sol.</div>
                                            </a> --}}
                                        </div>
                                        <div class="dropdown-grid-item last-item bg-light radius-right-side">
                                            <a href="#"><img src="img/about/bs-ppl.jpg" alt="add" class="img-fluid rounded-custom" /></a>
                                        </div>
                                    </div>
                                </div>
                            </li>
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="{{ route('business') }}" role="button" data-bs-toggle="dropdown" aria-expanded="false">Portfolio</a>
                                {{-- @guest
                                @if (Route::has('login'))
                                    <a href="{{ route('login') }}" class="btn btn-outline-primary me-2">Sign In</a>
                                @endif
                            @else
                            <a class="btn btn-outline-primary me-2" href="{{ route('logout') }}"
                                    onclick="event.preventDefault(); document.getElementById('logout-form').submit();">
                                    {{ __('Logout') }}
                                </a>
                                <form id="logout-form" action="{{ route('logout') }}" method="POST" class="d-none">
                                    @csrf
                                </form>

                            @endguest --}}
                                <div class="dropdown-menu border-0 rounded-custom shadow py-0 bg-white">
                                    <div class="dropdown-grid rounded-custom width-full">
                                        <div class="dropdown-grid-item">
                                            <h6 class="drop-heading">Enterprise Solutions</h6>
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link px-0">
                                                <span class="me-2"><i class="far fa-fingerprint"></i></span>
                                                <div class="drop-title">Livestoka</div>
                                            </a>
                                            <a href="https://radarmile.com/" class="dropdown-link px-0">
                                                <span class="me-2"><i class="far fa-address-book"></i></span>
                                                <div class="drop-title">Radarmile</div>
                                            </a>
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-code-branch"></i></span>
                                                <div class="drop-title">Nakwalify</div>
                                            </a>


                                        </div>
                                        <div class="dropdown-grid-item radius-right-side bg-light">
                                            <h6 class="drop-heading">Innovations</h6>
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-code-branch"></i></span>
                                                <div class="drop-title">Smart Risiti</div>
                                            </a>
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-life-ring"></i></span>
                                                <div class="drop-title">Mennyu</div>
                                            </a>
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-headset"></i></span>
                                                <div class="drop-title">Tavrenni</div>
                                            </a>
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-laptop-code"></i></span>
                                                <div class="drop-title">Avorra</div>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </li>
                        </ul>
                    </div>

                    <div class="action-btns text-end me-5 me-lg-0 d-none d-md-block d-lg-block">
                        <a href="{{ route('login') }}" class="btn btn-link text-decoration-none me-2">Sign In</a>
                        <a href="{{ route('contact-us') }}" class="btn btn-primary">Contact Us</a>
                    </div>

                       <!--offcanvas menu start-->
                       <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasWithBackdrop">
                        <div class="offcanvas-header d-flex align-items-center mt-4">
                            <a href="{{ url('/') }}" class="d-flex align-items-center mb-md-0 text-decoration-none">
                                <img src="img/fb_og_logo_drk.png" alt="logo" class="img-fluid ps-2" />
                            </a>
                            <button type="button" class="close-btn text-danger" data-bs-dismiss="offcanvas" aria-label="Close">
                                <i class="far fa-close"></i>
                            </button>
                        </div>
                        <div class="offcanvas-body">
                            <ul class="nav col-12 col-md-auto justify-content-center main-menu">
                                <li><a href="{{ url('/') }}" class="nav-link">Home</a></li>
                                <li><a href="{{ url('about') }}" class="nav-link">About us</a></li>
                                <li class="nav-item dropdown">
                                    <a class="nav-link dropdown-toggle" href=""{{ route('our-services') }}"" role="button" data-bs-toggle="dropdown" aria-expanded="false">Our Services</a>
                                    <div class="dropdown-menu border-0 rounded-custom shadow py-0 bg-white">
                                        <div class="dropdown-grid rounded-custom width-full-3">
                                            <div class="dropdown-grid-item">
                                                <h6 class="drop-heading">Digital Solutions</h6>
                                                <a href="{{ route('all-graphic-designs-services') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-bars"></i></span>
                                                    <div class="drop-title">Graphics Design</div>
                                                </a>

                                                <a href="{{ route('all-data-science-services') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-code-branch"></i></span>
                                                    <div class="drop-title">Data Science</div>
                                                </a>
                                                <a href="{{ route('all-web-development-services') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-globe"></i></span>
                                                    <div class="drop-title">Website Design & Development</div>
                                                </a>

                                                <a href="{{ route('all-mobile-development-services') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-mobile"></i></span>
                                                    <div class="drop-title">Mobile App Development</div>
                                                </a>
                                            </div>
                                            <div class="dropdown-grid-item">
                                                <h6 class="drop-heading">Business Solutions</h6>
                                                <a href="{{ route('all-prototyping-services') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-usd-square"></i></span>
                                                    <div class="drop-title">Prototyping</div>
                                                </a>
                                                <a href="{{ route('all-software-development-services') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-th-list"></i></span>
                                                    <div class="drop-title">Software Engineering</div>
                                                </a>
                                                <a href="{{ route('all-bus-sys-development-services') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-briefcase"></i></span>
                                                    <div class="drop-title">Business System Development</div>
                                                </a>
                                                <a href="{{ route('all-branding-services') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-heartbeat"></i></span>
                                                    <div class="drop-title">Branding & Digital Strategizing</div>
                                                </a>
                                            </div>
                                            <div class="dropdown-grid-item last-item bg-light radius-right-side">
                                                <a href="#"><img src="img/about/bs-ppl.jpg" alt="add" class="img-fluid rounded-custom" /></a>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li class="nav-item dropdown">
                                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Portfolio</a>
                                    <div class="dropdown-menu border-0 rounded-custom shadow py-0 bg-white">
                                        <div class="dropdown-grid rounded-custom width-full">
                                            <div class="dropdown-grid-item">
                                                <h6 class="drop-heading">Enterprise Solutions</h6>
                                                <a href="{{ route('coming-soon') }}" class="dropdown-link px-0">
                                                    <span class="me-2" ><i class="far fa-fingerprint"></i></span>
                                                    <div class="drop-title">Livestoka</div>
                                                </a>
                                                <a href="https://radarmile.com/" class="dropdown-link px-0">
                                                    <span class="me-2"><i class="far fa-address-book"></i></span>
                                                    <div class="drop-title">Radarmile</div>
                                                </a>
                                                <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-code-branch"></i></span>
                                                    <div class="drop-title">Nakwalify</div>
                                                </a>
                                            </div>
                                            <div class="dropdown-grid-item radius-right-side bg-light">
                                                <h6 class="drop-heading">Innovations</h6>

                                            <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-code-branch"></i></span>
                                                <div class="drop-title">Smart Risiti</div>
                                            </a>
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-life-ring"></i></span>
                                                <div class="drop-title">Mennyu</div>
                                            </a>
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-headset"></i></span>
                                                <div class="drop-title">Tavrenni</div>
                                            </a>
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-laptop-code"></i></span>
                                                <div class="drop-title">Avorra</div>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                            <div class="action-btns mt-4 ps-3">
                                    @guest
                                        @if (Route::has('login'))
                                            <a href="{{ route('login') }}" class="btn btn-outline-primary me-2">Sign In</a>
                                        @endif
                                    @else
                                    <a class="btn btn-outline-primary me-2" href="{{ route('logout') }}"
                                            onclick="event.preventDefault(); document.getElementById('logout-form').submit();">
                                            {{ __('Logout') }}
                                        </a>
                                        <form id="logout-form" action="{{ route('logout') }}" method="POST" class="d-none">
                                            @csrf
                                        </form>

                                    @endguest
                                    <div>
                                        <a href="{{ route('contact-us') }}" class="btn btn-primary">Contact us</a>
                                    </div>
                            </div>

                        </div>
                       </div>
                    <!--offcanvas menu end-->
                </div>
            </nav>
        </header>
        <!--header end-->
        <!--header section end-->

        <!--hero section start-->
        <section class="hero-section ptb-120 bg-dark text-white" style="background: url('img/shape/dot-dot-wave-shape.svg')no-repeat bottom left">
            <div class="container">
                <div class="row align-items-center justify-content-lg-between">
                    <div class="col-xl-5 col-lg-5">
                        <div class="hero-content-wrap text-center text-xl-start text-lg-start mt-5 mt-lg-0 mt-xl-0" data-aos="fade-up">
                            <h1 class="fw-bold display-5">Simplified, Tailored and Innovative Digital Solutions</h1>
                            <p class="lead">
                                We support business, corporate and
                                community development through
                                innovation and technology.
                            </p>
                            <div class="hero-subscribe-form-wrap pt-4 position-relative m-auto m-xl-0 d-none d-md-block d-lg-block d-xl-block">
                                {{-- <form id="subscribe-form" name="email-form" class="hero-subscribe-form d-block d-lg-flex d-md-flex">
                                    <input type="email" class="form-control me-2" name="Email" data-name="Email" placeholder="Enter Your Email Address" id="email-address" required="">
                                    <input type="submit" value="Subscribe" data-wait="Please wait..." class="btn btn-primary mt-3 mt-lg-0 mt-md-0">
                                </form>
                                <ul class="nav subscribe-feature-list mt-3 justify-content-lg-start justify-content-md-center">
                                    <li class="nav-item">
                                        <span class="ms-0"><i class="far fa-check-circle text-primary me-2"></i>Free for ever</span>
                                    </li>
                                    <li class="nav-item">
                                        <span><i class="far fa-check-circle text-primary me-2"></i>No credit card required</span>
                                    </li>
                                </ul> --}}
                            </div>
                        </div>
                    </div>
                    <div class="col-xl-6 col-lg-6 mt-lg-5 mt-4">
                        <div class="hero-img-wrap position-relative" style="" data-aos="fade-up">
                            <div class="hero-screen-wrap">
                                <div class="phone-screen">
                                    <img src="img/screen/phn-hd.png" alt="hero image" class="position-relative img-fluid">
                                </div>
                                <div class="mac-screen">
                                    <img src="img/screen/dash-hero.png" alt="hero image" class="position-relative img-fluid rounded-custom">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <!--hero section end-->

        <!--customer section start-->
        {{-- <div class="customer-section pb-120 bg-dark">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-8 col-12">
                        <ul class="customer-logos-grid text-center list-unstyled mb-0">
                            <li>
                                <img src="img/clients/client-logo-1.svg" width="150" alt="clients logo" class="img-fluid customer-logo p-1 p-md-2 p-lg-3 m-auto" data-aos="fade-up" data-aos-delay="50">
                            </li>
                            <li>
                                <img src="img/clients/client-logo-2.svg" width="150" alt="clients logo" class="img-fluid customer-logo p-1 p-md-2 p-lg-3 m-auto" data-aos="fade-up" data-aos-delay="50">
                            </li>
                            <li>
                                <img src="img/clients/client-logo-3.svg" width="150" alt="clients logo" class="img-fluid customer-logo p-1 p-md-2 p-lg-3 m-auto" data-aos="fade-up" data-aos-delay="50">
                            </li>
                            <li>
                                <img src="img/clients/client-logo-4.svg" width="150" alt="clients logo" class="img-fluid customer-logo p-1 p-md-2 p-lg-3 m-auto" data-aos="fade-up" data-aos-delay="50">
                            </li>
                            <li>
                                <img src="img/clients/client-logo-5.svg" width="150" alt="clients logo" class="img-fluid customer-logo p-1 p-md-2 p-lg-3 m-auto" data-aos="fade-up" data-aos-delay="100">
                            </li>
                            <li>
                                <img src="img/clients/client-logo-6.svg" width="150" alt="clients logo" class="img-fluid customer-logo p-1 p-md-2 p-lg-3 m-auto" data-aos="fade-up" data-aos-delay="100">
                            </li>
                            <li>
                                <img src="img/clients/client-logo-7.svg" width="150" alt="clients logo" class="img-fluid customer-logo p-1 p-md-2 p-lg-3 m-auto" data-aos="fade-up" data-aos-delay="100">
                            </li>
                            <li>
                                <img src="img/clients/client-logo-8.svg" width="150" alt="clients logo" class="img-fluid customer-logo p-1 p-md-2 p-lg-3 m-auto" data-aos="fade-up" data-aos-delay="100">
                            </li>
                        </ul>
                        <p class="text-center mt-lg-5 mt-4 mb-0" data-aos="fade-up" data-aos-delay="200">Trusted More than 25,00+ Companies Around the World</p>
                    </div>
                </div>
            </div>
        </div> --}}
        <!--customer section end-->


        <!--highlight promo start-->
        <section class="promo-section ptb-120">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-md-10 col-lg-6">
                        <div class="section-heading text-center" data-aos="fade-up">
                            <h2>Leading Our Community Into The
                                Future.</h2>
                            <p>
                                We believe the future is digital,
                                and through innovation and techonology,
                                we are leading our community into it.
                            </p>
                        </div>
                    </div>
                </div>
                {{-- <div class="row">
                    <div class="col-md-6 col-lg-4">
                        <div class="promo-card-wrap promo-border-hover border border-2 bg-white rounded-custom p-5 mb-4 mb-lg-0 mb-md-4" data-aos="fade-up" data-aos-delay="50">
                            <div class="promo-card-info">
                                <h3 class="display-5 fw-medium mb-4">15+</h3>
                                <h2 class="h5">Completed Projects</h2>
                                <p class="mb-0">Tailored solutions for businesses, development spaces and communities.</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 col-lg-4">
                        <div class="promo-card-wrap promo-border-hover border border-2 bg-white rounded-custom p-5 mb-4 mb-lg-0 mb-md-4" data-aos="fade-up" data-aos-delay="100">
                            <div class="promo-card-info">
                                <h3 class="display-5 fw-medium mb-4">2k</h3>
                                <h2 class="h5">Happy Client</h2>
                                <p class="mb-0">Rapid digital solutions that improve customer satisfaction.</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 col-lg-4">
                        <div class="promo-card-wrap promo-border-hover border border-2 bg-white rounded-custom p-5 mb-4 mb-lg-0 mb-md-0" data-aos="fade-up" data-aos-delay="150">
                            <div class="promo-card-info">
                                <h3 class="display-5 fw-medium mb-4">90%</h3>
                                <h2 class="h5">24/7 Support</h2>
                                <p class="mb-0">We offer on-call support for your business and product. </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div> --}}
        </section>
        <!--highlight promo end-->
        <!-- app two video promo start -->
        <section class="video-promo-with-icon">
            <div class="container">
                <div class="video-bg-with-icon" style="height: 680px; background: url('img/image-1.png')no-repeat center center / cover">
                    <a href="https://www.youtube.com/watch?v=MuJQnSe1R5k" class="popup-youtube"><i class="fas fa-play"></i></a>

                </div>
                {{-- <iframe width="560" height="315" src="https://www.youtube.com/embed/MuJQnSe1R5k" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> --}}
            </div>
            <div class="video-promo-icon-wrapper bg-light pt-80 pb-120">
                <div class="container">
                    <div class="row">
                        <div class="col-lg-3 col-xl-3 col-md-6 mt-4 mt-md-4 mt-lg-0">
                            <div class="single-icon-box p-0 p-lg-4">
                                <i class="far fa-chart-pie-alt icon-one"></i>
                                <h5 class="h6">Effective Solutions</h5>
                                <p>
                                    Efficient solutions that work
                                    in the real world.
                                </p>
                            </div>
                        </div>
                        <div class="col-lg-3 col-xl-3 col-md-6 mt-4 mt-md-4 mt-lg-0">
                            <div class="single-icon-box p-0 p-lg-4">
                                <i class="far fa-pen-nib icon-two"></i>
                                <h5 class="h6">Personalized Designs</h5>
                                <p>Get solutions that are built with the intended end-user in mind.</p>
                            </div>
                        </div>
                        <div class="col-lg-3 col-xl-3 col-md-6 mt-4 mt-md-4 mt-lg-0">
                            <div class="single-icon-box p-0 p-lg-4">
                                <i class="far fa-chart-network icon-three"></i>
                                <h5 class="h6">Versatile Solutions</h5>
                                <p>
                                    Digital solutions that
                                    continoulsy adapt to their
                                    intended environment
                                </p>
                            </div>
                        </div>
                        <div class="col-lg-3 col-xl-3 col-md-6 mt-4 mt-md-4 mt-lg-0">
                            <div class="single-icon-box p-0 p-lg-4">
                                <i class="far fa-bezier-curve icon-four"></i>
                                <h5 class="h6">Tailored Solutions </h5>
                                <p>Customised solutions that fit
                                    each unique context.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <!-- app two video promo end -->

        <!--feature section start-->
        <section class="feature-section-two pt-60 pb-120">
            <div class="container">
                <div class="row align-items-center justify-content-between">
                    <div class="col-lg-5 col-md-12">
                        <div class="section-heading" data-aos="fade-up">
                            <h4 class="h5 text-primary">Features</h4>
                            <h2>Powerful Solutions for Your Business</h2>
                            <p>
                                Implement digital strategies that are
                                tailored to your business needs with
                                the knowledge of what works for you.
                            </p>
                            <ul class="list-unstyled mt-5">
                                <li class="d-flex align-items-start mb-4">
                                    <div class="icon-box bg-primary rounded me-4">
                                        <i class="fas fa-bezier-curve text-white"></i>
                                    </div>
                                    <div class="icon-content">
                                        <h3 class="h5">Automate your business processes</h3>
                                        <p>
                                            We create digital software and strategies
                                            that automate various tasks within your
                                            business, thus improving efficiency,
                                            accuracy and ease of work.
                                        </p>
                                    </div>
                                </li>
                                <li class="d-flex align-items-start mb-4">
                                    <div class="icon-box bg-danger rounded me-4">
                                        <i class="fas fa-fingerprint text-white"></i>
                                    </div>
                                    <div class="icon-content">
                                        <h3 class="h5">Customized  &amp; Tailored Solutions</h3>
                                        <p>
                                            Out of the box solutions are good, but
                                            solutions that are developed specifically for
                                            your business are even better. We develop
                                            solutions specifically designed for your needs.
                                        </p>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-lg-6 col-md-7">
                        <div class="feature-img-wrap position-relative d-flex flex-column align-items-end">
                            <ul class="img-overlay-list list-unstyled position-absolute">
                                <li class="d-flex align-items-center bg-white rounded shadow-sm p-3" data-aos="fade-up" data-aos-delay="50">
                                    <i class="fas fa-check bg-primary text-white rounded-circle"></i>
                                    <h6 class="mb-0">Improve Business performance  </h6>
                                </li>
                                <li class="d-flex align-items-center bg-white rounded shadow-sm p-3" data-aos="fade-up" data-aos-delay="100">
                                    <i class="fas fa-check bg-primary text-white rounded-circle"></i>
                                    <h6 class="mb-0">Automate your business
                                        processes for increased
                                        efficiency. </h6>
                                </li>
                                <li class="d-flex align-items-center bg-white rounded shadow-sm p-3" data-aos="fade-up" data-aos-delay="150">
                                    <i class="fas fa-check bg-primary text-white rounded-circle"></i>
                                    <h6 class="mb-0">Make effective business
                                        decisions using data</h6>
                                </li>
                            </ul>
                            <img src="img/image-2.png" alt="feature image" class="img-fluid rounded-custom" data-aos="fade-up">
                        </div>
                    </div>
                </div>
            </div>
        </section>
        {{-- <section class="feature-section pt-60 pb-120">
            <div class="container">
                <div class="row align-items-lg-center justify-content-between">
                    <div class="col-lg-5 order-lg-2 mb-7 mb-lg-0">
                        <div class="mb-4" data-aos="fade-up">
                            <h2>Experience your Product with Integration</h2>
                            <p>
                                Conveniently deliver your services and products to a wide-range of clients and businesses, improve customer acquisition and enthusiastically drive customer satisfaction.
                            </p>
                        </div>
                        <ul class="list-unstyled d-flex flex-wrap list-two-col mt-5" data-aos="fade-up" data-aos-delay="50">
                            <li>
                                <span class="d-block mb-4"><i class="fal fa-user fa-2x text-primary"></i></span>
                                <h3 class="h5">Customer analysis</h3>
                                <p>Objectively understand your customer needs and wants, Make strategic business decisions using internal solutions data analysis metrics.
                                </p>
                            </li>
                            <li>
                                <span class="d-block mb-4"><i class="fal fa-watch fa-2x text-primary"></i></span>
                                <h3 class="h5">Real time metrics</h3>
                                <p>Utilize technology to map, track and increase transparency on how customers interact with your product. </p>
                            </li>
                        </ul>
                    </div>
                    <div class="col-lg-6 order-lg-1">
                        <div class="pr-lg-4">
                            <div class="bg-light text-center rounded-custom overflow-hidden p-lg-5 p-3 mx-lg-auto" data-aos="fade-up" data-aos-delay="50">
                                <img src="img/dashboard-img.svg" alt="" class="img-fluid">
                                <div class="position-absolute bg-primary-dark z--1 dot-mask dm-size-16 dm-wh-350 top--40 left--40 top-left"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section> --}}
        <!--feature section end-->

        <!--feature service grid section start-->
        <section class="feature-section ptb-120 bg-dark text-white ">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-6 col-md-10">
                        <div class="section-heading text-center" data-aos="fade-up">
                            <h2>Services We Offer</h2>
                            <p>Choose your digitalsolution today</p>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-12">
                        <div class="feature-grid">
                            <div class="feature-card  bg-custom-light promo-border-hover border border-2 border-light text-white shadow-sm highlight-card rounded-custom p-5" data-aos="fade-up" data-aos-delay="50">
                                <div class="icon-box d-inline-block rounded-circle bg-primary-soft mb-32">
                                    <i class="fal fa-analytics icon-sm text-primary"></i>
                                </div>
                                <div class="feature-content">
                                    <h3 class="h5">Business analysis & system
                                        development</h3>
                                    <p>
                                        Get custom made business software
                                        solutions that address your specific
                                        business needs, context and
                                        processes.
                                        We analyse our client's businesses
                                        and provide expert advice on how
                                        they can implement new software
                                        solutions or improve existing ones in
                                        order to:
                                        Increase business efficiency
                                        Increase ease of work
                                        Increase market competetiveness
                                        Improve customer engagement
                                        Expand their business.
                                    </p>
                                    <p>Our solution are built to be user-centered, increasing customer satisfaction which is optimal in growing a business.</p>
                                    <h6 class="mt-4">Included with...</h6>
                                    <ul class="list-unstyled mb-0">
                                        <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>High-convertion</li>
                                        <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Personal Branding</li>
                                        <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Performance optimized</li>
                                        <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>User friendly (UI/UX)</li>
                                        <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Efficient and cost effective</li>
                                        <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Easy customization features</li>
                                        <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Cross-Technology compatibility</li>
                                        <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Secure and encrypted data handling approaches</li>

                                    </ul>
                                </div>
                                <a href="{{ route('all-software-development-services') }}" class="link-with-icon text-decoration-none mt-3">View Details <i class="far fa-arrow-right"></i></a>
                            </div>
                            <div class="feature-card  bg-custom-light promo-border-hover border border-2 border-light text-white shadow-sm rounded-custom p-5" data-aos="fade-up" data-aos-delay="50">
                                <div class="icon-box d-inline-block rounded-circle bg-success-soft mb-32">
                                    <i class="fal fa-file-chart-line icon-sm text-success"></i>
                                </div>
                                <div class="feature-content">
                                    <h3 class="h5">Mobile app development</h3>
                                    <p class="mb-0">
                                        Get a tailor made mobile app for
                                        your business or corporation, or even
                                        simply bring your app idea to life.
                                        </p>
                                </div>
                                <a href="{{ route('all-software-development-services') }}" class="link-with-icon text-decoration-none mt-3">View Details <i class="far fa-arrow-right"></i></a>
                            </div>
                            <div class="feature-card  bg-custom-light promo-border-hover border border-2 border-light text-white shadow-sm rounded-custom p-5" data-aos="fade-up" data-aos-delay="50">
                                <div class="icon-box d-inline-block rounded-circle bg-danger-soft mb-32">
                                    <i class="fal fa-user-friends icon-sm text-danger"></i>
                                </div>
                                <div class="feature-content">
                                    <h3 class="h5">Software Engineering</h3>
                                    <p class="mb-0">
                                        Get custom made digital software that
                                        increases your business performance and
                                        efficiency as well as ease of work at any
                                        level,regardless of your industry or size.
                                    </p>
                                </div>
                                <a href="{{ route('all-prototyping-services') }}" class="link-with-icon text-decoration-none mt-3">View Details <i class="far fa-arrow-right"></i></a>
                            </div>
                            <div class="feature-card  bg-custom-light promo-border-hover border border-2 border-light text-white shadow-sm rounded-custom p-5" data-aos="fade-up" data-aos-delay="50">
                                <div class="icon-box d-inline-block rounded-circle bg-dark-soft mb-32">
                                    <i class="fal fa-spell-check icon-sm text-dark"></i>
                                </div>
                                <div class="feature-content">
                                    <h3 class="h5">Digital Marketing & Strategizing</h3>
                                    <p class="mb-0">
                                        Find out how you can stand out in today's
                                        crowded online scene and get more eyes
                                        on your business or project.
                                    </p>
                                </div>
                                <a href="{{ route('all-data-science-services') }}" class="link-with-icon text-decoration-none mt-3">View Details <i class="far fa-arrow-right"></i></a>
                            </div>
                            <div class="feature-card  bg-custom-light promo-border-hover border border-2 border-light text-white shadow-sm rounded-custom p-5" data-aos="fade-up" data-aos-delay="50">
                                <div class="icon-box d-inline-block rounded-circle bg-warning-soft mb-32">
                                    <i class="fal fa-cog icon-sm text-warning"></i>
                                </div>
                                <div class="feature-content">
                                    <h3 class="h5">Graphic design</h3>
                                    <p class="mb-0">
                                        Give your business and brand a
                                        proffessional essence with custom made
                                        graphic content.
                                    </p>
                                </div>
                                <a href="{{ route('all-graphic-designs-services') }}" class="link-with-icon text-decoration-none mt-3">View Details <i class="far fa-arrow-right"></i></a>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </section>
        <!--feature service grid section end-->

        <!--work process section start-->
        <section class="work-process ptb-120">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-md-10 col-lg-6">
                        <div class="section-heading text-center" data-aos="fade-up">
                            <h4 class="h5 text-primary">Process</h4>
                            <h2>A Development Process You Can Trust</h2>
                            <p>
                                Using world standard development
                                methodoligies, we design efficient
                                and high performing softwares
                                that address our clients needs
                                regardless of their size or industry.
                            </p>
                        </div>
                    </div>
                </div>
                <div class="row d-flex align-items-center">
                    <div class="col-md-6 col-lg-3">
                        <div class="process-card text-center px-4 py-lg-5 py-4 rounded-custom shadow-hover mb-3 mb-lg-0" data-aos="fade-up" data-aos-delay="50">
                            <div class="process-icon border border-light bg-custom-light rounded-custom p-3">
                                <span class="h2 mb-0 text-primary fw-bold">1</span>
                            </div>
                            <h3 class="h5">Research</h3>
                            <p class="mb-0">
                                Analysis of target market
                                and concept feasibility.
                            </p>
                        </div>
                    </div>
                    <div class="dots-line first"></div>
                    <div class="col-md-6 col-lg-3">
                        <div class="process-card text-center px-4 py-lg-5 py-4 rounded-custom shadow-hover mb-3 mb-lg-0" data-aos="fade-up" data-aos-delay="100">
                            <div class="process-icon border border-light bg-custom-light rounded-custom p-3">
                                <span class="h2 mb-0 text-primary fw-bold">2</span>
                            </div>
                            <h3 class="h5">Design</h3>
                            <p class="mb-0">
                                Transformation of concepts
                                    into effective prototypes.
                                </p>
                        </div>
                    </div>
                    <div class="dots-line first"></div>
                    <div class="col-md-6 col-lg-3">
                        <div class="process-card text-center px-4 py-lg-5 py-4 rounded-custom shadow-hover mb-3 mb-lg-0 mb-md-0" data-aos="fade-up" data-aos-delay="150">
                            <div class="process-icon border border-light bg-custom-light rounded-custom p-3">
                                <span class="h2 mb-0 text-primary fw-bold">3</span>
                            </div>
                            <h3 class="h5">Development</h3>
                            <p class="mb-0">
                                Materialisation of
                                prototypes into finalised
                                digital products.
                            </p>
                        </div>
                    </div>
                    <div class="dots-line first"></div>
                    <div class="col-md-6 col-lg-3">
                        <div class="process-card text-center px-4 py-lg-5 py-4 rounded-custom shadow-hover mb-0" data-aos="fade-up" data-aos-delay="200">
                            <div class="process-icon border border-light bg-custom-light rounded-custom p-3">
                                <span class="h2 mb-0 text-primary fw-bold">4</span>
                            </div>
                            <h3 class="h5">Delivery & Maintaince</h3>
                            <p class="mb-0">
                                Product launching, followed by
                                continous monitoring and
                                improvement.
                            </p>
                        </div>
                    </div>
                    {{-- <div class="dots-line first"></div>
                    <div class="col-md-6 col-lg-3">
                        <div class="process-card text-center px-4 py-lg-5 py-4 rounded-custom shadow-hover mb-0" data-aos="fade-up" data-aos-delay="200">
                            <div class="process-icon border border-light bg-custom-light rounded-custom p-3">
                                <span class="h2 mb-0 text-primary fw-bold">5</span>
                            </div>
                            <h3 class="h5">Maintain</h3>
                            <p class="mb-0">Uniquely for compelling initiatives expanded interactive.</p>
                        </div>
                    </div> --}}
                </div>
            </div>
        </section>
        <!--work process section end-->

        <!--integration section start-->
        {{-- <section class="integration-section pt-60 pb-120">
            <div class="container">
                <div class="row align-items-center justify-content-lg-between">
                    <div class="col-lg-6 col-md-12">
                        <div class="section-heading" data-aos="fade-up">
                            <h4 class="h5 text-primary">Integration</h4>
                            <h2>We Collaborate with Top Software Company</h2>
                        </div>
                    </div>
                    <div class="col-lg-4 col-md-12">
                        <div class="text-lg-end mb-5 mb-lg-0" data-aos="fade-up">
                            <a href="integrations.html" class="btn btn-primary">View All Integrations</a>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-12">
                        <div class="integration-wrapper position-relative w-100">
                            <!--animated shape start-->
                            <ul class="position-absolute animate-element parallax-element shape-service z--1 d-none d-lg-none d-xl-block">

                                <li class="layer" data-depth="0.02">
                                    <img src="img/color-shape/feature-2.svg" alt="shape" class="img-fluid position-absolute color-shape-2 z-5">
                                </li>
                                <li class="layer" data-depth="0.03">
                                    <img src="img/color-shape/feature-3.svg" alt="shape" class="img-fluid position-absolute color-shape-3">
                                </li>
                            </ul>
                            <!--animated shape end-->
                            <ul class="integration-list list-unstyled mb-0">
                                <li data-aos="fade-up" data-aos-delay="50">
                                    <div class="single-integration">
                                        <img src="img/integations/airbnb.png" alt="integration" class="img-fluid">
                                        <h6 class="mb-0 mt-4">Brand Name</h6>
                                    </div>
                                </li>
                                <li data-aos="fade-up" data-aos-delay="50">
                                    <div class="single-integration">
                                        <img src="img/integations/figma.png" alt="integration" class="img-fluid">
                                        <h6 class="mb-0 mt-4">Brand Name</h6>
                                    </div>
                                </li>
                                <li data-aos="fade-up" data-aos-delay="50">
                                    <div class="single-integration">
                                        <img src="img/integations/facebook.png" alt="integration" class="img-fluid">
                                        <h6 class="mb-0 mt-4">Brand Name</h6>
                                    </div>
                                </li>
                                <li data-aos="fade-up" data-aos-delay="50">
                                    <div class="single-integration">
                                        <img src="img/integations/sales-force.png" alt="integration" class="img-fluid">
                                        <h6 class="mb-0 mt-4">Brand Name</h6>
                                    </div>
                                </li>
                                <li data-aos="fade-up" data-aos-delay="50">
                                    <div class="single-integration">
                                        <img src="img/integations/atlassian.png" alt="integration" class="img-fluid">
                                        <h6 class="mb-0 mt-4">Brand Name</h6>
                                    </div>
                                </li>
                                <li data-aos="fade-up" data-aos-delay="50">
                                    <div class="single-integration">
                                        <img src="img/integations/dropbox-2.png" alt="integration" class="img-fluid">
                                        <h6 class="mb-0 mt-4">Brand Name</h6>
                                    </div>
                                </li>
                                <li data-aos="fade-up" data-aos-delay="100">
                                    <div class="single-integration">
                                        <img src="img/integations/dynamic-365.png" alt="integration" class="img-fluid">
                                        <h6 class="mb-0 mt-4">Brand Name</h6>
                                    </div>
                                </li>
                                <li data-aos="fade-up" data-aos-delay="100">
                                    <div class="single-integration">
                                        <img src="img/integations/erecruiter.png" alt="integration" class="img-fluid">
                                        <h6 class="mb-0 mt-4">Brand Name</h6>
                                    </div>
                                </li>
                                <li data-aos="fade-up" data-aos-delay="100">
                                    <div class="single-integration">
                                        <img src="img/integations/evernote.png" alt="integration" class="img-fluid">
                                        <h6 class="mb-0 mt-4">Brand Name</h6>
                                    </div>
                                </li>
                                <li data-aos="fade-up" data-aos-delay="100">
                                    <div class="single-integration">
                                        <img src="img/integations/google-icon.png" alt="integration" class="img-fluid">
                                        <h6 class="mb-0 mt-4">Brand Name</h6>
                                    </div>
                                </li>

                                <li data-aos="fade-up" data-aos-delay="100">
                                    <div class="single-integration">
                                        <img src="img/integations/slack.png" alt="integration" class="img-fluid">
                                        <h6 class="mb-0 mt-4">Brand Name</h6>
                                    </div>
                                </li>

                                <li data-aos="fade-up" data-aos-delay="100">
                                    <div class="single-integration">
                                        <img src="img/integations/google-analytics.png" alt="integration" class="img-fluid">
                                        <h6 class="mb-0 mt-4">Brand Name</h6>
                                    </div>
                                </li>

                                <li data-aos="fade-up" data-aos-delay="150">
                                    <div class="single-integration">
                                        <img src="img/integations/google-drive.png" alt="integration" class="img-fluid">
                                        <h6 class="mb-0 mt-4">Brand Name</h6>
                                    </div>
                                </li>

                                <li data-aos="fade-up" data-aos-delay="150">
                                    <div class="single-integration">
                                        <img src="img/integations/hubspot.png" alt="integration" class="img-fluid">
                                        <h6 class="mb-0 mt-4">Brand Name</h6>
                                    </div>
                                </li>

                                <li data-aos="fade-up" data-aos-delay="150">
                                    <div class="single-integration">
                                        <img src="img/integations/instagram.png" alt="integration" class="img-fluid">
                                        <h6 class="mb-0 mt-4">Brand Name</h6>
                                    </div>
                                </li>
                                <li data-aos="fade-up" data-aos-delay="150">
                                    <div class="single-integration">
                                        <img src="img/integations/linkedin.png" alt="integration" class="img-fluid">
                                        <h6 class="mb-0 mt-4">Brand Name</h6>
                                    </div>
                                </li>
                                <li data-aos="fade-up" data-aos-delay="150">
                                    <div class="single-integration">
                                        <img src="img/integations/mailchimp.png" alt="integration" class="img-fluid">
                                        <h6 class="mb-0 mt-4">Brand Name</h6>
                                    </div>
                                </li>
                                <li data-aos="fade-up" data-aos-delay="150">
                                    <div class="single-integration">
                                        <img src="img/integations/marekto.png" alt="integration" class="img-fluid">
                                        <h6 class="mb-0 mt-4">Brand Name</h6>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </section> --}}
        <!--integration section end-->

        <!--customer review tab section start-->
        {{-- <section class="testimonial-section ptb-120 bg-light">
            <div class="container">
                <div class="row justify-content-center align-content-center">
                    <div class="col-md-10 col-lg-6">
                        <div class="section-heading text-center" data-aos="fade-up">
                            <h4 class="h5 text-primary">Testimonial</h4>
                            <h2>What They Say About Us</h2>
                            <p>Uniquely promote adaptive quality vectors rather than stand-alone e-markets pontificate alternative architectures with accurate schemas.</p>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-12">
                        <div class="position-relative w-100" data-aos="fade-up" data-aos-delay="50">
                            <div class="swiper-container testimonialSwiper">
                                <div class="swiper-wrapper">
                                    <div class="swiper-slide border border-2 p-5 rounded-custom position-relative">
                                        <img src="img/testimonial/quotes-dot.svg" alt="quotes" width="100" class="img-fluid position-absolute left-0 top-0 z--1 p-3">
                                        <div class="d-flex mb-32 align-items-center">
                                            <img src="img/testimonial/1.jpg" class="img-fluid me-3 rounded" width="60" alt="user">
                                            <div class="author-info">
                                                <h6 class="mb-0">Mr.Rupan Oberoi</h6>
                                                <small>Founder and CEO at Amaara Herbs</small>
                                            </div>
                                        </div>
                                        <blockquote>
                                            <h6>The Best Template You Got to Have it!</h6>
                                            Globally network long-term high-impact schemas vis-a-vis distinctive e-commerce
                                            cross-media infrastructures rather than ethical
                                        </blockquote>
                                        <ul class="review-rate mb-0 mt-2 list-unstyled list-inline">
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                        </ul>
                                        <img src="img/testimonial/quotes.svg" alt="quotes" class="position-absolute right-0 bottom-0 z--1 pe-4 pb-4">
                                    </div>
                                    <div class="swiper-slide border border-2 p-5 rounded-custom position-relative">
                                        <img src="img/testimonial/quotes-dot.svg" alt="quotes" width="100" class="img-fluid position-absolute left-0 top-0 z--1 p-3">
                                        <div class="d-flex mb-32 align-items-center">
                                            <img src="img/testimonial/3.jpg" class="img-fluid me-3 rounded" width="60" alt="user">
                                            <div class="author-info">
                                                <h6 class="mb-0">Oberoi R.</h6>
                                                <small>CEO at Herbs</small>
                                            </div>
                                        </div>
                                        <blockquote>
                                            <h6>Embarrassed by the First Version.</h6>
                                            Dynamically create innovative core competencies with effective best
                                            practices promote innovative infrastructures.
                                        </blockquote>
                                        <ul class="review-rate mb-0 mt-2 list-unstyled list-inline">
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                        </ul>
                                        <img src="img/testimonial/quotes.svg" alt="quotes" class="position-absolute right-0 bottom-0 z--1 pe-4 pb-4">
                                    </div>
                                    <div class="swiper-slide border border-2 p-5 rounded-custom position-relative">
                                        <img src="img/testimonial/quotes-dot.svg" alt="quotes" width="100" class="img-fluid position-absolute left-0 top-0 z--1 p-3">
                                        <div class="d-flex mb-32 align-items-center">
                                            <img src="img/testimonial/2.jpg" class="img-fluid me-3 rounded" width="60" alt="user">
                                            <div class="author-info">
                                                <h6 class="mb-0">Mr.Rupan Oberoi</h6>
                                                <small>Founder and CEO</small>
                                            </div>
                                        </div>
                                        <blockquote>
                                            <h6>Amazing Future Basics template!</h6>
                                            Appropriately negotiate interactive niches rather than parallel strategic theme incubate premium total linkage areas.
                                        </blockquote>
                                        <ul class="review-rate mb-0 mt-2 list-unstyled list-inline">
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                        </ul>
                                        <img src="img/testimonial/quotes.svg" alt="quotes" class="position-absolute right-0 bottom-0 z--1 pe-4 pb-4">
                                    </div>
                                    <div class="swiper-slide border border-2 p-5 rounded-custom position-relative">
                                        <img src="img/testimonial/quotes-dot.svg" alt="quotes" width="100" class="img-fluid position-absolute left-0 top-0 z--1 p-3">
                                        <div class="d-flex mb-32 align-items-center">
                                            <img src="img/testimonial/4.jpg" class="img-fluid me-3 rounded" width="60" alt="user">
                                            <div class="author-info">
                                                <h6 class="mb-0">Joan Dho</h6>
                                                <small>Founder and CTO</small>
                                            </div>
                                        </div>
                                        <blockquote>
                                            <h6>Best Template for SAAS Company!</h6>
                                            Dynamically create innovative core competencies with effective best
                                            practices promote innovative infrastructures.
                                        </blockquote>
                                        <ul class="review-rate mb-0 mt-2 list-unstyled list-inline">
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                        </ul>
                                        <img src="img/testimonial/quotes.svg" alt="quotes" class="position-absolute right-0 bottom-0 z--1 pe-4 pb-4">
                                    </div>
                                    <div class="swiper-slide border border-2 p-5 rounded-custom position-relative">
                                        <img src="img/testimonial/quotes-dot.svg" alt="quotes" width="100" class="img-fluid position-absolute left-0 top-0 z--1 p-3">
                                        <div class="d-flex mb-32 align-items-center">
                                            <img src="img/testimonial/5.jpg" class="img-fluid me-3 rounded" width="60" alt="user">
                                            <div class="author-info">
                                                <h6 class="mb-0">Ranu Mondal</h6>
                                                <small>Lead Developer</small>
                                            </div>
                                        </div>
                                        <blockquote>
                                            <h6>It is undeniably good!</h6>
                                            Rapidiously supply client-centric e-markets and maintainable processes progressively engineer
                                        </blockquote>
                                        <ul class="review-rate mb-0 mt-2 list-unstyled list-inline">
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                            <li class="list-inline-item"><i class="fas fa-star text-warning"></i></li>
                                        </ul>
                                        <img src="img/testimonial/quotes.svg" alt="quotes" class="position-absolute right-0 bottom-0 z--1 pe-4 pb-4">
                                    </div>
                                </div>
                            </div>
                            <span class="swiper-button-next"></span>
                            <span class="swiper-button-prev"></span>
                        </div>
                    </div>
                </div>
            </div>
        </section> --}}
        <!--customer review tab section end-->

        <!--cat subscribe start-->
        <section class="cta-subscribe bg-dark text-white ptb-120 position-relative overflow-hidden">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-8 col-md-10">
                        <div class="subscribe-info-wrap text-center position-relative z-2">
                            <div class="section-heading" data-aos="fade-up">
                                <h4 class="h5 text-warning">Lets Build Your Digital Solution.
                                    Get Free Support.</h4>
                                <h2>Start Your Digital Solution Journey
                                    Today.</h2>
                                <p>Customised Digital Solutions For:
                                    Businesses, Communities & Corporations.</p>
                            </div>
                            <div class="form-block-banner mw-60 m-auto mt-5" data-aos="fade-up" data-aos-delay="50">
                                <a href="{{ route('contact-us') }}" class="btn btn-primary">Contact Us</a>
                                {{-- <a href="https://www.youtube.com/MuJQnSe1R5k"" class="text-decoration-none popup-youtube d-inline-flex align-items-center watch-now-btn ms-lg-3 ms-md-3 mt-3 mt-lg-0"> <i
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
                                    <img src="img/fb_og_logo.png" alt="logo" class="img-fluid logo-white">
                                    <img src="img/fb_og_logo_drk.png" alt="logo" class="img-fluid logo-color">
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
    <script src="js/vendors/jquery-3.6.0.min.js"></script>
    <script src="js/vendors/bootstrap.bundle.min.js"></script>
    <script src="js/vendors/swiper-bundle.min.js"></script>
    <script src="js/vendors/jquery.magnific-popup.min.js"></script>
    <script src="js/vendors/parallax.min.js"></script>
    <script src="js/vendors/aos.js"></script>
    <script src="js/app.js"></script>
    <!--endbuild-->
</body>

</html>
