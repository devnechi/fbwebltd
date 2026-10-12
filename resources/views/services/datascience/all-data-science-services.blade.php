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
    <link rel="icon" href="{{ asset('img/fbicon.png') }}" type="image/png" sizes="16x16">

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
        <section class="page-header position-relative overflow-hidden ptb-120 bg-dark" style="background: url('assets/img/page-header-bg.svg')no-repeat bottom left">
            <div class="container">
                <div class="row">
                    <div class="col-lg-8 col-md-12">
                        <h1 class="display-5 fw-bold">Data Science Services</h1>
                        <p class="lead">
                            Do you want to gain insight on a field, industry, market or business.
                                Make data driven decisions with the use of data analytics along with data mining concepts and tools.</p>

                        </p>
                    </div>
                </div>
                <div class="bg-circle rounded-circle circle-shape-3 position-absolute bg-dark-light right-5"></div>
            </div>
        </section>
        <!--page header section end-->

           <!--features grid section start-->
           <section class="feature-section ptb-120 bg-light">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-6 col-md-10">
                        <div class="section-heading text-center">
                            <h4 class="h5 text-primary">We can help You</h4>
                            <h2> Improve Perfomance By Making Data Driven Decisions</h2>

                            <p>
                               Optimize your competetiveness and efficiency in today's detail-driven world by making
                               effective decisions based on data.
                            </p>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-12">
                        <div class="feature-grid">

                            <div class="feature-card border border-light border-2 rounded-custom p-5">
                                <div class="rounded mb-2 d-flex align-items-center">
                                    <i class="far fa-layer-group fa-2x text-primary me-3"></i>
                                    <h3 class="h5 mb-0">Data science capacity strategies</h3>
                                </div>
                                <div class="feature-content">
                                    <p class="mb-0">
                                        We support businesses to establish
                                         data science potential, capacity
                                         requirements and strategies.
                                        </p>
                                </div>
                                {{-- <a href="service-single.html" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a> --}}
                            </div>
                            <div class="feature-card border border-light border-2 rounded-custom p-5">
                                <div class="rounded mb-2 d-flex align-items-center">
                                    <i class="far fa-user-friends fa-2x text-primary me-3"></i>
                                    <h3 class="h5 mb-0">Data collection strategies</h3>
                                </div>
                                <div class="feature-content">
                                    <p class="mb-0">With a strong team of data analysts we help our clients by developing effective strategies for data collection.</p>
                                </div>
                                {{-- <a href="{{ route('graphic-design-service-details') }}" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a> --}}
                            </div>
                            <div class="feature-card border border-light border-2 rounded-custom p-5">
                                <div class="rounded mb-2 d-flex align-items-center">
                                    <i class="far fa-spell-check fa-2x text-primary me-3"></i>
                                    <h3 class="h5 mb-0">Big Data Mining</h3>
                                </div>
                                <div class="feature-content">
                                    <p class="mb-0">
                                        We support our clients to extract and retrieve data relevant to their business needs.</p>
                                </div>
                                {{-- <a href="service-single.html" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a> --}}
                            </div>
                            <div class="feature-card border border-light border-2 rounded-custom p-5">
                                <div class="rounded mb-2 d-flex align-items-center">
                                    <i class="far fa-cog fa-2x text-primary me-3"></i>
                                    <h3 class="h5 mb-0">Data Modeling</h3>
                                </div>
                                <div class="feature-content">
                                    <p class="mb-0">
                                        We help our clients analyse, define and establish relationships between data
                                        </p>
                                </div>
                                {{-- <a href="service-single.html" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a> --}}
                            </div>
                            {{-- <div class="feature-card border border-light border-2 rounded-custom p-5">
                                <div class="rounded mb-2 d-flex align-items-center">
                                    <i class="far fa-network-wired fa-2x text-primary me-3"></i>
                                    <h3 class="h5 mb-0">Machine  Learning </h3>
                                </div>
                                <div class="feature-content">
                                     <p class="mb-0">
                                        Whether it is for a product,
                                        service, event or raising
                                        awareness, we offer effective
                                        advice and strategies on how to
                                        best carry out the advertisement
                                        and deployment.
                                        </p>
                                </div>
                                <a href="service-single.html" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a>
                            </div> --}}
                            {{-- <div class="feature-card border border-light border-2 rounded-custom p-5">
                                <div class="rounded mb-2 d-flex align-items-center">
                                    <i class="far fa-bezier-curve fa-2x text-primary me-3"></i>
                                    <h3 class="h5 mb-0">Artificial Intelligence</h3>
                                </div>
                                <div class="feature-content">
                                    {{-- <p class="mb-0">
                                        In today's world, packaging is almost
                                        as important as the quality and
                                        content of your product or service.
                                        We design quality packaging that
                                        helps your product or service give
                                        the first impression it deserves.
                                    </p>
                                </div>
                                <a href="service-single.html" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a>
                            </div> --}}
                        </div>
                    </div>
                </div>
            </div>
           </section>
          <!--features grid section end-->

          <!--our work process start-->
          <section class="work-process ptb-120">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-6 col-md-10">
                        <div class="section-heading text-center">
                            <h4 class="h5 text-primary">Process</h4>
                            <h2>Explore Our Data Science Process</h2>
                            <p>Do you want to gain insight on a field, industry, market or business.
                                Make data driven decisions with the use of data analytics and data mining concepts and tools.</p>
                        </div>
                    </div>
                </div>
                <div class="row align-items-center justify-content-between">
                    <div class="col-lg-5 col-md-12 order-1 order-lg-0">
                        <div class="img-wrap">
                            <img src="{{ asset('img/image-5.png') }}" alt="work process" class="img-fluid rounded-custom">
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
                                    <h3 class="h5 mb-2">Data Exploration and Value Extraction Workflow</h3>
                                    <p>
                                        Data is obtained and cleaned of "noise" and rid of in-complete data.
                                         The process entails of data sampling and transformation.
                                    </p>
                                </div>
                            </li>
                            <li class="d-flex align-items-start mb-4">
                                <div class="process-icon-2 border border-2 rounded-custom bg-white me-4 mt-2">
                                    <i class="far fa-bezier-curve fa-2x"></i>
                                </div>
                                <div class="icon-content">
                                    <span class="text-primary h6">Step 2</span>
                                    <h3 class="h5 mb-2">Data Modeling</h3>
                                    <p>
                                        Once the data has been cleaned and prepped,
                                         we implement machine learning algorithms which is where the data is fitted into the model whereby
                                         the model is derived from data selected and business requirement to be fulfilled.
                                    </p>
                                </div>
                            </li>
                            <li class="d-flex align-items-start mb-4">
                                <div class="process-icon-2 border border-2 rounded-custom bg-white me-4 mt-2">
                                    <i class="far fa-layer-group fa-2x"></i>
                                </div>
                                <div class="icon-content">
                                    <span class="text-primary h6">Step 3</span>
                                    <h3 class="h5 mb-2">Testing the Models</h3>
                                    <p>
                                        This is the most critical stage of the process whereby the model is tested
                                         with test data to evaluate the accuracy of data and has relevant desirable properties.
                                         If not xata modelling process is repeated or other alternative approaches are executed.
                                    </p>
                                </div>
                            </li>
                            <li class="d-flex align-items-start mb-4 mb-lg-0">
                                <div class="process-icon-2 border border-2 rounded-custom bg-white me-4 mt-2">
                                    <i class="far fa-truck fa-2x"></i>
                                </div>
                                <div class="icon-content">
                                    <span class="text-primary h6">Step 4</span>
                                    <h3 class="h5 mb-2">Deploy Models</h3>
                                    <p>
                                        The model that produces the accurate results based on the assessed
                                         findings is complete its delivered and deployed in the production environment.
                                    </p>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>
        <!--our work process end-->

   <!--cat subscribe start-->
   <section class="cta-subscribe bg-dark text-white ptb-120 position-relative overflow-hidden">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8 col-md-10">
                <div class="subscribe-info-wrap text-center position-relative z-2">
                    <div class="section-heading" data-aos="fade-up">
                        <h4 class="h5 text-warning">Lets Build Your Data Mining Get Free Support.</h4>
                        <h2>Start Your Data Mining Journey With Us.</h2>
                        <p>We can assist you in building a tailored digital solutions for your business.</p>
                    </div>
                    <div class="form-block-banner mw-60 m-auto mt-5" data-aos="fade-up" data-aos-delay="50">
                        <a href="{{ route('contact-us') }}" class="btn btn-primary">Contact Us</a>
                        {{-- <a href="http://www.youtube.com/watch?v=hAP2QF--2Dg" class="text-decoration-none popup-youtube d-inline-flex align-items-center watch-now-btn ms-lg-3 ms-md-3 mt-3 mt-lg-0"> <i
                                class="fas fa-play"></i> Watch Demo </a> --}}
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
                                <p class="mb-lg-0 mb-md-0">&copy; 2022 Future Basics Company Limited All Rights Reserved.</a></p>

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
