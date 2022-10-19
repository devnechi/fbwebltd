<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

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
    <link rel="icon" href="img/fbicon.png" type="image/png" sizes="16x16">

    <!--title-->
    <title>{{ config('app.name', 'Graphics Services - FutureBasics') }}</title>

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

        <!--page header section start-->
        <section class="page-header position-relative overflow-hidden ptb-120 bg-dark" style="background: url('assets/img/page-header-bg.svg')no-repeat bottom left">
            <div class="container">
                <div class="row">
                    <div class="col-lg-8 col-md-12">
                        <h1 class="display-5 fw-bold">Mobile Application Development Services</h1>
                        <p class="lead">
                            With our profound knowledge in modern
                            technologies, along with a creative and
                            dedicated team of experts, we design and
                            develop software tailored to your needs that
                            helps you achieve your goals more efficiently.</p>
                    </div>
                </div>
                <div class="bg-circle rounded-circle circle-shape-3 position-absolute bg-dark-light right-5"></div>
            </div>
        </section>
        <!--page header section end-->

        <!--services section start-->
        <section class="services-section ptb-120">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-6 col-md-10">
                        <div class="section-heading text-center">
                            {{-- <h4 class="h5 text-primary">Software development services</h4> --}}
                            <h2>Offering Mobile Application Development For Everyone</h2>
                            <p>
                                We offer software solutions for clients at
                                individual, business and corporate level
                                regardless of their industry or size.
                            </p>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-12">
                        <div class="position-relative w-100">
                            <div class="feature-grid position-relative">
                                <div class="feature-card border-line-style px-5 my-4">
                                    <div class="feature-icon rounded bg-primary mb-32">
                                        <i class="fal fa-share-alt fa-2x text-white"></i>
                                    </div>
                                    <div class="feature-content">
                                        <h3 class="h5">Android Applications Development</h3>
                                        <p>
                                            We design and develop a wide range of
                                            robust high quality applications that are
                                            compatible across all devices and platforms.
                                            We provide guidance and leadership
                                            throughout the entire development process
                                            from ideation, to data gathering and
                                            development.
                                        </p>
                                        <h6 class="mt-4">Development in...</h6>
                                        <ul class="list-unstyled mb-0">
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Intranet and Extranet Solutions</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Web applications</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Mobile applications</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Desktop applications</li>
                                        </ul>
                                    </div>
                                    <span class="border-line"></span>
                                </div>
                                <div class="feature-card border-line-style px-5 my-4">
                                    <div class="feature-icon rounded bg-danger mb-32">
                                        <i class="fal fa-file-chart-line fa-2x text-white"></i>
                                    </div>
                                    <div class="feature-content">
                                        <h3 class="h5">iOS Applications Development</h3>
                                        <p class="mb-0">
                                            We implement security protocols into every development solution to guarantee that our products are infallible and operate in secure environments.
                                            Our security protocols align with the legislation, industry-specific standards, and the corporate policies in place.
                                        </p>
                                        <h6 class="mt-4">Include...</h6>
                                        <ul class="list-unstyled mb-0">
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Operational security</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Infrastructure security</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Application security</li>
                                        </ul>
                                    </div>
                                    <span class="border-line"></span>
                                </div>
                                <div class="feature-card border-line-style px-5 my-4">
                                    <div class="feature-icon rounded bg-dark mb-32">
                                        <i class="fal fa-sync-alt fa-2x text-white"></i>
                                    </div>
                                    <div class="feature-content">
                                        <h3 class="h5">Hybrid/Native Mobile Applications</h3>
                                        <p class="mb-0">
                                            We provide development services to a wide
                                            range of clients. Whether you have idea that
                                            requires materialisation or need help with
                                            maintaining or upgrading your software, we
                                            are happy to offer our services at any stage of
                                            the process.
                                        </p>
                                        <h6 class="mt-4">Included with...</h6>
                                        <ul class="list-unstyled mb-0">
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Product consulting</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Product UX design</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>MVP development</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>In-product analytics</li>

                                        </ul>
                                    </div>
                                    <span class="border-line"></span>
                                </div>
                                <div class="feature-card border-line-style px-5 my-4">
                                    <div class="feature-icon rounded bg-success mb-32">
                                        <i class="fal fa-spell-check fa-2x text-white"></i>
                                    </div>
                                    <div class="feature-content">
                                        <h3 class="h5">Cross device Applications</h3>
                                        <p class="mb-0">
                                            We believe in quality, therefore we offer
                                            Quliaty Assurance (QA) Testing services that
                                            ensure your digital products are of the
                                            highest standard possible, thus ensuring
                                            better user experience and product
                                            performance.
                                        </p>
                                        <h6 class="mt-4">Tests Included...</h6>
                                        <ul class="list-unstyled mb-0">
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Ads A/B Testing</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>CR Optimization</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Content Optimization</li>
                                        </ul>
                                    </div>
                                    <span class="border-line"></span>
                                </div>
                                {{-- <div class="feature-card border-line-style px-5 my-4">
                                    <div class="feature-icon rounded bg-primary mb-32">
                                        <i class="fal fa-chart-pie fa-2x text-white"></i>
                                    </div>
                                    <div class="feature-content">
                                        <h3 class="h5">Advanced Analytics</h3>
                                        <p class="mb-0">Synergistically pursue accurate initiatives without economically sound
                                            imperatives. Professionally architect unique.</p>
                                        <h6 class="mt-4">Included with...</h6>
                                        <ul class="list-unstyled mb-0">
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Goals, Targets Setup</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Users Analytics</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Optimization Content</li>
                                        </ul>
                                    </div>
                                    <span class="border-line"></span>
                                </div> --}}
                                {{-- <div class="feature-card border-line-style px-5 my-4">
                                    <div class="feature-icon rounded bg-warning mb-32">
                                        <i class="fal fa-filter fa-2x text-white"></i>
                                    </div>
                                    <div class="feature-content">
                                        <h3 class="h5">Multi-page Applications</h3>
                                        <p class="mb-0">
                                            We assist clients with the maintenance of
                                        their IT software and infrastructure. We help
                                        them to continoulsy optimize their IT
                                        structures and performance.
                                        </p>
                                        <h6 class="mt-4">Maintaince in...</h6>
                                        <ul class="list-unstyled mb-0">
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Existing software</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Developed software</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Adopted software </li>
                                        </ul>
                                    </div>
                                    <span class="border-line"></span>
                                </div> --}}
                            </div>

                        </div>
                    </div>
                </div>
            </div>
        </section>
        <!--services section end-->

          {{-- <!--our work process start-->
          <section class="work-process ptb-120">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-6 col-md-10">
                        <div class="section-heading text-center">
                            <h4 class="h5 text-primary">Our Process</h4>
                            <h2> Our Development Process</h2>
                            <p>
                                We utilize best practices and efficient methodologies for software engineering,
                                 that guide us during the development process in a structured and systematic way.</p>
                        </div>
                    </div>
                </div>
                <div class="row align-items-center justify-content-between">
                    <div class="col-lg-5 col-md-12 order-1 order-lg-0">
                        <div class="img-wrap">
                            <img src="img/se.png" alt="work process" class="img-fluid rounded-custom">
                        </div>
                    </div>
                    <div class="col-lg-6 col-md-12 order-0 order-lg-1">
                        <ul class="work-process-list list-unstyled">
                            <li class="d-flex align-items-start mb-4">
                                <div class="process-icon-2 border border-2 rounded-custom bg-white me-4 mt-2">
                                    <i class="far fa-folder-tree fa-2x"></i>
                                </div>
                                <div class="icon-content">
                                    <span class="text-primary h6">Step 1</span>
                                    <h3 class="h5 mb-2">Research and Data gathering</h3>
                                    <p>
                                        We collect all relevant data, evaluate the goal of the solution and collect required feedback
                                         from stakeholders or anyone who stands to benefit from the digital solution.
                                    </p>
                                </div>
                            </li>
                            <li class="d-flex align-items-start mb-4">
                                <div class="process-icon-2 border border-2 rounded-custom bg-white me-4 mt-2">
                                    <i class="far fa-bezier-curve fa-2x"></i>
                                </div>
                                <div class="icon-content">
                                    <span class="text-primary h6">Step 2</span>
                                    <h3 class="h5 mb-2"> Defining</h3>
                                    <p>
                                        Once the data is gathered and business processes are identified,
                                        the next step is to define and document the requirements and architecture of the proposed software.
                                    </p>
                                </div>
                            </li>
                            <li class="d-flex align-items-start mb-4">
                                <div class="process-icon-2 border border-2 rounded-custom bg-white me-4 mt-2">
                                    <i class="far fa-solid fa-compass-drafting fa-2x"></i>
                                </div>
                                <div class="icon-content">
                                    <span class="text-primary h6">Step 3</span>
                                    <h3 class="h5 mb-2">Designing & Wireframing</h3>
                                    <p>
                                        Once the system requirements are
                                        documented and approved, the illustrations
                                        that will visualize the software are then
                                        designed. The aim is to produce an iteractive
                                        prototype that provides a look and feel of the
                                        final product.
                                    </p>
                                </div>
                            </li>
                            <li class="d-flex align-items-start mb-4 mb-lg-0">
                                <div class="process-icon-2 border border-2 rounded-custom bg-white me-4 mt-2">
                                    <i class="far fa-solid fa-code fa-2x"></i>
                                </div>
                                <div class="icon-content">
                                    <span class="text-primary h6">Step 4</span>
                                    <h3 class="h5 mb-2">Development</h3>
                                    <p>
                                        After a prototype is finalised, the
                                        development process of materialising the
                                        prototype into a fully funtctional software
                                        product begins. This step uses the most
                                        effective tools and technologies chosen
                                        carefully by our experts.
                                    </p>
                                </div>
                            </li>
                            <li class="d-flex align-items-start mb-4 mb-lg-0">
                                <div class="process-icon-2 border border-2 rounded-custom bg-white me-4 mt-2">
                                    <i class="far fa-solid fa-microscope fa-2x"></i>
                                </div>
                                <div class="icon-content">
                                    <span class="text-primary h6">Step 5</span>
                                    <h3 class="h5 mb-2">Testing</h3>
                                    <p>
                                        In this crucial step the developed software is
                                        evaluated and put through tests that aim to
                                        find and fix; errors, bugs and defects so to
                                        ensure the system functions as required.
                                    </p>
                                </div>
                            </li>
                            <li class="d-flex align-items-start mb-4 mb-lg-0">
                                <div class="process-icon-2 border border-2 rounded-custom bg-white me-4 mt-2">
                                    <i class="far fa-solid fa-rocket-launch fa-2x"></i>
                                </div>
                                <div class="icon-content">
                                    <span class="text-primary h6">Step 6</span>
                                    <h3 class="h5 mb-2">Deployment</h3>
                                    <p>
                                        Here the system is launched and made
                                        available for the target audience to use. The
                                        deployment process is also monitored
                                        closely, and any arising issues are attend to.

                                        </p>
                                </div>
                            </li>
                            <li class="d-flex align-items-start mb-4 mb-lg-0">
                                <div class="process-icon-2 border border-2 rounded-custom bg-white me-4 mt-2">
                                    <i class="far fa-solid fa-arrows-repeat fa-2x"></i>
                                </div>
                                <div class="icon-content">
                                    <span class="text-primary h6">Step 7</span>
                                    <h3 class="h5 mb-2">Maintenance & Up-keep</h3>
                                    <p>
                                        Once the software is deployed, we provide
                                        our clients with maintenance and up-keep
                                        services as this is another crucial element in
                                        the life span of a software. During this phase,
                                        the software is maintained and impoved
                                        accordingly.
                                    </p>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
          </section>
          <!--our work process end--> --}}

                  <!--footer section start-->
        <footer class="footer-section">
            <!--footer top start-->
            <!--for light footer add .footer-light class and for dark footer add .bg-dark .text-white class-->
            <div class="footer-top  bg-dark text-white ptb-120">
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
            <div class="footer-bottom  bg-dark text-white py-4">
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
