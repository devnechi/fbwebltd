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
        @include('partials.public-navigation', ['navVariant' => 'light'])
        <!--header section end-->

        <!--page header section start-->
        <section class="page-header position-relative overflow-hidden ptb-120 bg-dark" style="background: url('assets/img/page-header-bg.svg')no-repeat bottom left">
            <div class="container">
                <div class="row">
                    <div class="col-lg-8 col-md-12">
                        <h1 class="display-5 fw-bold">Business System Development Services</h1>
                        <p class="lead">
                            Digitizing your business has never been
                            more essential. We develop custom-made
                            softwares that automate processes
                            throughout your business thus improving
                            business performance and efficiency.
                        </p>
                    </div>
                </div>
                <div class="bg-circle rounded-circle circle-shape-3 position-absolute bg-dark-light right-5"></div>
            </div>
        </section>
        <!--page header section end-->


            <!--feature tab section start-->
            <section class="feature-tab-section ptb-120 bg-light">
                <div class="container">
                    <div class="row justify-content-center align-content-center">
                        <div class="col-md-10 col-lg-8">
                            <div class="section-heading text-center mb-4">
                                {{-- <h5 class="h6 text-primary">Features</h5> --}}
                                <h2>Developing Systems That Take Your Business
                                    To The Next Level</h2>
                                <p>
                                    Improve business performance and
                                    efficiency by implementing tailor-made
                                    software in your business processes.
                                    </p>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-12">
                            <ul class="nav justify-content-center feature-tab-list-2 mt-4" id="nav-tab-2" role="tablist">
                                <li class="nav-item">
                                    <a class="nav-link active" href="#tab-2-1" data-bs-toggle="tab" data-bs-target="#tab-2-1" role="tab" aria-selected="false">
                                        Intranet business systems
                                    </a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="#tab-2-2" data-bs-toggle="tab" data-bs-target="#tab-2-2" role="tab" aria-selected="false">
                                        Extranet business systems
                                    </a>
                                </li>

                            </ul>
                            <div class="tab-content" id="nav-tabContent-2">
                                <div class="tab-pane fade pt-60 active show" id="tab-2-1" role="tabpanel">
                                    <div class="row justify-content-center align-items-center justify-content-around">
                                        <div class="col-lg-12">
                                            <div class="feature-tab-info">
                                                <h3>Intranet System Tools</h3>
                                                <br />
                                                <br />
                                                <br />
                                                    <div class="row">
                                                        <div class="col-12">
                                                            <div class="feature-grid">
                                                                <div class="feature-card border border-light border-2 rounded-custom p-5">
                                                                    <div class="rounded mb-2 d-flex align-items-center">
                                                                        <i class="far fa-user-friends fa-2x text-primary me-3"></i>
                                                                        <h3 class="h5 mb-0">HR Systems</h3>
                                                                    </div>
                                                                    <div class="feature-content">
                                                                        <p class="mb-0">
                                                                            Software that helps you
                                                                            handle your humna resource
                                                                            digitally.

                                                                        </p>
                                                                    </div>
                                                                    {{-- <a href="{{ route('graphic-design-service-details') }}" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a> --}}
                                                                </div>
                                                                <div class="feature-card border border-light border-2 rounded-custom p-5">
                                                                    <div class="rounded mb-2 d-flex align-items-center">
                                                                        <i class="far fa-spell-check fa-2x text-primary me-3"></i>
                                                                        <h3 class="h5 mb-0">Point Of Sale Systems</h3>
                                                                    </div>
                                                                    <div class="feature-content">
                                                                        <p class="mb-0">
                                                                            Revolutionise the way your
                                                                            business handles sale
                                                                            transactions.
                                                                        </p>
                                                                    </div>
                                                                    {{-- <a href="service-single.html" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a> --}}
                                                                </div>
                                                                <div class="feature-card border border-light border-2 rounded-custom p-5">
                                                                    <div class="rounded mb-2 d-flex align-items-center">
                                                                        <i class="far fa-cog fa-2x text-primary me-3"></i>
                                                                        <h3 class="h5 mb-0">Per Request Systems</h3>
                                                                    </div>
                                                                    <div class="feature-content">
                                                                        <p class="mb-0">
                                                                            In collaboration with you, we
                                                                            develop software precisely
                                                                            aimed at your specific needs.
                                                                            </p>
                                                                    </div>
                                                                    {{-- <a href="service-single.html" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a> --}}
                                                                </div>
                                                                <div class="feature-card border border-light border-2 rounded-custom p-5">
                                                                    <div class="rounded mb-2 d-flex align-items-center">
                                                                        <i class="far fa-network-wired fa-2x text-primary me-3"></i>
                                                                        <h3 class="h5 mb-0">Project & Field Monitoring Systems </h3>
                                                                    </div>
                                                                    <div class="feature-content">
                                                                        <p class="mb-0">
                                                                            Digitally track your remote field
                                                                            projects from wherever you are
                                                                            with precision and ease.
                                                                            </p>
                                                                    </div>
                                                                    {{-- <a href="service-single.html" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a> --}}
                                                                </div>
                                                                <div class="feature-card border border-light border-2 rounded-custom p-5">
                                                                    <div class="rounded mb-2 d-flex align-items-center">
                                                                        <i class="far fa-layer-group fa-2x text-primary me-3"></i>
                                                                        <h3 class="h5 mb-0">Business Data Systems</h3>
                                                                    </div>
                                                                    <div class="feature-content">
                                                                        <p class="mb-0">
                                                                            Easily collect, store and analyse
                                                                            valuable business data in oder to
                                                                            effectively evaluate and monitor
                                                                            your business.
                                                                            </p>
                                                                    </div>
                                                                    {{-- <a href="service-single.html" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a> --}}
                                                                </div>
                                                                <div class="feature-card border border-light border-2 rounded-custom p-5">
                                                                    <div class="rounded mb-2 d-flex align-items-center">
                                                                        <i class="far fa-bezier-curve fa-2x text-primary me-3"></i>
                                                                        <h3 class="h5 mb-0">Business Management Systems</h3>
                                                                    </div>
                                                                    <div class="feature-content">
                                                                        <p class="mb-0">
                                                                            Software that helps you easily
                                                                            manage you rbusiness from all
                                                                            aspects.
                                                                        </p>
                                                                    </div>
                                                                    {{-- <a href="service-single.html" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a> --}}
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                            </div>
                                        </div>

                                    </div>
                                </div>
                                <div class="tab-pane fade pt-60" id="tab-2-2" role="tabpanel">
                                    <div class="row justify-content-center align-items-center justify-content-around">

                                        <div class="col-lg-12">
                                            <div class="feature-tab-info">
                                                <h3>Extranet system</h3>
                                                <br />
                                                <br />
                                                <br />
                                                    <div class="row">
                                                        <div class="col-12">
                                                            <div class="feature-grid">
                                                                <div class="feature-card border border-light border-2 rounded-custom p-5">
                                                                    <div class="rounded mb-2 d-flex align-items-center">
                                                                        <i class="far fa-user-friends fa-2x text-primary me-3"></i>
                                                                        <h3 class="h5 mb-0">HR Systems</h3>
                                                                    </div>
                                                                    <div class="feature-content">
                                                                        <p class="mb-0">
                                                                            Software that helps you
                                                                            handle your humna resource
                                                                            digitally.

                                                                        </p>
                                                                    </div>
                                                                    {{-- <a href="{{ route('graphic-design-service-details') }}" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a> --}}
                                                                </div>
                                                                <div class="feature-card border border-light border-2 rounded-custom p-5">
                                                                    <div class="rounded mb-2 d-flex align-items-center">
                                                                        <i class="far fa-spell-check fa-2x text-primary me-3"></i>
                                                                        <h3 class="h5 mb-0">Point Of Sale Systems</h3>
                                                                    </div>
                                                                    <div class="feature-content">
                                                                        <p class="mb-0">
                                                                            Revolutionise the way your
                                                                            business handles sale
                                                                            transactions.
                                                                        </p>
                                                                    </div>
                                                                    {{-- <a href="service-single.html" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a> --}}
                                                                </div>
                                                                <div class="feature-card border border-light border-2 rounded-custom p-5">
                                                                    <div class="rounded mb-2 d-flex align-items-center">
                                                                        <i class="far fa-cog fa-2x text-primary me-3"></i>
                                                                        <h3 class="h5 mb-0">Per Request Systems</h3>
                                                                    </div>
                                                                    <div class="feature-content">
                                                                        <p class="mb-0">
                                                                            In collaboration with you, we
                                                                            develop software precisely
                                                                            aimed at your specific needs.
                                                                            </p>
                                                                    </div>
                                                                    {{-- <a href="service-single.html" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a> --}}
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                            </div>
                        </div>
                    </div>
                </div>
            </section>
            <!--feature tab section end-->

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

                            </div>

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
            <div class="footer-top  footer-light ptb-120">
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
            <div class="footer-bottom  footer-light py-4">
                <div class="container">
                    <div class="row justify-content-between align-items-center">
                        <div class="col-md-7 col-lg-7">
                            <div class="copyright-text">
                                {{-- <p class="mb-lg-0 mb-md-0">&copy; 2021 Future Basics Rights Reserved. Designed By <a href="https://futurebasics.co.tz" class="text-decoration-none">Future </a></p> --}}
                                <p class="mb-lg-0 mb-md-0">&copy; 2022 Future Basics Company Limited Rights Reserved.</a></p>

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
