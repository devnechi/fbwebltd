<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

    <meta name="keywords" content="Development space，Radarmile, Livestoka, Technology, Innovations">
    <meta name="description"
        content="Future Basics is a digital company bringing simplified digital solution into complex Development Space">
    {{-- <meta name="viewport"
        content="width=device-width, initial-scale=1.0, user-scalable=0, minimum-scale=1.0, maximum-scale=1.0"> --}}
    <meta name="format-detection" content="telephone=no">
    <meta http-equiv="X-UA-Compatible" content="IE=Edge">

    <!--twitter og-->
    <meta name="twitter:site" content="@themetags">
    <meta name="twitter:creator" content="@themetags">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Quiety - Creative SAAS Technology & IT Solutions Bootstrap 5 HTML Template">
    <meta name="twitter:description" content="Quiety creative Saas, software technology, Saas agency & business Bootstrap 5 Html template. It is best and famous software company and Saas website template.">
    <meta name="twitter:image" content="#">

    <!--facebook og-->
    <meta property="og:url" content="#">
    <meta name="twitter:title" content="Quiety - Creative SAAS Technology & IT Solutions Bootstrap 5 HTML Template">
    <meta property="og:description" content="Quiety creative Saas, software technology, Saas agency & business Bootstrap 5 Html template. It is best and famous software company and Saas website template.">
    <meta property="og:image" content="#">
    <meta property="og:image:secure_url" content="#">
    <meta property="og:image:type" content="image/png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="600">

    <!--meta-->
    <meta name="description" content="Quiety creative Saas, software technology, Saas agency & business Bootstrap 5 Html template. It is best and famous software company and Saas website template.">
    <meta name="author" content="ThemeTags">

    <!--favicon icon-->
    <link rel="icon" href="img/fbicon.png" type="image/png" sizes="16x16">

    <!--title-->
    <title>{{ config('app.name', 'FutureBasics') }}</title>

    <!--google fonts-->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">

    <!--build:css-->
    {{-- <link rel="stylesheet" href="css/main.css"> --}}
    <link href="{{ asset('css/main.css') }}" rel="stylesheet">
    {{-- <link href="{{ asset('css/app.css') }}" rel="stylesheet"> --}}

    <!-- endbuild -->

    <!--custom css start-->
    {{-- <link rel="stylesheet" href="css/custom.css"> --}}
    <link href="{{ asset('css/custom.css') }}" rel="stylesheet">

    <!--custom css end-->
    <script src="{{ asset('js/app.js') }}"></script>


</head>

