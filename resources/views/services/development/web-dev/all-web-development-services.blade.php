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
                        <h1 class="display-5 fw-bold">Website Design & Development Services</h1>
                        <p class="lead">
                         Website design and development tailored to your needs.
                        </p>
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
                            <h2>Get A Website That Makes You Stand Out</h2>
                            <p>
                                Your brand and business deserve effective
                                and professionally aesthetic websites that
                                assure quality to your customers
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
                                        <i class="fal fa-repeat-1 fa-2x text-white"></i>
                                    </div>
                                    <div class="feature-content">
                                        <h3 class="h5">Static Website</h3>
                                        <p>
                                            Using the most up-to-date
                                            technologies,we develop
                                            high performing static
                                            websites that help you
                                            professionally showcase
                                            your brand and business
                                            online.
                                        </p>
                                        <h6 class="mt-4">Advantages of Static websites</h6>
                                        <ul class="list-unstyled mb-0">
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Faster page loading speed</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Quick creation</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Potential for enhanced security</li>
                                        </ul>
                                    </div>
                                    <span class="border-line"></span>
                                </div>
                                <div class="feature-card border-line-style px-5 my-4">
                                    <div class="feature-icon rounded bg-danger mb-32">
                                        <i class="fal fa-rectangle-vertical-history fa-2x text-white"></i>
                                    </div>
                                    <div class="feature-content">
                                        <h3 class="h5">Dynamic Website</h3>
                                        <p class="mb-0">
                                            Showcase your brand and business with more detail while
                                            giving your customers a better user experience with the
                                            use of dynamic websites.
                                        </p>
                                        <p class="mb-0">
                                            Using the latest technologies, we develop tailor-made
                                            websites that help you do exactly that.
                                        </p>
                                        <h6 class="mt-4">Advantages of Dynamic websites</h6>
                                        <ul class="list-unstyled mb-0">
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Easily updated</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Better user experience</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Greater functionality</li>
                                        </ul>
                                    </div>
                                    <span class="border-line"></span>
                                </div>
                                <div class="feature-card border-line-style px-5 my-4">
                                    <div class="feature-icon rounded bg-dark mb-32">
                                        <i class="fal fa-folder-grid fa-2x text-white"></i>
                                    </div>
                                    <div class="feature-content">
                                        <h3 class="h5">Hybrid Website</h3>
                                        <p class="mb-0">
                                            As websites are becoming more complex, increasing the
                                            demand formore functionality and better performance
                                            from our clients we take a hybrid approach towards
                                            developing your website.
                                        </p>
                                        <p class="mb-0">
                                            We design strategies that combine the implementation of
                                            both static and dynamic features into your website giving
                                            you the best of both worlds.
                                        </p>
                                        {{-- <h6 class="mt-4">Included with...</h6>
                                        <ul class="list-unstyled mb-0">
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Product consulting</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>Product UX design</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>MVP development</li>
                                            <li class="py-1"><i class="fad fa-check-circle me-2 text-primary"></i>In-product analytics</li>

                                        </ul> --}}
                                    </div>
                                    <span class="border-line"></span>
                                </div>
                                {{-- <div class="feature-card border-line-style px-5 my-4">
                                    <div class="feature-icon rounded bg-success mb-32">
                                        <i class="fal fa-arrow-trend-up fa-2x text-white"></i>
                                    </div>
                                    <div class="feature-content">
                                        <h3 class="h5">Progressive Web Applications (PWA's)</h3>
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
                                <div class="feature-card border-line-style px-5 my-4">
                                    <div class="feature-icon rounded bg-warning mb-32">
                                        <i class="fal fa-files fa-2x text-white"></i>
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
