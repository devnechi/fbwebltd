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
    <title>{{ config('app.name', 'Careers - FutureBasics') }}</title>

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
                                            <a href="{{ route('all-graphic-designs-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-globe"></i></span>
                                                <div class="drop-title">Website Development</div>
                                            </a>

                                            <a href="{{ route('all-data-science-services') }}" class="dropdown-link">
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
                                                <span class="me-2"><i class="far fa-bars"></i></span>
                                                <div class="drop-title">Software Eng.</div>
                                            </a>
                                            <a href="{{ route('all-graphic-designs-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-globe"></i></span>
                                                <div class="drop-title">Website Development</div>
                                            </a>

                                            <a href="{{ route('all-data-science-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-mobile"></i></span>
                                                <div class="drop-title">Mobile App Development</div>
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
                                                <a href="{{ route('all-graphic-designs-services') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-globe"></i></span>
                                                    <div class="drop-title">Website Development</div>
                                                </a>

                                                <a href="{{ route('all-data-science-services') }}" class="dropdown-link">
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
                                                    <div class="drop-title">Software Eng.</div>
                                                </a>
                                                <a href="{{ route('all-graphic-designs-services') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-globe"></i></span>
                                                    <div class="drop-title">Website Development</div>
                                                </a>

                                                <a href="{{ route('all-data-science-services') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-mobile"></i></span>
                                                    <div class="drop-title">Mobile App Development</div>
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
        <section class="page-header position-relative overflow-hidden ptb-120 bg-dark" style="background: url('img/page-header-bg.svg')no-repeat bottom left">
            <div class="container">
                <div class="row justify-content-between align-items-center">
                    <div class="col-lg-8 col-12">
                        <div class="company-info-wrap">
                            <div class="company-logo p-4 bg-white shadow rounded-custom me-4 mt-2">
                                <div class="logo">
                                    <img src="img/company/2.png" alt="company logo" class="img-fluid">
                                </div>
                            </div>
                            <div class="company-overview">
                                <h1 class="display-5 fw-bold">Senior Backend Developer</h1>

                                <h6>About The Company</h6>
                                <ul class="list-unstyled list-inline mb-0 mt-3">
                                    <li class="list-inline-item me-4"><i class="far fa-house-building me-2"></i> Google</li>
                                    <li class="list-inline-item me-4">

                                        <div class="star-rating">
                                            <i class="far fa-smile me-2"></i>
                                            <span class="fas fa-star small text-warning"></span>
                                            <span class="fas fa-star small text-warning"></span>
                                            <span class="fas fa-star small text-warning"></span>
                                            <span class="fas fa-star small text-warning"></span>
                                            <span class="fas fa-star small text-warning"></span>
                                        </div>
                                    </li>
                                    <li class="list-inline-item me-4"><i class="far fa-map-marker-alt me-2"></i>United
                                        Kingdom
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-12">
                        <div class="annual-salary-wrap rounded-custom">
                            <h6>Annual Salary</h6>
                            <span class="display-6 fw-semi-bold text-dark mb-0">$35k - $38k</span>
                        </div>
                    </div>
                </div>

                <div class="bg-circle rounded-circle circle-shape-3 position-absolute bg-dark-light right-5"></div>
            </div>
        </section>
        <!--page header section end-->

        <!--job details section start-->
        <section class="job-details ptb-120">
            <div class="container">
                <div class="row justify-content-between">
                    <div class="col-lg-8 pe-lg-5">
                        <div class="job-details-wrap">
                            <h2>Job Details</h2>
                            <p>Objectively restore stand-alone markets rather than enterprise-wide products. Uniquely
                                underwhelm best-of-breed mindshare through adaptive niches. Seamlessly parallel task
                                open-source content without resource sucking technology.
                            </p>
                            <div class="job-details-info mt-5">
                                <h3 class="h5">Job Responsibilities</h3>
                                <ul class="content-list list-unstyled">
                                    <li>Be involved in every step of the product design cycle from discovery and user
                                        acceptance testing.
                                    </li>
                                    <li>Work with BAs, product managers and tech teams to lead the Product Design</li>
                                    <li>Maintain quality of the design process and ensure that when designs are translated
                                        into code they accurately.
                                    </li>
                                    <li>Accurately estimate design tickets during planning sessions.</li>
                                    <li>Contribute to sketching sessions involving non-designersCreate, and pattern
                                        libraries.
                                    </li>
                                    <li>Design pixel perfect responsive UI’s and understand that adopting common interface
                                    </li>
                                    <li>Interface patterns is better for UX than reinventing the wheel</li>
                                </ul>
                            </div>
                            <div class="job-details-info mt-5">
                                <h3 class="h5">Job Requirements</h3>
                                <ul class="content-list list-unstyled">
                                    <li>Interactively plagiarize covalent "outside the box" thinking vis-a-vis.</li>
                                    <li>Holisticly communicate integrated channels via backend interfaces. Authoritatively.
                                    </li>
                                    <li>Globally actualize effective processes through synergistic ROI. Interactively.</li>
                                </ul>
                            </div>

                            <div class="job-details-info mt-5">
                                <h3 class="h5">Skill & Experience</h3>
                                <ul class="content-list list-unstyled">
                                    <li>You have at least 3 years’ experience working as a Product Designer.</li>
                                    <li>You have experience using Sketch and InVision or Framer X</li>
                                    <li>You have some previous experience working in an agile environment – Think two-week
                                        sprints.
                                    </li>
                                    <li>You are familiar using Jira and Confluence in your workflow</li>
                                </ul>
                            </div>

                            <img src="img/apply-now-1.jpg" class="img-fluid mt-5 rounded-custom" alt="apply">
                        </div>
                    </div>
                    <div class="col-lg-4">
                        <div class="job-overview-wrap bg-light p-5 sticky-sidebar rounded-custom mt-5 mt-lg-0">
                            <h5>Job Overviews</h5>
                            <ul class="job-overview-list list-unstyled mt-4">
                                <li>
                                    <i class="far fa-map-marker-alt text-primary"></i>
                                    <div class="overview-item">
                                        <h6 class="mb-0">Location:</h6>
                                        <span>London, UK</span>
                                    </div>
                                </li>
                                <li>
                                    <i class="far fa-user text-primary"></i>
                                    <div class="overview-item">
                                        <h6 class="mb-0">Job Title:</h6>
                                        <span>Designer</span>
                                    </div>
                                </li>
                                <li>
                                    <i class="far fa-clock text-primary"></i>
                                    <div class="overview-item">
                                        <h6 class="mb-0">Hours:</h6>
                                        <span>50h / week</span>
                                    </div>
                                </li>
                                <li>
                                    <i class="far fa-history text-primary"></i>
                                    <div class="overview-item">
                                        <h6 class="mb-0">Rate:</h6>
                                        <span>$15 - $25 / hour</span>
                                    </div>
                                </li>
                                <li>
                                    <i class="far fa-wallet text-primary"></i>
                                    <div class="overview-item">
                                        <h6 class="mb-0">Salary:</h6>
                                        <span>$35k - $45k</span>
                                    </div>
                                </li>
                            </ul>
                            <a href="contact-us.html" class="btn btn-primary d-block mt-5">Apply now</a>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <!--job details section end-->

        <!--related job start-->
        {{-- <section class="related-job-list ptb-120 bg-light">
            <div class="container">
                <div class="row align-items-center justify-content-between">
                    <div class="col-lg-4 col-md-12">
                        <div class="section-heading">
                            <h4 class="h5 text-primary">Related Jobs</h4>
                            <h2>More Openings Jobs at Quiety</h2>
                        </div>
                    </div>
                    <div class="col-lg-7 col-md-12">
                        <p>Phosfluorescently disintermediate revolutionary paradigms before enabled interfaces. Dynamically
                            transition skills vis-a-vis virtual customer service via impactful partnerships with technically
                            sound paradigms with cutting-edge initiatives. </p>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-4 col-md-6">
                        <a href="career-single.html" class="text-decoration-none mt-4 mt-lg-0 mt-xl-0 single-open-job p-5 bg-white d-block rounded-custom">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <span class="text-muted h6 mb-2 job-time"><i class="far fa-briefcase me-2"></i> Remote - Full Time</span>
                                <span class="badge rounded-pill px-3 py-2 bg-primary-soft text-primary small">Developer</span>
                            </div>
                            <h3 class="h5">Jr Frontend Developer</h3>
                            <ul class="job-info-list list-inline list-unstyled text-muted">
                                <li class="list-inline-item"><span class="far fa-house-building me-1"></span> Google</li>
                                <li class="list-inline-item"><span class="far fa-map-marker-alt me-1"></span> London, UK
                                </li>
                                <li class="list-inline-item"><span class="far fa-wallet me-1"></span> $35k - $45k</li>
                            </ul>
                            <div class="btn btn-primary btn-sm d-inline-block mt-4">Apply Now</div>
                        </a>
                    </div>
                    <div class="col-lg-4 col-md-6">
                        <a href="career-single.html" class="text-decoration-none mt-4 mt-lg-0 mt-xl-0 single-open-job p-5 bg-white d-block rounded-custom">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <span class="text-muted h6 mb-2 job-time"><i class="far fa-briefcase me-2"></i> Remote - Full Time</span>
                                <span class="badge rounded-pill px-3 py-2 bg-danger-soft text-danger small">Designer</span>
                            </div>
                            <h3 class="h5">UI/UX Product Designer</h3>
                            <ul class="job-info-list list-inline list-unstyled text-muted">
                                <li class="list-inline-item"><span class="far fa-house-building me-1"></span> Figma</li>
                                <li class="list-inline-item"><span class="far fa-map-marker-alt me-1"></span> California
                                </li>
                                <li class="list-inline-item"><span class="far fa-wallet me-1"></span> $25k - $35k</li>
                            </ul>
                            <div class="btn btn-primary btn-sm d-inline-block mt-4">Apply Now</div>
                        </a>
                    </div>
                    <div class="col-lg-4 col-md-6">
                        <a href="career-single.html" class="text-decoration-none mt-4 mt-lg-0 mt-xl-0 single-open-job p-5 bg-white d-block rounded-custom">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <span class="text-muted h6 mb-2 job-time"><i
                                        class="far fa-briefcase me-2"></i> Full Time</span>
                                <span class="badge rounded-pill px-3 py-2 bg-success-soft text-success small">Manager</span>
                            </div>
                            <h3 class="h5">Senior Office Manager</h3>
                            <ul class="job-info-list list-inline list-unstyled text-muted">
                                <li class="list-inline-item"><span class="far fa-house-building me-1"></span> Dribble</li>
                                <li class="list-inline-item"><span class="far fa-map-marker-alt me-1"></span> California
                                </li>
                                <li class="list-inline-item"><span class="far fa-wallet me-1"></span> $55k - $62k</li>
                            </ul>
                            <div class="btn btn-primary btn-sm d-inline-block mt-4">Apply Now</div>
                        </a>
                    </div>
                </div>
            </div>
        </section> --}}
        <!--related job end-->

           <!--cat subscribe start-->
           <section class="cta-subscribe bg-dark text-white ptb-120 position-relative overflow-hidden">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-8 col-md-10">
                        <div class="subscribe-info-wrap text-center position-relative z-2">
                            <div class="section-heading" data-aos="fade-up">
                                <h4 class="h5 text-warning">Lets Build Your Solution Get Free Support.</h4>
                                <h2>Start Your Development Journey With Us.</h2>
                                <p>We can assist you in building a tailored digital solutions for your business.</p>
                            </div>
                            <div class="form-block-banner mw-60 m-auto mt-5" data-aos="fade-up" data-aos-delay="50">
                                <a href="{{ route('contact-us') }}" class="btn btn-primary">Contact Us</a>
                                <a href="http://www.youtube.com/watch?v=hAP2QF--2Dg" class="text-decoration-none popup-youtube d-inline-flex align-items-center watch-now-btn ms-lg-3 ms-md-3 mt-3 mt-lg-0"> <i
                                        class="fas fa-play"></i> Watch Demo </a>
                            </div>
                            {{-- <ul class="nav justify-content-center subscribe-feature-list mt-4" data-aos="fade-up" data-aos-delay="100">
                                <li class="nav-item">
                                    <span><i class="far fa-check-circle text-primary me-2"></i>No hidden charges</span>
                                </li>
                                <li class="nav-item">
                                    <span><i class="far fa-check-circle text-primary me-2"></i>No credit card required</span>
                                </li>
                                <li class="nav-item">
                                    <span><i class="far fa-check-circle text-primary me-2"></i>Support 24/7</span>
                                </li>
                                <li class="nav-item">
                                    <span><i class="far fa-check-circle text-primary me-2"></i>Be part of the development</span>
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