<body>

    <!--preloader start-->
    {{-- <div id="preloader">
        <div class="preloader-wrap">
            <img src="img/favicon.png" alt="logo" class="img-fluid preloader-icon" />
            <div class="loading-bar"></div>
        </div>
    </div> --}}
    <!--preloader end-->
    <!--main content wrapper start-->
    <div class="main-wrapper">

        <!--header section start-->
        <header class="main-header w-100">
            <nav class="navbar navbar-expand-xl navbar-light sticky-header">
                <div class="container d-flex align-items-center justify-content-lg-between position-relative">
                    <a href="{{ url('/') }}" class="navbar-brand d-flex align-items-center mb-md-0 text-decoration-none">
                        <img src="img/fb_og_logo.png" alt="logo" class="img-fluid logo-white" />
                        <img src="img/fb_og_logo.png" alt="logo" class="img-fluid logo-color" />
                    </a>

                    <a class="navbar-toggler position-absolute right-0 border-0" href="#offcanvasWithBackdrop" role="button">
                        <span class="far fa-bars" data-bs-toggle="offcanvas" data-bs-target="#offcanvasWithBackdrop" aria-controls="offcanvasWithBackdrop"></span>
                    </a>
                    <div class="clearfix"></div>
                    <div class="collapse navbar-collapse justify-content-center">
                        <ul class="nav col-12 col-md-auto justify-content-center main-menu">
                            <li><a href="{{ url('/') }}" class="nav-link">Home</a></li>
                            {{-- <li><a href="{{ route('about') }}" class="nav-link">About us</a></li> --}}
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="{{ route('about') }}" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                    About us
                                </a>
                                <div class=" dropdown-menu border-0 rounded-custom shadow py-0 bg-white">
                                    <div class="dropdown-grid rounded-custom width-half">
                                        <div class="dropdown-grid-item">
                                            <h6 class="drop-heading">More about us</h6>
                                            <a href="{{ route('about') }}#valuenmission" class="dropdown-link">
                                                <span class="demo-list bg-primary rounded text-white fw-bold">1</span>
                                                <div class="dropdown-info">
                                                    <div class="drop-title">Vision & Mission</div>
                                                    {{-- <p>It's for <strong>SaaS Software</strong> Company</p> --}}
                                                </div>
                                            </a>
                                            <a href="{{ route('about') }}#our-team" class="dropdown-link">
                                                <span class="demo-list bg-primary rounded text-white fw-bold">2</span>
                                                <div class="dropdown-info">
                                                    <div class="drop-title">Our Team</div>
                                                    {{-- <p>Modern <strong>Saas agency</strong></p> --}}
                                                </div>
                                            </a>
                                            <a href="{{ route('about') }}" class="dropdown-link">
                                                <span class="demo-list bg-primary rounded text-white fw-bold">2</span>
                                                <div class="dropdown-info">
                                                    <div class="drop-title">Our Culture</div>
                                                    {{-- <p>Modern <strong>Saas agency</strong></p> --}}
                                                </div>
                                            </a>
                                            <a href="{{ route('about') }}#office-location" class="dropdown-link">
                                                <span class="demo-list bg-primary rounded text-white fw-bold">3</span>
                                                <div class="dropdown-info">
                                                    <div class="drop-title">Our Offices</div>
                                                    {{-- <p><strong>Web Software</strong> Company</p> --}}
                                                </div>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </li>
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Services</a>
                                <div class="dropdown-menu border-0 rounded-custom shadow py-0 bg-white">
                                    <div class="dropdown-grid rounded-custom width-full-3">
                                        <div class="dropdown-grid-item">
                                            <h6 class="drop-heading">Digital Solutions</h6>
                                            <a href="{{ route('business') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-eject"></i></span>
                                                <div class="drop-title">Graphic Design</div>
                                            </a>
                                            <a href="{{ route('business') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-bolt"></i></span>
                                                <div class="drop-title">Design & Prototyping</div>
                                            </a>
                                            <a href="{{ route('business') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-bars"></i></span>
                                                <div class="drop-title">Desktop applications Development</div>
                                            </a>

                                            <a href="{{ route('business') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-browser"></i></span>
                                                <div class="drop-title">Web applications Development</div>
                                            </a>
                                            <a href="{{ route('business') }}" class="dropdown-link">
                                                <span class="me-2" ><i class="far fa-address-card"></i></span>
                                                <div class="drop-title">Mobile applications Development</div>
                                            </a>


                                            <a href="{{ route('business') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-closed-captioning"></i></span>
                                                <div class="drop-title">Data Mining & Data Science</div>
                                            </a>


                                        </div>
                                        <div class="dropdown-grid-item">
                                            <h6 class="drop-heading">Business Solutions</h6>
                                            <a href="{{ route('our-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-usd-square"></i></span>
                                                <div class="drop-title">Business System Analysis</div>
                                            </a>
                                            <a href="{{ route('our-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-th-list"></i></span>
                                                <div class="drop-title">Business Processes Administration</div>
                                            </a>
                                            <a href="{{ route('our-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-chart-network"></i></span>
                                                <div class="drop-title">Data Analytics</div>
                                            </a>

                                            <a href="{{ route('our-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-paper-plane"></i></span>
                                                <div class="drop-title">Digital Strategy Fomulation</div>
                                            </a>
                                            <a href="{{ route('our-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-th-large"></i></span>
                                                <div class="drop-title">Business Systems Development</div>
                                            </a>

                                            <a href="{{ route('our-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-user"></i></span>
                                                <div class="drop-title">AI/ML Model Development</div>
                                            </a>
                                        </div>
                                        <div class="dropdown-grid-item last-item bg-light radius-right-side">
                                            <a href="#"><img src="img/about/bs-ppl.jpg" alt="add" class="img-fluid rounded-custom" /></a>
                                        </div>
                                    </div>
                                </div>
                            </li>
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="{{ route('business') }}" role="button" data-bs-toggle="dropdown" aria-expanded="false">Portfolio</a>
                                <div class="dropdown-menu border-0 rounded-custom shadow py-0 bg-white">
                                    <div class="dropdown-grid rounded-custom width-full">
                                        <div class="dropdown-grid-item">
                                            <h6 class="drop-heading">Enterprise Solutions</h6>
                                            <a href="{{ route('business') }}" class="dropdown-link px-0">
                                                <span class="me-2"><i class="far fa-fingerprint"></i></span>
                                                <div class="drop-title">Livestoka</div>
                                            </a>
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link px-0">
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
                                            <a href="{{ route('business') }}" class="dropdown-link">
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
                                <button type="button" class="close-btn text-danger" data-bs-dismiss="offcanvas" aria-label="Close">
                                    <i class="far fa-close"></i>
                                </button>
                            </div>
                            <div class="offcanvas-body">
                                <ul class="nav col-12 col-md-auto justify-content-center main-menu">
                                    <li><a href="{{ url('/') }}" class="nav-link">Home</a></li>

                                    <li class="nav-item dropdown">
                                        <a class="nav-link dropdown-toggle" href="{{ route('about') }}" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                            about us
                                        </a>
                                        <div class=" dropdown-menu border-0 rounded-custom shadow py-0 bg-white">
                                            <div class="dropdown-grid rounded-custom width-half">
                                                <div class="dropdown-grid-item">
                                                    <h6 class="drop-heading">More about us</h6>
                                                    <a href="{{ route('about') }}#valuenmission" class="dropdown-link">
                                                        <span class="demo-list bg-primary rounded text-white fw-bold">1</span>
                                                        <div class="dropdown-info">
                                                            <div class="drop-title">Vision & Mission</div>
                                                        </div>
                                                    </a>
                                                    <a href="{{ route('about') }}#our-team" class="dropdown-link">
                                                        <span class="demo-list bg-primary rounded text-white fw-bold">2</span>
                                                        <div class="dropdown-info">
                                                            <div class="drop-title">Our Team</div>
                                                            {{-- <p>Modern <strong>Saas agency</strong></p> --}}
                                                        </div>
                                                    </a>
                                                    <a href="{{ route('about') }}" class="dropdown-link">
                                                        <span class="demo-list bg-primary rounded text-white fw-bold">3</span>
                                                        <div class="dropdown-info">
                                                            <div class="drop-title">Our Culture</div>
                                                            {{-- <p><strong>Web Software</strong> Company</p> --}}
                                                        </div>
                                                    </a>
                                                    <a href="{{ route('about') }}#office-location" class="dropdown-link">
                                                        <span class="demo-list bg-primary rounded text-white fw-bold">4</span>
                                                        <div class="dropdown-info">
                                                            <div class="drop-title">Our Offices</div>
                                                            {{-- <p>App and <strong>Software</strong> Landing</p> --}}
                                                        </div>
                                                    </a>
                                                </div>
                                            </div>
                                        </div>
                                    </li>
                                    <li class="nav-item dropdown">
                                        <a class="nav-link dropdown-toggle" href=""{{ route('our-services') }}"" role="button" data-bs-toggle="dropdown" aria-expanded="false">Our Services</a>
                                        <div class="dropdown-menu border-0 rounded-custom shadow py-0 bg-white">
                                            <div class="dropdown-grid rounded-custom width-full-3">
                                                <div class="dropdown-grid-item">
                                                    <h6 class="drop-heading">Digital Solutions</h6>
                                                    <a href={{ route('business') }}" class="dropdown-link">
                                                        <span class="me-2"><i class="far fa-bars"></i></span>
                                                        <div class="drop-title">Graphic Design</div>
                                                    </a>
                                                    <a href={{ route('business') }}" class="dropdown-link">
                                                        <span class="me-2"><i class="far fa-browser"></i></span>
                                                        <div class="drop-title">Design & Prototyping</div>
                                                    </a>
                                                    <a href={{ route('business') }}" class="dropdown-link">
                                                        <span class="me-2" ><i class="far fa-address-card"></i></span>
                                                        <div class="drop-title">Desktop applications Development</div>
                                                    </a>
                                                    <a href={{ route('business') }}" class="dropdown-link">
                                                        <span class="me-2"><i class="far fa-bolt"></i></span>
                                                        <div class="drop-title">Web applications Development</div>
                                                    </a>
                                                    <a href={{ route('business') }}" class="dropdown-link">
                                                        <span class="me-2"><i class="far fa-eject"></i></span>
                                                        <div class="drop-title">Mobile applications Development</div>
                                                    </a>
                                                    <a href={{ route('business') }}" class="dropdown-link">
                                                        <span class="me-2"><i class="far fa-code-branch"></i></span>
                                                        <div class="drop-title">Data Mining & Data Science</div>
                                                    </a>

                                                </div>
                                                <div class="dropdown-grid-item">
                                                    <h6 class="drop-heading">Business Solutions</h6>
                                                    <a href="{{ route('our-services') }}" class="dropdown-link">
                                                        <span class="me-2"><i class="far fa-usd-square"></i></span>
                                                        <div class="drop-title">Business System Analysis</div>
                                                    </a>
                                                    <a href="{{ route('our-services') }}" class="dropdown-link">
                                                        <span class="me-2"><i class="far fa-th-list"></i></span>
                                                        <div class="drop-title">Business Processes Administration</div>
                                                    </a>
                                                    <a href="{{ route('our-services') }}" class="dropdown-link">
                                                        <span class="me-2"><i class="far fa-chart-network"></i></span>
                                                        <div class="drop-title">Data Analytics</div>
                                                    </a>
                                                    <a href="{{ route('our-services') }}" class="dropdown-link">
                                                        <span class="me-2"><i class="far fa-closed-captioning"></i></span>
                                                        <div class="drop-title">Digital Strategy Fomulation</div>
                                                    </a>

                                                    <a href="{{ route('our-services') }}" class="dropdown-link">
                                                        <span class="me-2"><i class="far fa-user"></i></span>
                                                        <div class="drop-title">Business Systems Development</div>
                                                    </a>
                                                    <a href="{{ route('our-services') }}" class="dropdown-link">
                                                        <span class="me-2"><i class="far fa-paper-plane"></i></span>
                                                        <div class="drop-title">AI/ML Model Development</div>
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
                                                    <a href="https/:www.livestoka.com" class="dropdown-link px-0">
                                                        <span class="me-2" ><i class="far fa-fingerprint"></i></span>
                                                        <div class="drop-title">Livestoka</div>
                                                    </a>
                                                    <a href="{{ route('coming-soon') }}" class="dropdown-link px-0">
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
                                                    <a href="{{ route('business') }}" class="dropdown-link">
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

      <!--Navbar -->
     {{-- <main class="py-4"> --}}
      @yield('content')
      {{-- end of content --}}

{{-- </main> --}}

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
