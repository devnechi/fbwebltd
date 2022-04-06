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
    <title>{{ config('app.name', 'Graphics Services - FutureBasics') }}</title>

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
                                <a class="nav-link dropdown-toggle" href="{{ route('our-services') }}" role="button"
                                    data-bs-toggle="dropdown" aria-expanded="false">Services</a>
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
                                        </div>
                                        <div class="dropdown-grid-item">
                                            <h6 class="drop-heading">Business Solutions</h6>
                                            <a href="{{ route('all-prototyping-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-bolt"></i></span>
                                                <div class="drop-title">Prototyping</div>
                                            </a>
                                            <a href="{{ route('all-software-development-services') }}"
                                                class="dropdown-link">
                                                <span class="me-2"><i class="far fa-bars"></i></span>
                                                <div class="drop-title">Software Eng.</div>
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
                                            <a href="#"><img src="img/about/bs-ppl.jpg" alt="add"
                                                    class="img-fluid rounded-custom" /></a>
                                        </div>
                                    </div>
                                </div>
                            </li>
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="{{ route('business') }}" role="button"
                                    data-bs-toggle="dropdown" aria-expanded="false">Portfolio</a>
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
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-code-branch"></i></span>
                                                <div class="drop-title">Nakwalify</div>
                                            </a>


                                        </div>
                                        <div class="dropdown-grid-item radius-right-side bg-light">
                                            <h6 class="drop-heading">Innovations</h6>
                                            <a href="https://smartrisiti.com/" class="dropdown-link">
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
                            <button type="button" class="close-btn text-danger" data-bs-dismiss="offcanvas"
                                aria-label="Close">
                                <i class="far fa-close"></i>
                            </button>
                        </div>
                        <div class="offcanvas-body">
                            <ul class="nav col-12 col-md-auto justify-content-center main-menu">
                                <li><a href="{{ url('/') }}" class="nav-link">Home</a></li>
                                <li><a href="{{ url('about') }}" class="nav-link">About us</a></li>
                                <li class="nav-item dropdown">
                                    <a class="nav-link dropdown-toggle" href="" {{ route('our-services') }}""
                                        role="button" data-bs-toggle="dropdown" aria-expanded="false">Our Services</a>
                                    <div class="dropdown-menu border-0 rounded-custom shadow py-0 bg-white">
                                        <div class="dropdown-grid rounded-custom width-full-3">
                                            <div class="dropdown-grid-item">
                                                <h6 class="drop-heading">Digital Solutions</h6>
                                                <a href="{{ route('all-graphic-designs-services') }}"
                                                    class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-bars"></i></span>
                                                    <div class="drop-title">Graphics Design</div>
                                                </a>

                                                <a href="{{ route('all-data-science-services') }}"
                                                    class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-code-branch"></i></span>
                                                    <div class="drop-title">Data Science</div>
                                                </a>

                                            </div>
                                            <div class="dropdown-grid-item">
                                                <h6 class="drop-heading">Business Solutions</h6>
                                                <a href="{{ route('all-prototyping-services') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-usd-square"></i></span>
                                                    <div class="drop-title">Prototyping</div>
                                                </a>
                                                <a href="{{ route('all-software-development-services') }}"
                                                    class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-th-list"></i></span>
                                                    <div class="drop-title">Software Eng.</div>
                                                </a>

                                            </div>
                                            <div class="dropdown-grid-item last-item bg-light radius-right-side">
                                                <a href="#"><img src="img/about/bs-ppl.jpg" alt="add"
                                                        class="img-fluid rounded-custom" /></a>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li class="nav-item dropdown">
                                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                                        aria-expanded="false">Portfolio</a>
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
                                                <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-code-branch"></i></span>
                                                    <div class="drop-title">Nakwalify</div>
                                                </a>
                                            </div>
                                            <div class="dropdown-grid-item radius-right-side bg-light">
                                                <h6 class="drop-heading">Innovations</h6>
                                                <a href="https://smartrisiti.com/" class="dropdown-link">
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
                                                    <span class="me-2"><i class="far fa-laptop-code"></i></span>
                                                    <div class="drop-title">Avorra</div>
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                            <div class="action-btns mt-4 ps-3">
                                <a href="{{ route('login') }}" class="btn btn-outline-primary me-2">Sign In</a>
                                <a href="{{ route('contact-us') }}" class="btn btn-primary">Contact us</a>
                            </div>
                        </div>
                    </div>
                    <!--offcanvas menu end-->
                </div>
            </nav>
        </header>
        <!--header section end-->

        <!--page header section start-->
        <section class="page-header position-relative overflow-hidden ptb-120 bg-dark"
            style="background: url('assets/img/page-header-bg.svg')no-repeat bottom left">
            <div class="container">
                <div class="row">
                    <div class="col-lg-8 col-md-12">
                        <h1 class="display-5 fw-bold">Are You a Software Developer?</h1>
                        <p class="lead">

                            Join our pool of developers, programmers, creative designers and innovators to be
                            shortlisted in future projects.
                        </p>
                    </div>
                </div>
                <div class="bg-circle rounded-circle circle-shape-3 position-absolute bg-dark-light right-5"></div>
            </div>
        </section>
        <!--page header section end-->


        <!--faq section start-->
        <section class="faq-section ptb-120">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-7 col-12">
                        <div class="section-heading text-center">
                            <h5 class="h6 text-primary">Developer Details</h5>
                            <h2>Join Our Developer Pool</h2>
                            <p>
                                Developers and Programmers are encourage to fill the form as accurate as possible so as
                                we can accurately assess your best fit with us.
                            </p>
                        </div>
                    </div>
                </div>
                <div class="row justify-content-between">
                    <div class="col-lg-3 col-md-4 d-none d-md-block d-lg-block">
                        <div class="support-article-sidebar sticky-sidebar bg-light rounded-custom p-4 mt-5">
                            <ul class="nav flex-column nav-pills support-article-tab accordion-list w-100">
                                <li class="nav-link"><a href="#dev-personal-info" class="text-decoration-none">Personal
                                        Details</a></li>
                                <li class="nav-link"><a href="#dev-skills-info" class="text-decoration-none"> Skills</a>
                                </li>

                                <li class="nav-link"><a href="#dev-education-info"
                                        class="text-decoration-none">Education</a></li>
                                <li class="nav-link"><a href="#dev-documentaion-upload" class="text-decoration-none">Upload
                                        Documents</a></li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-lg-8 col-md-8">
                        <form action="#" method="post" class="register-form">
                            @csrf
                            <div class="accordion-faq-content-wrap">
                                <div id="dev-personal-info" class="py-4">
                                    <h4>Fill all required areas</h4>
                                    <div class="accordion faq-accordion my-5" id="accordionExample-2">
                                        <div class="accordion-item border border-2 active">
                                            <h5 class="accordion-header" id="faq-2-1">
                                                <button class="accordion-button" type="button" data-bs-toggle="collapse"
                                                    data-bs-target="#collapse-2-1" aria-expanded="true">
                                                    Personal Information
                                                </button>
                                            </h5>
                                            <div id="collapse-2-1" class="accordion-collapse collapse show"
                                                aria-labelledby="faq-2-1" data-bs-parent="#accordionExample-2">
                                                <div class="accordion-body">
                                                    <div class="row">
                                                        <div class="col-sm-6">
                                                            <label for="firstName" class="mb-1">First name <span
                                                                    class="text-danger">*</span></label>
                                                            <div class="input-group mb-3">
                                                                <input type="text" class="form-control" name="firstName"
                                                                    id="firstName" required placeholder="First name"
                                                                    aria-label="First name">
                                                                @error('firstName')
                                                                <span class="invalid-feedback" role="alert">
                                                                    <strong>{{ $message }}</strong>
                                                                </span>
                                                                @enderror
                                                            </div>
                                                        </div>
                                                        <div class="col-sm-6 ">
                                                            <label for="lastName" class="mb-1">Middle name</label>
                                                            <div class="input-group mb-3">
                                                                <input type="text" class="form-control" name="lastName"
                                                                    id="lastName" required placeholder="Middle name"
                                                                    aria-label="Last name">
                                                            </div>
                                                        </div>
                                                        <div class="col-sm-6 ">
                                                            <label for="lastName" class="mb-1">Last name</label>
                                                            <div class="input-group mb-3">
                                                                <input type="text" class="form-control" name="lastName"
                                                                    id="lastName" required placeholder="Last name"
                                                                    aria-label="Last name">
                                                            </div>
                                                        </div>
                                                        <div class="col-sm-6 ">
                                                            <div class="form-group form-control-sm">
                                                                <label for="exampleFormControlSelect1">Gender</label>
                                                                <select class="form-control"
                                                                    id="exampleFormControlSelect1">
                                                                    <option>Select</option>
                                                                    <option>Male</option>
                                                                    <option>Female</option>
                                                                </select>
                                                            </div>
                                                        </div>
                                                        <div class="col-sm-6 ">
                                                            <label for="lastName" class="mb-1">Date of Birth</label>
                                                            <div class="input-group mb-3">
                                                                <input type="date" class="form-control" name="lastName"
                                                                    id="lastName" required placeholder="Date of Birth"
                                                                    aria-label="Last name">
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="accordion-item border border-2">
                                            <h5 class="accordion-header" id="faq-2-2">
                                                <button class="accordion-button collapsed" type="button"
                                                    data-bs-toggle="collapse" data-bs-target="#collapse-2-2"
                                                    aria-expanded="false">
                                                    Contact Information
                                                </button>
                                            </h5>
                                            <div id="collapse-2-2" class="accordion-collapse collapse"
                                                aria-labelledby="faq-2-2" data-bs-parent="#accordionExample-2">
                                                <div class="accordion-body">
                                                    <div class="row">
                                                        <div class="col-sm-6">
                                                            <label for="contactemail" class="mb-1">Email
                                                                @error('contactemail')
                                                                <span class="invalid-feedback" role="alert">
                                                                    <span class="text-danger">*</span>
                                                                </span>
                                                                @enderror
                                                            </label>
                                                            <div class="input-group mb-3">
                                                                <input type="email" class="form-control"
                                                                    name="contactemail" id="contactemail"
                                                                    @error('contactemail') is-invalid @enderror required
                                                                    placeholder="Email" aria-label="Email">
                                                            </div>
                                                        </div>
                                                        <div class="col-sm-6 ">
                                                            <label for="lastName" class="mb-1">Phone Number</label>
                                                            <div class="input-group mb-3">
                                                                <input type="text" class="form-control" name="lastName"
                                                                    id="Phonenumber" required placeholder="Phone Number"
                                                                    aria-label="Last name">
                                                            </div>
                                                        </div>

                                                    </div>

                                                </div>
                                            </div>
                                        </div>

                                    </div>
                                </div>
                                <div id="dev-skills-info" class="py-4">
                                    <h4>Personal Skills</h4>
                                    <div class="accordion faq-accordion my-5" id="accordionExample-3">
                                        <div class="accordion-item border border-2">
                                            <h5 class="accordion-header" id="faq-3-2">
                                                <button class="accordion-button collapsed" type="button"
                                                    data-bs-toggle="collapse" data-bs-target="#collapse-3-2"
                                                    aria-expanded="false">
                                                    Developer Skills
                                                </button>
                                            </h5>
                                            <div id="collapse-3-2" class="accordion-collapse collapse"
                                                aria-labelledby="faq-3-2" data-bs-parent="#accordionExample-3">
                                                <div class="accordion-body">
                                                    <div class="row">
                                                        <div class="col-sm-6 ">
                                                            <div class="form-group form-control-sm">
                                                                <label for="exampleFormControlSelect1">Category</label>
                                                                <select class="form-control"
                                                                    id="exampleFormControlSelect1">
                                                                    <option>Select</option>
                                                                    <option>Full Stack Developer</option>
                                                                    <option>Front-end developer</option>
                                                                    <option>Back-end developer</option>
                                                                    <option>Fairy programmer</option>
                                                                </select>
                                                            </div>
                                                        </div>

                                                    </div>
                                                    {{-- start dynamic fieds --}}
                                                    <div class="row">
                                                        <div class="col-sm-6 ">
                                                            <label for="lastName" class="mb-1">Technical Skills</label>
                                                            <div class="input-group mb-3">
                                                                <input type="text" class="form-control" name="lastName"
                                                                    id="lastName" required
                                                                    placeholder="Ex. React, laravel, java, c#"
                                                                    aria-label="Last name">
                                                            </div>
                                                        </div>
                                                        <div class="col-sm-8">
                                                            <div class="form-group form-control-sm">
                                                                <label for="exampleFormControlSelect1">Level of
                                                                    Technical Skill</label>
                                                                <select class="form-control"
                                                                    id="exampleFormControlSelect1">
                                                                    <option>Select</option>
                                                                    <option>Beginner</option>
                                                                    <option>Intermediate</option>
                                                                    <option>Master</option>
                                                                    <option>Professional</option>
                                                                </select>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    {{-- end dynamic fieds --}}
                                                </div>
                                            </div>
                                        </div>
                                        <div class="accordion-item border border-2">
                                            <h5 class="accordion-header" id="faq-3-3">
                                                <button class="accordion-button collapsed" type="button"
                                                    data-bs-toggle="collapse" data-bs-target="#collapse-3-3"
                                                    aria-expanded="false">
                                                    Work, Portfolio and Socials
                                                </button>
                                            </h5>
                                            <div id="collapse-3-3" class="accordion-collapse collapse"
                                                aria-labelledby="faq-3-3" data-bs-parent="#accordionExample-3">
                                                <div class="accordion-body">
                                                    {{-- start dynamic fieds --}}
                                                    <div class="form-group col-lg-12">
                                                        <div class="form-group multiple-form-group" data-max=6>
                                                            <label for="formGroupExampleInput2">Link to</label>
                                                            <div class="form-group input-group">
                                                                <input type="text" class="form-control"
                                                                    name="phonenumbers[]" placeholder="Ex. github" id="phonenumbers"
                                                                    value="<?= isset($_POST['pobox']) ? $_POST['pobox'] : ''; ?>">

                                                                <label for="formGroupExampleInput2">URL</label>
                                                                <input type="text" class="form-control"
                                                                    name="phonenumbers[]" id="phonenumbers" placeholder="ex. github.com/dev"
                                                                    value="<?= isset($_POST['pobox']) ? $_POST['pobox'] : ''; ?>">
                                                                <a href="#" class="btn btn-primary btn-add ">add +</a>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    {{-- end dynamic fieds --}}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div id="dev-education-info" class="py-4">
                                    <h4>Education Level</h4>
                                    <div class="accordion faq-accordion my-5" id="accordionExample-4">
                                        <div class="accordion-item border border-2">
                                            <h5 class="accordion-header" id="faq-4-4">
                                                <button class="accordion-button collapsed" type="button"
                                                    data-bs-toggle="collapse" data-bs-target="#collapse-4-4"
                                                    aria-expanded="false">
                                                    Education
                                                </button>
                                            </h5>
                                            <div id="collapse-4-4" class="accordion-collapse collapse"
                                                aria-labelledby="faq-4-4" data-bs-parent="#accordionExample-4">
                                                <div class="accordion-body">

                                                    <div class="row">
                                                        <div class="col-sm-6 ">
                                                            <div class="form-group form-control-sm">
                                                                <label for="exampleFormControlSelect1">Level of
                                                                    Education</label>
                                                                <select class="form-control"
                                                                    id="exampleFormControlSelect1">
                                                                    <option>Select</option>
                                                                    <option>Primary</option>
                                                                    <option>Secondary</option>
                                                                    <option>Diploma</option>
                                                                    <option>Barchelors Degree</option>
                                                                    <option>Masters Degree</option>
                                                                    <option>Doctrate</option>
                                                                    <option>Vacational Training</option>

                                                                </select>
                                                            </div>
                                                        </div>
                                                        <div class="col-sm-8">
                                                            <label for="contactemail" class="mb-1">Name of Institution
                                                                @error('contactemail')
                                                                <span class="invalid-feedback" role="alert">
                                                                    <span class="text-danger">*</span>
                                                                </span>
                                                                @enderror
                                                            </label>
                                                            <div class="input-group mb-3">
                                                                <input type="email" class="form-control"
                                                                    name="contactemail" id="contactemail"
                                                                    @error('contactemail') is-invalid @enderror required
                                                                    placeholder="Ex. School" aria-label="Email">
                                                            </div>
                                                        </div>
                                                    </div>

                                                </div>
                                            </div>
                                        </div>


                                    </div>
                                </div>
                                <div id="dev-documentaion-upload" class="py-4">
                                    <h4>Upload Documents</h4>
                                    <div class="accordion faq-accordion my-5" id="accordionExample-4">
                                        <div class="accordion-item border border-2">
                                            <h5 class="accordion-header" id="faq-4-4">
                                                <button class="accordion-button collapsed" type="button"
                                                    data-bs-toggle="collapse" data-bs-target="#collapse-4-6"
                                                    aria-expanded="false">
                                                    Personal Photo
                                                </button>
                                            </h5>
                                            <div id="collapse-4-6" class="accordion-collapse collapse"
                                                aria-labelledby="faq-4-4" data-bs-parent="#accordionExample-4">
                                                <div class="accordion-body">
                                                    <div class="form-group form-control-sm">
                                                        <div class="form-group">
                                                            <label for="exampleFormControlFile1">Select Photo</label>
                                                            <br />
                                                            <input type="file" class="form-control-file"
                                                                id="exampleFormControlFile1">
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="accordion-item border border-2">
                                            <h5 class="accordion-header" id="faq-4-5">
                                                <button class="accordion-button collapsed" type="button"
                                                    data-bs-toggle="collapse" data-bs-target="#collapse-4-5"
                                                    aria-expanded="false">
                                                    Curriculum Vitae
                                                </button>
                                            </h5>
                                            <div id="collapse-4-5" class="accordion-collapse collapse"
                                                aria-labelledby="faq-4-5" data-bs-parent="#accordionExample-4">
                                                <div class="accordion-body">
                                                    <div class="form-group form-control-sm">
                                                        <div class="form-group">
                                                            <label for="exampleFormControlFile1">Upload CV</label>
                                                            <br />
                                                            <input type="file" class="form-control-file"
                                                                id="exampleFormControlFile1">
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="accordion-item border border-2">
                                            <h5 class="accordion-header" id="faq-4-2">
                                                <button class="accordion-button collapsed" type="button"
                                                    data-bs-toggle="collapse" data-bs-target="#collapse-4-2"
                                                    aria-expanded="false">
                                                    Cover Letter
                                                </button>
                                            </h5>
                                            <div id="collapse-4-2" class="accordion-collapse collapse"
                                                aria-labelledby="faq-4-2" data-bs-parent="#accordionExample-4">
                                                <div class="accordion-body">
                                                    <div class="form-group form-control-sm">
                                                        <div class="form-group">
                                                            <label for="exampleFormControlFile1">Upload Cover
                                                                letter</label>
                                                            <br />
                                                            <input type="file" class="form-control-file"
                                                                id="exampleFormControlFile1">
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>

                                    </div>
                                </div>
                            </div>
                            <button type="submit" name="submit" value="submit"
                                class="btn btn-primary mt-4">Submit</button>

                        </form>
                    </div>
                </div>
            </div>
        </section>
        <!--faq section end-->

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
                                            <li><a href="{{ route('about') }}" class="text-decoration-none">About Us</a>
                                            </li>
                                            <li><a href="{{ route('careers-with-us') }}"
                                                    class="text-decoration-none">Join Us</a></li>
                                        </ul>
                                    </div>
                                </div>
                                <div class="col-md-4 col-lg-4 mt-4 mt-md-0 mt-lg-0">
                                    <div class="footer-single-col">
                                        <h3>Information</h3>
                                        <ul class="list-unstyled footer-nav-list mb-lg-0">
                                            <li><a href="{{ route('coming-soon') }}" class="text-decoration-none">Latest
                                                    news</a></li>
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
                                            <li><a href="{{ route('contact-us') }}" class="text-decoration-none">Contact
                                                    us</a></li>
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

    <script>
        (function ($) {
            $(function () {

                var addFormGroup = function (event) {
                    event.preventDefault();

                    var $formGroup = $(this).closest('.form-group');
                    var $multipleFormGroup = $formGroup.closest('.multiple-form-group');
                    var $formGroupClone = $formGroup.clone();

                    $(this)
                        .toggleClass('btn-default btn-add btn-danger btn-remove')
                        .html('–');

                    $formGroupClone.find('input').val('');
                    //
                    $formGroupClone.insertAfter($formGroup);

                    var $lastFormGroupLast = $multipleFormGroup.find('.form-group:last');
                    if ($multipleFormGroup.data('max') <= countFormGroup($multipleFormGroup)) {
                        $lastFormGroupLast.find('.btn-add').attr('disabled', true);
                    }
                };

                var removeFormGroup = function (event) {
                    event.preventDefault();

                    var $formGroup = $(this).closest('.form-group');
                    var $multipleFormGroup = $formGroup.closest('.multiple-form-group');

                    var $lastFormGroupLast = $multipleFormGroup.find('.form-group:last');
                    if ($multipleFormGroup.data('max') >= countFormGroup($multipleFormGroup)) {
                        $lastFormGroupLast.find('.btn-add').attr('disabled', false);
                    }

                    $formGroup.remove();
                };

                var countFormGroup = function ($form) {
                    return $form.find('.form-group').length;
                };

                $(document).on('click', '.btn-add', addFormGroup);
                $(document).on('click', '.btn-remove', removeFormGroup);

            });
        })(jQuery);



        function addob(e) {

            const obv = document.getElementById('pob');
            var n = '<a href="" class=" list-group-item" onclick="remofond(event)">' + obv.value +
                ' <span>&times;</span><input type="hidden" value="' + obv.value + '" name="project_objectives[]"></a>';
            if (obv.value != "") {
                $('.listob').append(n);
                obv.value = "";
            }
        }

    </script>


    <!--endbuild-->
</body>

</html>
