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
    <title>{{ config('app.name', 'Not Found - FutureBasics') }}</title>

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
            <img src="img/fbincon.png" alt="logo" class="img-fluid preloader-icon" />
            <div class="loading-bar"></div>
        </div>
    </div>
    <!--preloader end-->
    <!--main content wrapper start-->
    <div class="main-wrapper">

        <!--404 section start-->
        <section class="error-section ptb-120 bg-dark min-vh-100 w-100 d-flex flex-column justify-content-center" style="background: url('img/page-header-bg.svg')no-repeat bottom right">
            <div class="container">
                <div class="row align-items-center justify-content-center">
                    <div class="col-lg-5 col-md-6">
                        <div class="error-page-content-wrap">
                            <h2 class="error-404 text-warning">404</h2>
                            <h1 class="display-5 fw-bold">Page Not Found</h1>
                            <p class="lead">Efficiently reinvent next-generation scenarios without focused networks. Collaboratively productize superior technology before robust potentialities. </p>

                            <a href="index.html" class="btn btn-primary mt-4">Go Back Home</a>
                        </div>
                    </div>
                    <div class="col-lg-6 col-md-8 mt-5 d-none d-md-block d-lg-block">
                        <div class="hero-img position-relative circle-shape-images">
                            <!--animated shape start-->
                            <ul class="position-absolute animate-element parallax-element circle-shape-list">
                                <li class="layer" data-depth="0.03">
                                    <img src="img/shape/circle-1.svg" alt="shape" class="circle-shape-item type-0 hero-1">
                                </li>
                                <li class="layer" data-depth="0.02">
                                    <img src="img/shape/circle-1.svg" alt="shape" class="circle-shape-item type-1 hero-1">
                                </li>
                                <li class="layer" data-depth="0.04">
                                    <img src="img/shape/circle-1.svg" alt="shape" class="circle-shape-item type-2 hero-1">
                                </li>
                                <li class="layer" data-depth="0.04">
                                    <img src="img/shape/circle-1.svg" alt="shape" class="circle-shape-item type-3 hero-1">
                                </li>
                                <li class="layer" data-depth="0.03">
                                    <img src="img/shape/circle-1.svg" alt="shape" class="circle-shape-item type-4 hero-1">
                                </li>
                                <li class="layer" data-depth="0.03">
                                    <img src="img/shape/circle-1.svg" alt="shape" class="circle-shape-item type-5 hero-1">
                                </li>
                            </ul>
                            <!--animated shape end-->
                            <img src="img/hero-1.png" alt="hero img" class="img-fluid position-relative z-5">
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <!--404 section end-->

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