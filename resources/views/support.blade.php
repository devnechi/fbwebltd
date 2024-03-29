<!DOCTYPE html>
<html lang="en">

<head>
    <!--required meta tags-->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">


    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
 <!--twitter og-->
 <meta name="twitter:site" content="@futurebasicsltd">
 <meta name="twitter:creator" content="@futurebasicsltd">
 <meta name="twitter:card" content="summary_large_image">
 <meta name="twitter:title" content="Future Basics - Simplified, Tailored and Innovative Digital Solutions">
 <meta name="twitter:description" content="Future Basics is a digital company bringing simplified digital solution into complex Development Spaces.">
 <meta name="twitter:image" content="#">
 <!--facebook og-->
 <meta property="og:url" content="#">
 <meta name="twitter:title" content="Future Basics - Simplified, Tailored and Innovative Digital Solutions">
 <meta property="og:description" content="Future Basics is a digital company bringing simplified digital solution into complex Development Spaces.">
 <meta property="og:image" content="#">
 <meta property="og:image:secure_url" content="#">
 <meta property="og:image:type" content="image/png">
 <meta property="og:image:width" content="1200">
 <meta property="og:image:height" content="600">
 <!--meta-->
 <meta name="description" content="Basics is a digital company bringing simplified digital solution into complex Development Spaces.">
 <meta name="author" content="ThemeTags">
    <link rel="icon" href="assets/img/favicon.png" type="image/png" sizes="16x16">

    <!--title-->
    <title>Support - Software & IT Solutions HTML Template</title>

    <!--google fonts-->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">

    <!--build:css-->
    <link rel="stylesheet" href="assets/css/main.css">
    <!-- endbuild -->

    <!--custom css start-->
    <link rel="stylesheet" href="assets/css/custom.css">
    <!--custom css end-->

</head>

