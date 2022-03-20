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
    <link rel="icon" href="img/fbicon.png" type="image/png" sizes="16x16">

    <!--title-->
    <title>{{ config('app.name', 'Coming soon - FutureBasics') }}</title>

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


        <!--coming soon section start-->
        <section class="coming-soon-section min-vh-100 ptb-120 overflow-hidden position-relative w-100 d-flex flex-column justify-content-center" style="background: url('img/page-header-bg.svg')no-repeat bottom right">
            <div class="bg-dark fixed-bg"></div>
            <div class="container">
                <div class="row">
                    <div class="col-lg-5 col-12">
                        <div class="coming-soon-content-wrap position-relative z-2">
                            <a href="{{ url('/') }}" class="mb-5 d-block"><img src="img/fb_og_logo.png" alt="logo" class="img-fluid"></a>

                            <h5 class="text-white">We are Coming Soon...</h5>
                            <h1 class="text-white">We are Working Our New Website, Please Stay With us!</h1>
                            <div class="action-btns">
                                {{-- <a href="#notify-form" class="btn btn-primary mt-5 popup-with-form">Notify Me!</a> --}}
                                {{-- <a href="https://futurebasics.co.tz/contact-us" class="btn btn-primary mt-5 popup-with-form">Notify Me!</a> --}}
                                <a href="{{ route('contact-us') }}" class="btn btn-primary">Contact Us</a>

                            </div>

                            <div class="social-list-wrap mt-100">
                                <ul class="list-unstyled author-social-list social-bg-ts list-inline mb-0">
                                    <li class="list-inline-item"><a href="https://www.instagram.com/futurebasicsltd/"><i class="fab fa-instagram"></i></a></li>
                                    <li class="list-inline-item"><a href="https://twitter.com/futurebasicsltd"><i class="fab fa-twitter"></i></a></li>
                                    <li class="list-inline-item"><a href="https://github.com/devnechi/fbwebltd.git""><i class="fab fa-github"></i></a></li>
                                    {{-- <li class="list-inline-item"><a href="#"><i class="fab fa-facebook-f"></i></a></li> --}}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
                <!--popup form start-->
                <div id="notify-form" class="mfp-hide white-popup-block  rounded-custom bg-white p-5">
                    <div class="subscribe-info-wrap text-center position-relative z-2">
                        <div class="section-heading">
                            <h3>Subscribe for Latest News and Updated!</h3>
                            <p>We can help you to create your dream website for better business revenue.</p>
                        </div>
                        <div class="form-block-banner mw-60 m-auto">
                            <form id="email-form2" name="email-form" class="subscribe-form d-flex">
                                <input type="email" class="form-control me-2" name="Email" data-name="Email" placeholder="Your email" id="Email2" required="">
                                <input type="submit" value="Subscribe!" data-wait="Please wait..." class="btn btn-primary">
                            </form>
                        </div>
                        {{-- <ul class="nav justify-content-center subscribe-feature-list mt-3">
                            <li class="nav-item">
                                <span><i class="fad fa-dot-circle text-primary me-2"></i>No credit card required</span>
                            </li>
                            <li class="nav-item">
                                <span><i class="fad fa-dot-circle text-primary me-2"></i>Support 24/7</span>
                            </li>
                            <li class="nav-item">
                                <span><i class="fad fa-dot-circle text-primary me-2"></i>Cancel anytime</span>
                            </li>
                        </ul> --}}
                    </div>
                </div>
                <!--popup form end-->
            </div>

            <ul class="animated-circle list-unstyled z--1">
                <li class="transition-delay-1 bg-danger"></li>
                <li class="transition-delay-2 bg-warning"></li>
                <li class="transition-delay-3 bg-primary"></li>
            </ul>
        </section>
        <!--coming soon section end-->

    </div>
    <!--main content wrapper end-->

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
