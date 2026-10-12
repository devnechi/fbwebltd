<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

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
    <!--favicon icon-->
    <link rel="icon" href="{{ asset('img/fbicon.png') }}" type="image/png" sizes="16x16">

    <!--title-->
    <title>{{ config('app.name', 'Our services - FutureBasics') }}</title>

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
        <section class="page-header position-relative overflow-hidden ptb-120 bg-dark" style="background: url('img/page-header-bg.svg')no-repeat bottom left">
            <div class="container">
                <div class="row">
                    <div class="col-lg-8 col-md-12">
                        <h1 class="display-5 fw-bold">We are Development Experts</h1>
                        <p class="lead">Seamlessly actualize client-based users after out-of-the-box value. Globally embrace
                            strategic data through frictionless expertise.</p>
                    </div>
                </div>
                <div class="bg-circle rounded-circle circle-shape-3 position-absolute bg-dark-light right-5"></div>
            </div>
        </section>
        <!--page header section end-->

        <!--features grid section start-->
        <section class="feature-section bg-light ptb-120">
            <div class="container">
                <div class="row">
                    <div class="col-12">
                        <div class="feature-grid">
                            <div class="feature-card bg-white shadow-sm highlight-card rounded-custom p-5">
                                <div class="icon-box d-inline-block rounded-circle bg-primary-soft mb-32">
                                    <i class="fal fa-analytics icon-sm text-primary"></i>
                                </div>
                                <div class="feature-content">
                                    <h3 class="h5">Advanced analytics</h3>
                                    <p>Synergistically pursue accurate initiatives without economically sound
                                        imperatives.</p>
                                    <p> Professionally architect unique process improvements via optimal.</p>
                                    <h6 class="mt-4">Included with...</h6>
                                    <ul class="list-unstyled mb-0">
                                        <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>High-converting
                                        </li>
                                        <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Personal
                                            branding
                                        </li>
                                        <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Modernized
                                            prospecting
                                        </li>
                                        <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Clean and
                                            modern
                                        </li>
                                        <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Showcasing
                                            success
                                        </li>
                                        <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Bootstrap
                                            latest version
                                        </li>
                                    </ul>
                                </div>
                                <a href="service-single.html" class="link-with-icon text-decoration-none mt-3">View Details <i
                                        class="far fa-arrow-right"></i></a>
                            </div>
                            <div class="feature-card bg-white shadow-sm rounded-custom p-5">
                                <div class="icon-box d-inline-block rounded-circle bg-success-soft mb-32">
                                    <i class="fal fa-file-chart-line icon-sm text-success"></i>
                                </div>
                                <div class="feature-content">
                                    <h3 class="h5">Automated Reports</h3>
                                    <p class="mb-0">Synergistically pursue accurate initiatives without economically
                                        imperatives.</p>
                                </div>
                                <a href="service-single.html" class="link-with-icon text-decoration-none mt-3">View Details <i
                                        class="far fa-arrow-right"></i></a>
                            </div>
                            <div class="feature-card bg-white shadow-sm rounded-custom p-5">
                                <div class="icon-box d-inline-block rounded-circle bg-danger-soft mb-32">
                                    <i class="fal fa-user-friends icon-sm text-danger"></i>
                                </div>
                                <div class="feature-content">
                                    <h3 class="h5">User Journey Flow</h3>
                                    <p class="mb-0">Quickly productize prospective value before collaborative benefits.</p>
                                </div>
                                <a href="service-single.html" class="link-with-icon text-decoration-none mt-3">View Details <i
                                        class="far fa-arrow-right"></i></a>
                            </div>
                            <div class="feature-card bg-white shadow-sm rounded-custom p-5">
                                <div class="icon-box d-inline-block rounded-circle bg-dark-soft mb-32">
                                    <i class="fal fa-spell-check icon-sm text-dark"></i>
                                </div>
                                <div class="feature-content">
                                    <h3 class="h5">Compare A/B Testing</h3>
                                    <p class="mb-0">Credibly disintermediate functional processes for team driven
                                        action.</p>
                                </div>
                                <a href="service-single.html" class="link-with-icon text-decoration-none mt-3">View Details <i
                                        class="far fa-arrow-right"></i></a>
                            </div>
                            <div class="feature-card bg-white shadow-sm rounded-custom p-5">
                                <div class="icon-box d-inline-block rounded-circle bg-warning-soft mb-32">
                                    <i class="fal fa-cog icon-sm text-warning"></i>
                                </div>
                                <div class="feature-content">
                                    <h3 class="h5">Easy Customization</h3>
                                    <p class="mb-0">Dynamically develop ubiquitous opportunities whereas relationships.</p>
                                </div>
                                <a href="service-single.html" class="link-with-icon text-decoration-none mt-3">View Details <i
                                        class="far fa-arrow-right"></i></a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <!--features grid section end-->

        <!--testimonial section start-->
        <section class="testimonial-section ptb-120">
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
                                        <img src="{{ asset('img/testimonial/quotes-dot.svg') }}" alt="quotes" width="100" class="img-fluid position-absolute left-0 top-0 z--1 p-3">
                                        <div class="d-flex mb-32 align-items-center">
                                            <img src="{{ asset('img/testimonial/1.jpg') }}" class="img-fluid me-3 rounded" width="60" alt="user">
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
                                        <img src="{{ asset('img/testimonial/quotes.svg') }}" alt="quotes" class="position-absolute right-0 bottom-0 z--1 pe-4 pb-4">
                                    </div>
                                    <div class="swiper-slide border border-2 p-5 rounded-custom position-relative">
                                        <img src="{{ asset('img/testimonial/quotes-dot.svg') }}" alt="quotes" width="100" class="img-fluid position-absolute left-0 top-0 z--1 p-3">
                                        <div class="d-flex mb-32 align-items-center">
                                            <img src="{{ asset('img/testimonial/3.jpg') }}" class="img-fluid me-3 rounded" width="60" alt="user">
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
                                        <img src="{{ asset('img/testimonial/quotes.svg') }}" alt="quotes" class="position-absolute right-0 bottom-0 z--1 pe-4 pb-4">
                                    </div>
                                    <div class="swiper-slide border border-2 p-5 rounded-custom position-relative">
                                        <img src="{{ asset('img/testimonial/quotes-dot.svg') }}" alt="quotes" width="100" class="img-fluid position-absolute left-0 top-0 z--1 p-3">
                                        <div class="d-flex mb-32 align-items-center">
                                            <img src="{{ asset('img/testimonial/2.jpg') }}" class="img-fluid me-3 rounded" width="60" alt="user">
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
                                        <img src="{{ asset('img/testimonial/quotes.svg') }}" alt="quotes" class="position-absolute right-0 bottom-0 z--1 pe-4 pb-4">
                                    </div>
                                    <div class="swiper-slide border border-2 p-5 rounded-custom position-relative">
                                        <img src="{{ asset('img/testimonial/quotes-dot.svg') }}" alt="quotes" width="100" class="img-fluid position-absolute left-0 top-0 z--1 p-3">
                                        <div class="d-flex mb-32 align-items-center">
                                            <img src="{{ asset('img/testimonial/4.jpg') }}" class="img-fluid me-3 rounded" width="60" alt="user">
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
                                        <img src="{{ asset('img/testimonial/quotes.svg') }}" alt="quotes" class="position-absolute right-0 bottom-0 z--1 pe-4 pb-4">
                                    </div>
                                    <div class="swiper-slide border border-2 p-5 rounded-custom position-relative">
                                        <img src="{{ asset('img/testimonial/quotes-dot.svg') }}" alt="quotes" width="100" class="img-fluid position-absolute left-0 top-0 z--1 p-3">
                                        <div class="d-flex mb-32 align-items-center">
                                            <img src="{{ asset('img/testimonial/5.jpg') }}" class="img-fluid me-3 rounded" width="60" alt="user">
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
                                        <img src="{{ asset('img/testimonial/quotes.svg') }}" alt="quotes" class="position-absolute right-0 bottom-0 z--1 pe-4 pb-4">
                                    </div>
                                </div>
                            </div>
                            <span class="swiper-button-next"></span>
                            <span class="swiper-button-prev"></span>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <!--testimonial section end-->

        <!--cat subscribe start-->
        <section class="cta-subscribe bg-dark ptb-120 position-relative overflow-hidden">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-8 col-md-10">
                        <div class="subscribe-info-wrap text-center position-relative z-2">
                            <div class="section-heading">
                                <h4 class="h5 text-warning">Let's Try! Get Free Support</h4>
                                <h2>Start Your 14-Day Free Trial</h2>
                                <p>We can help you to create your dream website for better business revenue.</p>
                            </div>
                            <div class="form-block-banner mw-60 m-auto mt-5">
                                <a href="contact-us.html" class="btn btn-primary">Contact with Us</a>
                                <a href="http://www.youtube.com/watch?v=hAP2QF--2Dg" class="text-decoration-none popup-youtube d-inline-flex align-items-center watch-now-btn ms-lg-3 ms-md-3 mt-3 mt-lg-0">
                                    <i
                                            class="fas fa-play"></i> Watch Demo </a>
                            </div>
                            {{-- <ul class="nav justify-content-center subscribe-feature-list mt-4">
                                <li class="nav-item">
                                    <span><i class="far fa-check-circle text-primary me-2"></i>Free 14-day trial</span>
                                </li>
                                <li class="nav-item">
                                    <span><i
                                            class="far fa-check-circle text-primary me-2"></i>No credit card required</span>
                                </li>
                                <li class="nav-item">
                                    <span><i class="far fa-check-circle text-primary me-2"></i>Support 24/7</span>
                                </li>
                                <li class="nav-item">
                                    <span><i class="far fa-check-circle text-primary me-2"></i>Cancel anytime</span>
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
                                <p class="mb-lg-0 mb-md-0">&copy; 2022 Future Basics Company Limited Rights Reserved.</a></p>

                            </div>
                        </div>
                        <div class="col-md-4 col-lg-4">
                            <div class="footer-single-col text-start text-lg-end text-md-end">
                                <ul class="list-unstyled list-inline footer-social-list mb-0">
                                    {{-- <li class="list-inline-item"><a href="#"><i class="fab fa-facebook-f"></i></a></li> --}}
                                    <li class="list-inline-item"><a href="https://wa.me/message/YD7YWU6AS55ZN1s"><i class="fab fa-whatsapp"></i></a></li>
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
