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
    <meta name="twitter:description"
        content="Future Basics is a digital company bringing simplified digital solution into complex Development Spaces.">
    <meta name="twitter:image" content="#">

    <!--facebook og-->
    <meta property="og:url" content="#">
    <meta name="twitter:title" content="Future Basics - Creators of livestoka, radarmile and avorra">
    <meta property="og:description"
        content="Future Basics is a digital company bringing simplified digital solution into complex Development Spaces.">
    <meta property="og:image" content="#">
    <meta property="og:image:secure_url" content="#">
    <meta property="og:image:type" content="image/png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="600">

    <!--meta-->
    <meta name="description"
        content="=Basics is a digital company bringing simplified digital solution into complex Development Spaces.">
    <meta name="author" content="ThemeTags">
    <!--favicon icon-->
    <link rel="icon" href="img/fbicon.png" type="image/png" sizes="16x16">

    <!--title-->
    <title>{{ config('app.name', 'About us - FutureBasics') }}</title>

    <!--google fonts-->
    <link
        href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Open+Sans:wght@400;600&display=swap"
        rel="stylesheet">

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
            <img src="img/fbicon.png" alt="logo" class="img-fluid preloader-icon" />
            <div class="loading-bar"></div>
        </div>
    </div>
    <!--preloader end-->
    <!--main content wrapper start-->
    <div class="main-wrapper">

        <!--header section start-->
        <header class="main-header w-100">
            <nav class="navbar navbar-expand-xl navbar-light sticky-header">
                <div class="container d-flex align-items-center justify-content-lg-between position-relative">
                    <a href="{{ url('/') }}"
                        class="navbar-brand d-flex align-items-center mb-md-0 text-decoration-none">
                        <img src="img/fb_og_logo.png" alt="logo" class="img-fluid logo-white" />
                        <img src="img/fb_og_logo_drk.png" alt="logo" class="img-fluid logo-color" />
                    </a>

                    <a class="navbar-toggler position-absolute right-0 border-0" href="#offcanvasWithBackdrop"
                        role="button">
                        <span class="far fa-bars" data-bs-toggle="offcanvas" data-bs-target="#offcanvasWithBackdrop"
                            aria-controls="offcanvasWithBackdrop"></span>
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
                                                <div class="drop-title">Website Development</div>
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
                                            <a href="http://livestoka.com/" class="dropdown-link px-0">
                                                <span class="me-2"><i class="far fa-fingerprint"></i></span>
                                                <div class="drop-title">Livestoka</div>
                                            </a>
                                            <a href="https://radarmile.com/" class="dropdown-link px-0">
                                                <span class="me-2"><i class="far fa-address-book"></i></span>
                                                <div class="drop-title">Radarmile</div>
                                            </a>
                                            {{-- <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-code-branch"></i></span>
                                                <div class="drop-title">Nakwalify</div>
                                            </a> --}}


                                        </div>
                                        <div class="dropdown-grid-item radius-right-side bg-light">
                                            <h6 class="drop-heading">Innovations</h6>
                                            <a href="https://smartrisiti.com/" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-code-branch"></i></span>
                                                <div class="drop-title">Smart Risiti</div>
                                            </a>
                                            {{-- <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-life-ring"></i></span>
                                                <div class="drop-title">Wakala +</div>
                                            </a>
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-headset"></i></span>
                                                <div class="drop-title">Wakili</div>
                                            </a>
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-laptop-code"></i></span>
                                                <div class="drop-title">Avorra</div>
                                            </a> --}}
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
                                                <a href="{{ route('all-software-development-services') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-globe"></i></span>
                                                    <div class="drop-title">Website Development</div>
                                                </a>

                                                <a href="{{ route('all-software-development-services') }}" class="dropdown-link">
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
                                                <a href="{{ route('all-software-development-services') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-briefcase"></i></span>
                                                    <div class="drop-title">Business System Development</div>
                                                </a>
                                                <a href="{{ route('all-software-development-services') }}" class="dropdown-link">
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
                                                <a href="http://livestoka.com/" class="dropdown-link px-0">
                                                    <span class="me-2" ><i class="far fa-fingerprint"></i></span>
                                                    <div class="drop-title">Livestoka</div>
                                                </a>
                                                <a href="https://radarmile.com/" class="dropdown-link px-0">
                                                    <span class="me-2"><i class="far fa-address-book"></i></span>
                                                    <div class="drop-title">Radarmile</div>
                                                </a>
                                                {{-- <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-code-branch"></i></span>
                                                    <div class="drop-title">Nakwalify</div>
                                                </a> --}}
                                            </div>
                                            <div class="dropdown-grid-item radius-right-side bg-light">
                                                <h6 class="drop-heading">Innovations</h6>
                                                {{-- <a href="https://smartrisiti.com/" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-code-branch"></i></span>
                                                    <div class="drop-title">Smart Risiti</div>
                                                </a>
                                                <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-life-ring"></i></span>
                                                    <div class="drop-title">Wakala +</div>
                                                </a>
                                                <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-headset"></i></span>
                                                    <div class="drop-title">Wakili</div>
                                                </a>
                                                <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                    <span class="me-2" ><i class="far fa-laptop-code"></i ></span>
                                                    <div class="drop-title">Avorra</div>
                                                </a> --}}
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
        <!--header section end-->

        <!--about header section start-->
        <section class="about-header-section ptb-120 position-relative overflow-hidden bg-dark"
            style="background: url('img/page-header-bg.svg')no-repeat center right">
            <div class="container">
                <div class="row">
                    <div class="col-12">
                        <div class="section-heading-wrap d-flex justify-content-between z-5 position-relative">
                            <div class="about-content-left">
                                <div class="about-info mb-5">
                                    <h1 class="fw-bold display-5">
                                        We are leading our community into the
                                        future. Are you coming?
                                    </h1>
                                    <p class="lead">
                                        Future Basics aims to respond to the widely un-acknowledged and un-attended need
                                        for digitization in our society at corporate,
                                        business and community level. We believe the future is digital, and we aim
                                        to be part of the frontliners that lead our community into this future.
                                    </p>
                                    <p class="lead">
                                        Through innovation and technology, we implement the
                                        concept of digitization in various parts of our society, which in turn
                                        improves local business effeciency and the ease of life our
                                        community.
                                    </p>
                                    {{-- <a href="{{ route('careers-with-us') }}"
                                    class="btn btn-primary mt-4 me-3">Join Us</a>
                                    <a href="{{ route('developers-info-entery-form') }}"
                                        class="btn btn-primary mt-4 me-3">Join Our Dev Pool</a>
                                    <a href="{{ route('collection-of-innovators') }}"
                                        class="btn btn-primary mt-4 me-3">Join Our Talent Pool</a> --}}

                                    {{-- <a href="#our-team" class="btn btn-soft-primary mt-4">Meet Our Team</a> --}}
                                </div>

                                <br />
                                <br />
                                <br />
                                <br />
                                <br />
                                <br />
                                <br />
                                <br />
                                <br />
                                <br />
                                <br />
                                <br />
                                <br />
                                <br />
                                <br />
                                <br />
                                <img src="img/about/buildbus.jpg" style="display: none;" alt="about"
                                    class="img-fluid about-img-first mt-5 rounded-custom shadow">
                            </div>
                            <div class="about-content-right">
                                <img src="img/about/school-kids.jpg" alt="about"
                                    class="img-fluid mb-5 rounded-custom shadow">
                                {{-- <img src="img/about/auto-tina.jpg" alt="about" class="rounded-custom about-img-last shadow"> --}}
                                <img src="img/1.png" alt="about" class="rounded-custom about-img-last shadow">

                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="bg-white position-absolute bottom-0 h-25 bottom-0 left-0 right-0 z-2 py-5">
            </div>
        </section>
        <!--about header section end-->

        <!--our story section start-->
        {{-- <section class="our-story-section pt-60 pb-120" style="background: url('img/shape/dot-dot-wave-shape.svg')no-repeat left bottom">
            <div class="container">
                <div class="row justify-content-between">
                    <div class="col-lg-5 col-md-12 order-lg-1">
                        <div class="section-heading sticky-sidebar">
                            <h4 class="h5 text-primary">Our Story</h4>
                            <h2>A Great Story Starts with a Friendly Team</h2>
                            <p>We support access to future technologies, execute large to small projects, consult SMEs, Local Authorities,
                                Government Agencies, Not-for-profit organisations and development programs on using technologies to build value.
                                We are a value-oriented company, we bring creativity and excellence in everything we are involved in.
                                 We thrive in designing and developing digital solutions  that positively impacts our communities. </p>
                            <div class="mt-4">
                                <h6 class="mb-3">We Are Awarded By-</h6>
                                <img src="img/awards-01.svg" alt="awards" class="me-4 img-fluid">
                                <img src="img/awards-02.svg" alt="awards" class="img-fluid">
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-6 col-md-12 order-lg-0">
                        <div class="story-grid-wrapper position-relative">
                            <!--animated shape start-->
                            <ul class="position-absolute animate-element parallax-element shape-service d-none d-lg-block">
                                <li class="layer" data-depth="0.02">
                                    <img src="img/color-shape/image-2.svg" alt="shape" class="img-fluid position-absolute color-shape-2 z-5">
                                </li>
                                <li class="layer" data-depth="0.03">
                                    <img src="img/color-shape/feature-3.svg" alt="shape" class="img-fluid position-absolute color-shape-3">
                                </li>
                            </ul>
                            <!--animated shape end-->
                            <div class="story-grid rounded-custom bg-dark overflow-hidden position-relative">
                                <div class="story-item bg-light border">
                                    <h3 class="display-5 fw-bold mb-1 text-success">12K+</h3>
                                    <h6 class="mb-0">Active Users</h6>
                                </div>
                                <div class="story-item bg-white border">
                                    <h3 class="display-5 fw-bold mb-1 text-primary">20+</h3>
                                    <h6 class="mb-0">Team Members</h6>
                                </div>
                                <div class="story-item bg-white border">
                                    <h3 class="display-5 fw-bold mb-1 text-dark">$20K+</h3>
                                    <h6 class="mb-0">Revenue Per/Year</h6>
                                </div>
                                <div class="story-item bg-light border">
                                    <h3 class="display-5 fw-bold mb-1 text-warning">8 Years</h3>
                                    <h6 class="mb-0">In Business</h6>
                                </div>
                                <div class="story-item bg-light border">
                                    <h3 class="display-5 fw-bold mb-1 text-danger">20+</h3>
                                    <h6 class="mb-0">Clients Worldwide</h6>
                                </div>
                                <div class="story-item bg-white border">
                                    <h3 class="display-5 fw-bold mb-1 text-primary">15+</h3>
                                    <h6 class="mb-0">Projects Completed</h6>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section> --}}
        <!--our story section end-->

        <!--feature section two start-->
        <section id="valuenmission" class="feature-section-two ptb-120 bg-light">
            <div class="container">
                <div class="row align-items-center justify-content-center">
                    <div class="col-lg-6 col-md-12">
                        <div class="section-heading">
                            <h4 class="h5 text-primary">Our Values</h4>
                            <h2>The Core Values That Drive Us</h2>
                            <p>
                                A commitment to lead, innovate and
                                continously improve businesses and
                                communities around us.
                            </p>
                            <ul class="list-unstyled mt-5">
                                <li class="d-flex align-items-start mb-4">
                                    <div class="icon-box bg-primary rounded me-4">
                                        <i class="fas fa-bezier-curve text-white"></i>
                                    </div>
                                    <div class="icon-content">
                                        <h3 class="h5">Community Obligation</h3>
                                        <p>
                                            We believe in equitable growth, where everbody is included.
                                        </p>
                                    </div>
                                </li>
                                <li class="d-flex align-items-start mb-4">
                                    <div class="icon-box bg-danger rounded me-4">
                                        <i class="fas fa-fingerprint text-white"></i>
                                    </div>
                                    <div class="icon-content">
                                        <h3 class="h5">Innovative Thinking</h3>
                                        <p>
                                            We belive in taking the road less travelled while using technology to
                                            shape the future of our businesses and communities.
                                        </p>
                                    </div>
                                </li>
                                <li class="d-flex align-items-start mb-4">
                                    <div class="icon-box bg-dark rounded me-4">
                                        <i class="fas fa-cog text-white"></i>
                                    </div>
                                    <div class="icon-content">
                                        <h3 class="h5">Accountability & Transparency</h3>
                                        <p>
                                            We maintain trust, practise ethics and intergirty to
                                            ensure safety and comfort to all our clients.
                                        </p>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-lg-6 col-md-7">
                        <div class="feature-img-wrap position-relative d-flex flex-column align-items-end">
                            <ul class="img-overlay-list list-unstyled position-absolute">
                                <li class="d-flex align-items-center bg-white rounded shadow-sm p-3">
                                    <i class="fas fa-check bg-primary text-white rounded-circle"></i>
                                    <h6 class="mb-0">Digitizing businesses and communities </h6>
                                </li>
                                <li class="d-flex align-items-center bg-white rounded shadow-sm p-3">
                                    <i class="fas fa-check bg-primary text-white rounded-circle"></i>
                                    <h6 class="mb-0">Providing access to solutions</h6>
                                </li>
                                <li class="d-flex align-items-center bg-white rounded shadow-sm p-3">
                                    <i class="fas fa-check bg-primary text-white rounded-circle"></i>
                                    <h6 class="mb-0">Facilitating development</h6>
                                </li>
                            </ul>
                            <img src="img/image-4.png" alt="feature image" class="img-fluid rounded-custom">
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <!--feature section two end-->

        <!--team section start-->
        {{-- <section id="our-team" class="team-section ptb-120">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-6 col-md-12">
                        <div class="section-heading text-center">
                            <h5 class="h6 text-primary">Our Team</h5>
                            <h2>The People Behind Future Basics</h2>
                            <p>When your mission is scaling,  growth and maximizing efficiency, you need a competent team to support your vision. You need people,
                                digital solutions and strategies that align with your business goals, in short,
                                what we are saying is Our team is your team.
                            </p>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-3 col-md-6">
                        <div class="team-single-wrap mb-5">
                            <div class="team-img rounded-custom">
                                <img src="img/team/p-1.jpg" alt="team" class="img-fluid position-relative">
                                <ul class="list-unstyled team-social-list d-flex flex-column mb-0">
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-linkedin-in"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-twitter"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-github"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-facebook-f"></i></a></li>
                                </ul>
                            </div>
                            <div class="team-info mt-4 text-center">
                                <h5 class="h6 mb-1">Dennis Michael Kilawila</h5>
                                <p class="text-muted small mb-0">Senior Developer/ Founder</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-6">
                        <div class="team-single-wrap mb-5">
                            <div class="team-img rounded-custom">
                                <img src="img/team/p-2.jpg" alt="team" class="img-fluid position-relative">
                                <ul class="list-unstyled team-social-list d-flex flex-column mb-0">
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-linkedin-in"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-twitter"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-github"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-facebook-f"></i></a></li>
                                </ul>
                            </div>
                            <div class="team-info mt-4 text-center">
                                <h5 class="h6 mb-1">Daniel Kikumbo</h5>
                                <p class="text-muted small mb-0">Senior Developer</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-6">
                        <div class="team-single-wrap mb-5">
                            <div class="team-img rounded-custom">
                                <img src="img/team/p-3.jpg" alt="team" class="img-fluid position-relative">
                                <ul class="list-unstyled team-social-list d-flex flex-column mb-0">
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-linkedin-in"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-twitter"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-github"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-facebook-f"></i></a></li>
                                </ul>
                            </div>
                            <div class="team-info mt-4 text-center">
                                <h5 class="h6 mb-1">Felix Msimbo</h5>
                                <p class="text-muted small mb-0">Senior Developers</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-6">
                        <div class="team-single-wrap mb-5">
                            <div class="team-img rounded-custom">
                                <img src="img/team/p-4.jpg" alt="team" class="img-fluid position-relative">
                                <ul class="list-unstyled team-social-list d-flex flex-column mb-0">
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-linkedin-in"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-twitter"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-github"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-facebook-f"></i></a></li>
                                </ul>
                            </div>
                            <div class="team-info mt-4 text-center">
                                <h5 class="h6 mb-1">Emmanuel Kisoki</h5>
                                <p class="text-muted small mb-0">Junior Developer </p>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-6">
                        <div class="team-single-wrap mb-5">
                            <div class="team-img rounded-custom">
                                <img src="img/team/dada.jpg" alt="team" class="img-fluid position-relative">
                                <ul class="list-unstyled team-social-list d-flex flex-column mb-0">
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-linkedin-in"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-twitter"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-github"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-facebook-f"></i></a></li>
                                </ul>
                            </div>
                            <div class="team-info mt-4 text-center">
                                <h5 class="h6 mb-1">Amina Mollel</h5>
                                <p class="text-muted small mb-0">Head of Design/Front End Developer</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-6">
                        <div class="team-single-wrap mb-5">
                            <div class="team-img rounded-custom">
                                <img src="img/team/p-6.jpg" alt="team" class="img-fluid position-relative">
                                <ul class="list-unstyled team-social-list d-flex flex-column mb-0">
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-linkedin-in"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-twitter"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-github"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-facebook-f"></i></a></li>
                                </ul>
                            </div>
                            <div class="team-info mt-4 text-center">
                                <h5 class="h6 mb-1">Jerome Mhinga</h5>
                                <p class="text-muted small mb-0">Junior / Backend Developer</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-6">
                        <div class="team-single-wrap mb-5">
                            <div class="team-img rounded-custom">
                                <img src="img/team/p-7.jpg" alt="team" class="img-fluid position-relative">
                                <ul class="list-unstyled team-social-list d-flex flex-column mb-0">
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-linkedin-in"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-twitter"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-github"></i></a></li>
                                    <li class="list-inline-item"><a href="#"><i class="fab fa-facebook-f"></i></a></li>
                                </ul>
                            </div>
                            <div class="team-info mt-4 text-center">
                                <h5 class="h6 mb-1">Fiona Swai</h5>
                                <p class="text-muted small mb-0">Digital Strategiest</p>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </section> --}}
        <!--team section end-->

        <!--testimonial section start-->
        {{-- <section class="testimonial-section ptb-120 bg-light">
            <div class="container">
                <div class="row justify-content-center align-content-center">
                    <div class="col-md-10 col-lg-6">
                        <div class="section-heading text-center">
                            <h4 class="h5 text-primary">Testimonial</h4>
                            <h2>What They Say About Us</h2>
                            <p>Dynamically initiate market positioning total linkage with clicks-and-mortar technology
                                compelling data for cutting-edge markets.</p>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-12">
                        <div class="position-relative w-100">
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
                                            <h6>Amazing Quiety template!</h6>
                                            Appropriately negotiate interactive niches rather than parallel strategic theme
                                            incubate premium total linkage areas.
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
                                            Rapidiously supply client-centric e-markets and maintainable processes
                                            progressively engineer
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
        <!--testimonial section end-->

        <!--our location address start-->
        {{--<section id="office-location" class="office-address-section ptb-120">
             <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-6 col-md-12">
                        <div class="section-heading text-center">
                            <h4 class="h5 text-primary">Our Office</h4>
                            <h2>Located Around the Country</h2>
                            <p>
                                We are located around Tanzania in multiple regions, we are looking forward to hearing from you. Meet us and lets build a brighter future together.
                            </p>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-3 col-md-6 mt-4 mt-lg-0 mt-xl-0">
                        <div class="rounded-custom border d-block office-address overflow-hidden z-2" style="background: url('img/some/cds.JPG')no-repeat center center / cover">
                            <div class="office-content text-center p-4">
                                <span class="office-overlay"></span>
                                <div class="office-info">
                                    <h5>Dar es salaam</h5>
                                    <address>
                                       Head offices<br> Dar es salaam, Tanzania., <br>Kinondoni, Biafra.
                                    </address>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-6 mt-4 mt-lg-0 mt-xl-0">
                        <div class="rounded-custom border d-block office-address overflow-hidden z-2" style="background: url('img/some/top.JPG')no-repeat center center / cover">
                            <div class="office-content text-center p-4">
                                <span class="office-overlay"></span>
                                <div class="office-info">
                                    <h5>Mwanza</h5>
                                    <address>
                                       Mwanza <br> Bukoba, <br> Ali Hassan road
                                    </address>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-6 mt-4 mt-lg-0 mt-xl-0">
                        <div class="rounded-custom border d-block office-address overflow-hidden z-2" style="background: url('img/some/tbl.JPG')no-repeat center center / cover">
                            <div class="office-content text-center p-4">
                                <span class="office-overlay"></span>
                                <div class="office-info">
                                    <h5>Kilimanjaro</h5>
                                    <address>
                                        Old Moshi <br> Moshi, <br> Tanzania
                                    </address>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-6 mt-4 mt-lg-0 mt-xl-0">
                        <div class="rounded-custom border d-block office-address overflow-hidden z-2" style="background: url('img/some/tina.jpg')no-repeat center center / cover">
                            <div class="office-content text-center p-4">
                                <span class="office-overlay"></span>
                                <div class="office-info">
                                    <h5>Mbeya</h5>
                                     <address>
                                        Brandenburgische Straße <br> DE. Berlin Kreuzberg, <br>Berlin(CA), 10997
                                    </address> -
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>--}}
        <!--our location address end-->

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
                                    Businesses, Communities & Corporations.
                                </p>
                            </div>
                            <div class="form-block-banner mw-60 m-auto mt-5" data-aos="fade-up" data-aos-delay="50">
                                <a href="{{ route('contact-us') }}" class="btn btn-primary">Contact
                                    Us</a>
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
                                            <li><a href="{{ url('/') }}"
                                                    class="text-decoration-none">Home</a></li>
                                            <li><a href="{{ route('about') }}"
                                                    class="text-decoration-none">About Us</a></li>
                                            <li><a href="{{ route('careers-with-us') }}"
                                                    class="text-decoration-none">Join Us</a></li>
                                        </ul>
                                    </div>
                                </div>
                                <div style="display: none;" class="col-md-4 col-lg-4 mt-4 mt-md-0 mt-lg-0">
                                    <div class="footer-single-col">
                                        <h3>Information</h3>
                                        <ul class="list-unstyled footer-nav-list mb-lg-0">
                                            <li><a href="{{ route('coming-soon') }}"
                                                    class="text-decoration-none">Latest news</a></li>
                                            <li><a href="{{ route('coming-soon') }}"
                                                    class="text-decoration-none">Blog</a></li>
                                            {{-- <li><a href="blog.html" class="text-decoration-none">Career</a></li> --}}

                                        </ul>
                                    </div>
                                </div>
                                <div class="col-md-4 col-lg-4 mt-4 mt-md-0 mt-lg-0">
                                    <div class="footer-single-col">
                                        <h3>Quick access</h3>
                                        <ul class="list-unstyled footer-nav-list mb-lg-0">
                                            <li><a href="{{ route('contact-us') }}"
                                                    class="text-decoration-none">Contact us</a></li>
                                            {{-- <li><a href="support.html" class="text-decoration-none">Support</a></li>
                                            <li><a href="support-single.html" class="text-decoration-none">Support center</a></li>
                                            <li><a href="team.html" class="text-decoration-none">Our Team</a></li> --}}
                                            <li><a href="{{ route('careers-with-us') }}"
                                                    class="text-decoration-none">Careers</a>
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
                                    <li class="list-inline-item"><a href="https://wa.me/message/YD7YWU6AS55ZN1"><i
                                                class="fab fa-whatsapp"></i></a></li>
                                    <li class="list-inline-item"><a href="https://www.instagram.com/futurebasicsltd/"><i
                                                class="fab fa-instagram"></i></a></li>
                                    <li class="list-inline-item"><a href="https://twitter.com/futurebasicsltd"><i
                                                class="fab fa-twitter"></i></a></li>
                                    <li class="list-inline-item"><a href="https://github.com/devnechi/fbwebltd.git"><i
                                                class="fab fa-github"></i></a></li>
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
