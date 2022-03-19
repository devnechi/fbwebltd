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
    {{-- <div id="preloader">
        <div class="preloader-wrap">
            <img src="img/fbicon.png" alt="logo" class="img-fluid preloader-icon" />
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
                                        </div>
                                        <div class="dropdown-grid-item">
                                            <h6 class="drop-heading">Business Solutions</h6>
                                            <a href="{{ route('all-prototyping-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-bolt"></i></span>
                                                <div class="drop-title">Prototyping</div>
                                            </a>
                                            <a href="{{ route('all-software-development-services') }}" class="dropdown-link">
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

                                            </div>
                                            <div class="dropdown-grid-item">
                                                <h6 class="drop-heading">Business Solutions</h6>
                                                <a href="{{ route('all-prototyping-services') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-usd-square"></i></span>
                                                    <div class="drop-title">Prototyping</div>
                                                </a>
                                                <a href="{{ route('all-software-development-services') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-th-list"></i></span>
                                                    <div class="drop-title">Software Eng.</div>
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
                </div>
            </nav>
        </header>
        <!--header section end-->

        <!--page header section start-->
        <section class="page-header position-relative overflow-hidden ptb-120 bg-dark" style="background: url('assets/img/page-header-bg.svg')no-repeat bottom left">
            <div class="container">
                <div class="row">
                    <div class="col-lg-8 col-md-12">
                        <h1 class="display-5 fw-bold">Quality Graphic Design Services</h1>
                        <p class="lead">
                            Future Basics is a full-service digital design firm with a constant understanding that people's needs and desires are ever-changing, For us we are committed in a world of constant change to create actionable and sustainable solutions that offer a competitive edge to our partners.
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
                            <h4 class="h5 text-primary">How we can help</h4>
                            <h2>Impactful Design Services for Your Business</h2>
                            <p>
                                Our designs are the epitome of our company values we blend creativity and innovation to create  thoughtful and interactive solutions,
                                 which evidently support our partners  Large, Medium and Small, Year after Year.
                            </p>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-12">
                        <div class="feature-grid">
                            <div class="feature-card border border-light border-2 rounded-custom p-5">
                                <div class="rounded mb-2 d-flex align-items-center">
                                    <i class="far fa-user-friends fa-2x text-primary me-3"></i>
                                    <h3 class="h5 mb-0">Logos and Branding</h3>
                                </div>
                                <div class="feature-content">
                                    <p class="mb-0">All Major brands logos are the first impression of the company, We've narrowed it to a science, a process of building logos that are unforgettable and sustain themselves over time.</p>
                                </div>
                                <a href="{{ route('graphic-design-service-details') }}" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a>
                            </div>
                            <div class="feature-card border border-light border-2 rounded-custom p-5">
                                <div class="rounded mb-2 d-flex align-items-center">
                                    <i class="far fa-spell-check fa-2x text-primary me-3"></i>
                                    <h3 class="h5 mb-0">Info-graphics Design</h3>
                                </div>
                                <div class="feature-content">
                                    <p class="mb-0">
                                        Its well known High-quality info-graphics are more likely to be read than blunt Text, We understand the need to properly convey ideas and information visually in away that appeals to the intended user.</p>
                                </div>
                                <a href="service-single.html" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a>
                            </div>
                            <div class="feature-card border border-light border-2 rounded-custom p-5">
                                <div class="rounded mb-2 d-flex align-items-center">
                                    <i class="far fa-cog fa-2x text-primary me-3"></i>
                                    <h3 class="h5 mb-0">Printing & Publishing</h3>
                                </div>
                                <div class="feature-content">
                                    <p class="mb-0">
                                        We'll ensure that your print persona - from posters, reports, brochures to invitations to personalized cards - communicate your message to increase customer convention.</p>
                                </div>
                                <a href="service-single.html" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a>
                            </div>
                            <div class="feature-card border border-light border-2 rounded-custom p-5">
                                <div class="rounded mb-2 d-flex align-items-center">
                                    <i class="far fa-network-wired fa-2x text-primary me-3"></i>
                                    <h3 class="h5 mb-0">Digital Advertising and Marketing </h3>
                                </div>
                                <div class="feature-content">
                                    <p class="mb-0">Whether its for  a product, magazine, poster, or billboard creative designs play a major role in your marketing and advertising strategy, we at FBC can create ads that are both engaging and speak for you.</p>
                                </div>
                                <a href="service-single.html" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a>
                            </div>
                            <div class="feature-card border border-light border-2 rounded-custom p-5">
                                <div class="rounded mb-2 d-flex align-items-center">
                                    <i class="far fa-layer-group fa-2x text-primary me-3"></i>
                                    <h3 class="h5 mb-0">Content Creation</h3>
                                </div>
                                <div class="feature-content">
                                    <p class="mb-0">
                                        We'll assist you in crafting your intended message, help you target the right audience and help you build a interactive community around your content objective.</p>
                                </div>
                                <a href="service-single.html" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a>
                            </div>
                            <div class="feature-card border border-light border-2 rounded-custom p-5">
                                <div class="rounded mb-2 d-flex align-items-center">
                                    <i class="far fa-bezier-curve fa-2x text-primary me-3"></i>
                                    <h3 class="h5 mb-0">Packaging Design</h3>
                                </div>
                                <div class="feature-content">
                                    <p class="mb-0">Its actually true  although many don't admit that people do judge a book by its cover and products by its package. We can make your first impression memorable and enticing.</p>
                                </div>
                                <a href="service-single.html" class="link-with-icon text-decoration-none mt-4">View Details <i class="far fa-arrow-right"></i></a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
           </section>
          <!--features grid section end-->


             <!--footer section start-->
            <footer class="footer-section">
                <!--footer top start-->
                <!--for light footer add .footer-light class and for dark footer add .bg-dark .text-white class-->
                <div class="footer-top bg-dark text-white ptb-120">
                    <div class="container">
                        <div class="row justify-content-between">
                            <div class="col-md-8 col-lg-4 mb-md-4 mb-lg-0">
                                <div class="footer-single-col">
                                    <div class="footer-single-col mb-4">
                                        <img src="img/fb_og_logo.png" alt="logo" class="img-fluid logo-white">
                                        <img src="img/fb_og_logo_drk.png" alt="logo" class="img-fluid logo-color">
                                    </div>
                                    <p>Our latest news, articles, and resources, we will sent to
                                        your inbox weekly.</p>

                                    <form class="newsletter-form position-relative d-block d-lg-flex d-md-flex">
                                        <input type="text" class="input-newsletter form-control me-2" placeholder="Enter your email" name="email" required="" autocomplete="off">
                                        <input type="submit" value="Subscribe" data-wait="Please wait..." class="btn btn-primary mt-3 mt-lg-0 mt-md-0">
                                    </form>
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
                                    <div class="col-md-4 col-lg-4 mt-4 mt-md-0 mt-lg-0">
                                        <div class="footer-single-col">
                                            <h3>Information</h3>
                                            <ul class="list-unstyled footer-nav-list mb-lg-0">
                                                <li><a href="blog-single.html" class="text-decoration-none">Latest news</a></li>
                                                <li><a href="pricing.html" class="text-decoration-none">Blog</a></li>
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
                <div class="footer-bottom bg-dark text-white py-4">
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
                                        <li class="list-inline-item"><a href="#"><i class="fab fa-facebook-f"></i></a></li>
                                        <li class="list-inline-item"><a href="#"><i class="fab fa-instagram"></i></a></li>
                                        <li class="list-inline-item"><a href="#"><i class="fab fa-twitter"></i></a></li>
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
