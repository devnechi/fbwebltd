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
    <title>{{ config('app.name', 'Contact us - FutureBasics') }}</title>

    <!--google fonts-->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">

    <!--build:css-->
    <link href="{{ asset('css/main.css') }}" rel="stylesheet">
    <!-- endbuild -->

    <!--custom css start-->
    <link href="{{ asset('css/custom.css') }}" rel="stylesheet">
    <!--custom css end-->

    {{-- <script src='https://www.google.com/recaptcha/api.js'></script> --}}

    <script src="https://www.google.com/recaptcha/api.js" async defer></script>
    {!! RecaptchaV3::initJs() !!}

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
        <section class="page-header position-relative overflow-hidden ptb-120 bg-dark" style="background: url('img/page-header-bg.svg')no-repeat bottom left">
            <div class="container">
                <div class="row">
                    <div class="col-lg-6 col-md-12">
                        <h1 class="display-5 fw-bold">Contact Us</h1>
                        <p class="lead">We are always happy to hear from
                            you, so don't hesitate to get in
                            touch with us.</p>
                    </div>
                </div>
                <div class="bg-circle rounded-circle circle-shape-3 position-absolute bg-dark-light right-5"></div>
            </div>
        </section>
        <!--page header section end-->

                <!--contact us form start-->
                <section class="contact-us-form pt-60 pb-120" style="background: url('img/shape/contact-us-bg.svg')no-repeat center bottom">
                    <div class="container">
                        <br/><br/>
                        @if (Session::has('success'))
                                <div class="alert alert-info" id="al">{{ Session::get('success') }}
                                  <button class="close" onclick="document.getElementById('al').style.display='none'" >&cross;</button>
                                </div>
                        @endif
                        @if ($errors->any())
                        <div class="alert alert-danger">
                            <ul>
                                @foreach ($errors->all() as $error)
                                    <li>{{ $error }}</li>
                                @endforeach
                            </ul>
                        </div>
                        {{-- start of contact form --}}
                      @endif
                        <div class="row justify-content-lg-between align-items-center">
                            <div class="col-lg-6 col-md-8">
                                <div class="section-heading">
                                    <h2>Talk To Our Customer Service Department</h2>
                                    <p>
                                        Leave us a message and we will get back to
                                        you as soon as possible.
                                        </p>
                                </div>

                                <form action="{{ route('contact-em') }}" method="post" class="register-form">
                                    @csrf
                                    <div class="row">
                                        <div class="col-sm-6">
                                            <label for="firstName" class="mb-1">First name <span
                                                    class="text-danger">*</span></label>
                                            <div class="input-group mb-3">
                                                <input type="text" class="form-control" name="firstName" id="firstName" required placeholder="First name" aria-label="First name">
                                                @error('firstName')
                                                <span class="invalid-feedback" role="alert">
                                                    <strong>{{ $message }}</strong>
                                                </span>
                                            @enderror
                                            </div>
                                        </div>
                                        <div class="col-sm-6 ">
                                            <label for="lastName" class="mb-1">
                                                Last name
                                                <span class="text-danger">*</span>
                                            </label>
                                            <div class="input-group mb-3">
                                                <input type="text" class="form-control" name="lastName" id="lastName" required placeholder="Last name" aria-label="Last name">
                                            </div>
                                        </div>
                                        <div class="col-sm-6">
                                            <label for="phone" class="mb-1">
                                                Phone
                                                <span class="text-danger">*</span>
                                            </label>
                                            <div class="input-group mb-3">
                                                <input type="text" class="form-control" name="phone" id="phone" required placeholder="Phone" aria-label="Phone">
                                                @error('phone')
                                                <span class="invalid-feedback" role="alert">
                                                    <strong>{{ $message }}</strong>
                                                </span>
                                            @enderror
                                            </div>
                                        </div>
                                       <div class="row">
                                        <div class="col-sm-6 ">
                                            <label for="subject" class="mb-1">
                                                Subject
                                                <span
                                                    class="text-danger">*</span>
                                            </label>
                                            <div class="input-group mb-3">
                                                <input type="text" class="form-control"  id="subject" name="subject" placeholder="Subject" aria-label="Subject">
                                                @error('subject')
                                                <span class="invalid-feedback" role="alert">
                                                    <strong>{{ $message }}</strong>
                                                </span>
                                            @enderror
                                            </div>
                                        </div>
                                    </div>
                                        <div class="col-sm-6">
                                            <label for="contactemail" class="mb-1">Email
                                                <span
                                                class="text-danger">*</span>
                                            </label>
                                            <div class="input-group mb-3">
                                                <input type="email" class="form-control" name="contactemail" id="contactemail" @error('contactemail') is-invalid @enderror required placeholder="Email" aria-label="Email">
                                            </div>
                                        </div>
                                        <div class="col-12">
                                            <label for="yourMessage" class="mb-1">Message <span class="text-danger">*</span></label>
                                            <div class="input-group mb-3">
                                                <textarea class="form-control" name="message" id="message" required placeholder="How can we help you?" style="height: 160px"></textarea>
                                                @error('message')
                                                <span class="invalid-feedback" role="alert">
                                                    <strong>{{ $message }}</strong>
                                                </span>
                                            @enderror
                                            </div>
                                        </div>

                                        <div class="col-sm-6">
                                            {{-- @if(config('services.recaptcha.key'))
                                            <div class="g-recaptcha"
                                                data-sitekey="{{config('services.recaptcha.key')}}">
                                            </div>
                                        @endif --}}
                                        {{-- <div class="form-group">
                                            <strong>Just making sure you are not a robot :</strong>
                                            {!! NoCaptcha::renderJs() !!}
                                            {!! NoCaptcha::display() !!}
                                         </div>
                                        </div> --}}
                                        <div class="form-group{{ $errors->has('g-recaptcha-response') ? ' has-error' : '' }}">
                                            <div class="col-md-6">
                                                {!! RecaptchaV3::field('contactfbc') !!}
                                                @if ($errors->has('g-recaptcha-response'))
                                                    <span class="help-block">
                                                        <strong>{{ $errors->first('g-recaptcha-response') }}</strong>
                                                    </span>
                                                @endif
                                            </div>
                                        </div>
                                    </div>
                                        <div class="col-sm-6">
                                            <div class="form-group" style="display: none;">
                                                <label for="simpfill">not to fill
                                                 <input type="checkbox" name="simpfill" id="simpfill" />
                                                </label>
                                               </div>
                                        </div>
                                    </div>
                                    <button type="submit" name="submit" value="submit" class="btn btn-primary mt-4">Get in Touch</button>
                                </form>
                            </div>
                            <div class="col-lg-5 col-md-10">
                                {{-- <div class="contact-us-img">
                                    <img src="img/contact-us-img-2.svg" alt="contact us" class="img-fluid">
                                </div> --}}
                            </div>
                        </div>
                    </div>
                </section>
                <!--contact us form end-->
                <!--contact us promo section start-->
                <section class="contact-promo ptb-120">
                    <div class="container">
                        <div class="row justify-content-center">
                            {{-- <div class="col-lg-4 col-md-6 mt-4 mt-lg-0">
                                <div class="contact-us-promo p-5 bg-white rounded-custom custom-shadow text-center d-flex flex-column h-100">
                                    <span class="fad fa-comment-alt-lines fa-3x text-primary"></span>
                                    <div class="contact-promo-info mb-4">
                                        <h5>Chat with us</h5>
                                        <p>We've got live Social Experts waiting to help you <strong>monday to friday</strong> from
                                            <strong>9am to 5pm EAT.</strong>
                                        </p>
                                    </div>
                                    <a href="mailto:info@futurebasics.co.tz" class="btn btn-link mt-auto">Chat with us</a>
                                </div>
                            </div> --}}
                            <div class="col-lg-4 col-md-6 mt-4 mt-lg-0">
                                <div class="contact-us-promo p-5 bg-white rounded-custom custom-shadow text-center d-flex flex-column h-100">
                                    <span class="fad fa-envelope fa-3x text-primary"></span>
                                    <div class="contact-promo-info mb-4">
                                        <h5>Email Us</h5>
                                        <p>Send us an email at <strong>info@futurebasics.co.tz</strong>
                                            and we will reply as soon as possible.</p>
                                    </div>
                                    <a href="mailto:hellothemetags@gmail.com" class="btn btn-primary mt-auto">Email Us</a>
                                </div>
                            </div>
                            <div class="col-lg-4 col-md-6 mt-4 mt-lg-0">
                                <div class="contact-us-promo p-5 bg-white rounded-custom custom-shadow text-center d-flex flex-column h-100">
                                    <span class="fad fa-phone fa-3x text-primary"></span>
                                    <div class="contact-promo-info mb-4">
                                        <h5>Give us a call</h5>
                                        <p>Give us a call. We are open <strong>monday to friday</strong> from
                                            <strong>9am to 5pm</strong>  EAT.
                                        </p>
                                    </div>
                                    <a href="tel:00-255-687-859-500" class="btn btn-link mt-auto"> + 255 687 859 500 </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
                <!--contact us promo section end-->



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
                                <div style="display: none;"  class="col-md-4 col-lg-4 mt-4 mt-md-0 mt-lg-0">
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
            <div class="footer-bottom bg-dark text-white py-4">
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