<body>

    <!--preloader start-->
    <div id="preloader">
        <div class="preloader-wrap">
            <img src="assets/img/favicon.png" alt="logo" class="img-fluid preloader-icon" />
            <div class="loading-bar"></div>
        </div>
    </div>
    <!--preloader end-->
    <!--main content wrapper start-->
    <div class="main-wrapper">

        <!--header section start-->
        <header class="main-header w-100">
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
                <div class="row justify-content-center">
                    <div class="col-lg-8 col-md-12">
                        <div class="text-center">
                            <h1 class="display-5 fw-bold">Support</h1>
                            <p class="lead">Seamlessly actualize client-based users after out-of-the-box value. Globally embrace strategic high-quality platforms before frictionless expertise.</p>

                            <div class="form-block-banner mw-60 m-auto mt-5">
                                <form name="search" class="search-form d-flex">
                                    <input type="email" class="form-control me-2" name="search" data-name="search" placeholder="Search for a topic or question" id="searchForm" required="">
                                    <input type="submit" value="Search" data-wait="Please wait..." class="btn btn-primary">
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="bg-circle rounded-circle circle-shape-3 position-absolute bg-dark-light right-5"></div>
            </div>
        </section>
        <!--page header section end-->


        <!--support content section start-->
        <section class="support-content ptb-120">
            <div class="container">
                <div class="row justify-content-between">
                    <div class="col-lg-4 col-md-4 d-none d-md-block d-lg-block">
                        <div class="support-article-sidebar sticky-sidebar">
                            <div class="nav flex-column nav-pills support-article-tab bg-light rounded-custom p-5" id="v-pills-support" role="tablist" aria-orientation="vertical">
                                <button class="nav-link active" data-bs-target="#support-tab-1" data-bs-toggle="pill" type="button" role="tab" aria-selected="true">All Documentation</button>
                                <button class="nav-link" data-bs-target="#support-tab-2" data-bs-toggle="pill" type="button" role="tab" aria-selected="false">Payments Query</button>
                                <button class="nav-link" data-bs-target="#support-tab-3" data-bs-toggle="pill" type="button" role="tab" aria-selected="false">Setup or Installment</button>
                                <button class="nav-link" data-bs-target="#support-tab-4" data-bs-toggle="pill" type="button" role="tab" aria-selected="false">Technical Support</button>
                                <button class="nav-link" data-bs-target="#support-tab-5" data-bs-toggle="pill" type="button" role="tab" aria-selected="false">Retailers & Customer</button>
                                <button class="nav-link" data-bs-target="#support-tab-6" data-bs-toggle="pill" type="button" role="tab" aria-selected="false">Security Issues</button>
                                <button class="nav-link" data-bs-target="#support-tab-7" data-bs-toggle="pill" type="button" role="tab" aria-selected="false">Brand Creation</button>
                                <button class="nav-link" data-bs-target="#support-tab-8" data-bs-toggle="pill" type="button" role="tab" aria-selected="false">Legal Support</button>
                            </div>
                            <div class="bg-light p-5 mt-4 rounded-custom quick-support">
                                <a href="contact-us.html" class="text-decoration-none text-muted d-flex align-items-center py-2">
                                    <div class="quick-support-icon rounded-circle bg-success-soft me-3">
                                        <i class="far fa-ballot-check text-success"></i>
                                    </div>
                                    <div class="contact-option-text">Quick Support Form</div>
                                </a>
                                <a href="mailto:info@themetags.com" class="text-decoration-none text-muted d-flex align-items-center py-2">
                                    <div class="quick-support-icon rounded-circle bg-primary-soft me-3">
                                        <i class="far fa-envelope text-primary"></i>
                                    </div>
                                    <div class="contact-option-text">info@themetags.com</div>
                                </a>
                                <a href="#" target="_blank" class="text-decoration-none text-muted d-flex align-items-center py-2">
                                    <div class="quick-support-icon rounded-circle bg-danger-soft me-3">
                                        <i class="far fa-comment-alt-lines text-danger"></i>
                                    </div>
                                    <div class="contact-option-text">Live Support Chat</div>
                                </a>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-7 col-md-8">
                        <div class="tab-content" id="v-pills-supportContent">
                            <div class="tab-pane fade show active" id="support-tab-1" role="tabpanel">
                                <div class="support-article-wrap">
                                    <h2>All Support Articles</h2>
                                    <ul class="support-article-list list-unstyled mt-4">
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What is the monthly cost of your app?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Do you have any local branches?</h3>
                                                <p>Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices standardized...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What do I need to create an account?</h3>
                                                <p> Intrinsicly evisculate e-business best practices productivate standardized convergence. Credibly evisculate mission-critical alternative infrastructures with high standards in e-markets...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Are you open for new podcast guests?</h3>
                                                <p>Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">When is the upcoming annual event?</h3>
                                                <p>Intrinsicly evisculate e-business best practices productivate standardized convergence. Rapidiously incubate alternative infrastructures with high standards in e-markets...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What is the monthly cost of your app?</h3>
                                                <p>A lternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Do you offer refunds for the subscriptions?</h3>
                                                <p>Mission-critical products before quality e-services. Rapidiously incubate alternative infrastructures with high standards e-business best practices standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What’s inside the Facebook community?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative infrastructures with high standards in e-markets...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">How often is there a subscribers stream?</h3>
                                                <p>Critical products before quality e-services. Incubate alternative infrastructures with high standards in intrinsicly evisculate e-business best alternative infrastructures practices...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What certifications does Agency has?</h3>
                                                <p>Credibly evisculate mission-critical ncubate alternative infrastructures with high standards in e-markets. e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            <div class="tab-pane fade" id="support-tab-2" role="tabpanel">
                                <div class="support-article-wrap">
                                    <h2>Payments Query</h2>
                                    <ul class="support-article-list list-unstyled">
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Do you offer refunds for the subscriptions?</h3>
                                                <p>Credibly evisculate mission-critical with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What is the monthly cost of your app?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Intrinsicly evisculate e-business best practices ...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Do you have any local branches?</h3>
                                                <p>Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices standardized...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What do I need to create an account?</h3>
                                                <p> Intrinsicly evisculate e-business best practices productivate standardized convergence. Credibly evisculate mission-critical ...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Are you open for new podcast guests?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative infrastructures with high standards in e-markets...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">When is the upcoming annual event?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative e-business best practices productivate standardized...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What is the monthly cost of your app?</h3>
                                                <p>Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What’s inside the Facebook community?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            <div class="tab-pane fade" id="support-tab-3" role="tabpanel">
                                <div class="support-article-wrap">
                                    <h2>Setup or Installment</h2>
                                    <ul class="support-article-list list-unstyled">
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Do you offer refunds for the subscriptions?</h3>
                                                <p>Credibly evisculate mission-critical with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What is the monthly cost of your app?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Intrinsicly evisculate e-business best practices ...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Do you have any local branches?</h3>
                                                <p>Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices standardized...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">When is the upcoming annual event?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative e-business best practices productivate standardized...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What do I need to create an account?</h3>
                                                <p> Intrinsicly evisculate e-business best practices productivate standardized convergence. Credibly evisculate mission-critical ...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Are you open for new podcast guests?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative infrastructures with high standards in e-markets...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What is the monthly cost of your app?</h3>
                                                <p>Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What’s inside the Facebook community?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            <div class="tab-pane fade" id="support-tab-4" role="tabpanel">
                                <div class="support-article-wrap">
                                    <h2>Technical Support</h2>
                                    <ul class="support-article-list list-unstyled">
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Do you have any local branches?</h3>
                                                <p>Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices standardized...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What do I need to create an account?</h3>
                                                <p> Intrinsicly evisculate e-business best practices productivate standardized convergence. Credibly evisculate mission-critical ...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Do you offer refunds for the subscriptions?</h3>
                                                <p>Credibly evisculate mission-critical with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What is the monthly cost of your app?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Intrinsicly evisculate e-business best practices ...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Are you open for new podcast guests?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative infrastructures with high standards in e-markets...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">When is the upcoming annual event?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative e-business best practices productivate standardized...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What is the monthly cost of your app?</h3>
                                                <p>Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What’s inside the Facebook community?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            <div class="tab-pane fade" id="support-tab-5" role="tabpanel">
                                <div class="support-article-wrap">
                                    <h2>Retailers & Customer</h2>
                                    <ul class="support-article-list list-unstyled">
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Do you offer refunds for the subscriptions?</h3>
                                                <p>Credibly evisculate mission-critical with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What is the monthly cost of your app?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Intrinsicly evisculate e-business best practices ...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Do you have any local branches?</h3>
                                                <p>Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices standardized...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What do I need to create an account?</h3>
                                                <p> Intrinsicly evisculate e-business best practices productivate standardized convergence. Credibly evisculate mission-critical ...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Are you open for new podcast guests?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative infrastructures with high standards in e-markets...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">When is the upcoming annual event?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative e-business best practices productivate standardized...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What is the monthly cost of your app?</h3>
                                                <p>Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What’s inside the Facebook community?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            <div class="tab-pane fade" id="support-tab-6" role="tabpanel">
                                <div class="support-article-wrap">
                                    <h2>Security Issues</h2>
                                    <ul class="support-article-list list-unstyled">
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Do you offer refunds for the subscriptions?</h3>
                                                <p>Credibly evisculate mission-critical with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What is the monthly cost of your app?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Intrinsicly evisculate e-business best practices ...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Do you have any local branches?</h3>
                                                <p>Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices standardized...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">When is the upcoming annual event?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative e-business best practices productivate standardized...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What do I need to create an account?</h3>
                                                <p> Intrinsicly evisculate e-business best practices productivate standardized convergence. Credibly evisculate mission-critical ...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Are you open for new podcast guests?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative infrastructures with high standards in e-markets...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What is the monthly cost of your app?</h3>
                                                <p>Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What’s inside the Facebook community?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            <div class="tab-pane fade" id="support-tab-7" role="tabpanel">
                                <div class="support-article-wrap">
                                    <h2>Brand Creation</h2>
                                    <ul class="support-article-list list-unstyled">
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Do you have any local branches?</h3>
                                                <p>Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices standardized...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What do I need to create an account?</h3>
                                                <p> Intrinsicly evisculate e-business best practices productivate standardized convergence. Credibly evisculate mission-critical ...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Do you offer refunds for the subscriptions?</h3>
                                                <p>Credibly evisculate mission-critical with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What is the monthly cost of your app?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Intrinsicly evisculate e-business best practices ...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Are you open for new podcast guests?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative infrastructures with high standards in e-markets...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">When is the upcoming annual event?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative e-business best practices productivate standardized...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What is the monthly cost of your app?</h3>
                                                <p>Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What’s inside the Facebook community?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            <div class="tab-pane fade" id="support-tab-8" role="tabpanel">
                                <div class="support-article-wrap">
                                    <h2>Legal Support</h2>
                                    <ul class="support-article-list list-unstyled">
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Do you have any local branches?</h3>
                                                <p>Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices standardized...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What do I need to create an account?</h3>
                                                <p> Intrinsicly evisculate e-business best practices productivate standardized convergence. Credibly evisculate mission-critical ...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Do you offer refunds for the subscriptions?</h3>
                                                <p>Credibly evisculate mission-critical with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What is the monthly cost of your app?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Intrinsicly evisculate e-business best practices ...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">Are you open for new podcast guests?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative infrastructures with high standards in e-markets...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">When is the upcoming annual event?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative e-business best practices productivate standardized...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What is the monthly cost of your app?</h3>
                                                <p>Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                        <li class="py-4 border-top border-light">
                                            <a href="support-single.html" class="text-decoration-none d-block text-muted">
                                                <h3 class="h5 support-article-title">What’s inside the Facebook community?</h3>
                                                <p>Credibly evisculate mission-critical products before quality e-services. Rapidiously incubate alternative infrastructures with high standards in e-markets. Intrinsicly evisculate e-business best practices productivate standardized convergence...</p>
                                                <span class="btn-link text-decoration-none read-more-link">Read More <i class="far fa-arrow-right ms-2"></i></span>
                                            </a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <!--support content section end-->


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
                                            <li><a href="{{ route('business') }}" class="text-decoration-none">Services</a></li>
                                            <li><a href="{{ route('careers-with-us') }}" class="text-decoration-none">Our Portfolio</a></li>
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
                                            {{-- <li><a href="{{ route('careers-with-us') }}" class="text-decoration-none">Careers</a> --}}
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
    <script src="assets/js/vendors/jquery-3.6.0.min.js"></script>
    <script src="assets/js/vendors/bootstrap.bundle.min.js"></script>
    <script src="assets/js/vendors/swiper-bundle.min.js"></script>
    <script src="assets/js/vendors/jquery.magnific-popup.min.js"></script>
    <script src="assets/js/vendors/parallax.min.js"></script>
    <script src="assets/js/vendors/aos.js"></script>
    <script src="assets/js/app.js"></script>
    <!--endbuild-->
</body>

</html>
