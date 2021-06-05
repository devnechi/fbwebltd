<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>Future Basics</title>

    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
    <link href="{{ mix('css/app.css') }}" rel="stylesheet">
    <!-- <link rel="stylesheet" href="css/bootstrap.min.css"> -->
    <!-- Bootstrap CDN -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.5/css/bootstrap.min.css"
        integrity="sha384-AysaV+vQoT3kOAXZkl02PThvDr8HYKPZhNT5h/CXfBThSRXQ6jW5DO2ekP5ViFdi" crossorigin="anonymous">


    <!-- <link rel="stylesheet" href="css/themify-icons.css"> -->
    <link rel="stylesheet" href="css/themefisher-fonts.css">
    <link rel="stylesheet" href="css/font-awesome.min.css">
    <link rel="stylesheet" href="css/owl.carousel.css">
    <link rel="stylesheet" href="css/animate.css">
    <link rel="stylesheet" href="css/style.css">
    <!-- Responsive Stylesheet -->
    <link rel="stylesheet" href="css/responsive.css">
    <link rel="stylesheet" href="css/themify-icons.css">
    {{-- <!--[if lt IE 8]><!-->
        <link rel="stylesheet" href="{{ mix() }}"> --}}
        <style>
            @keyframes spinning {
              from { transform: rotate(0deg) }
              to { transform: rotate(360deg) }
            }
            .spin {
              animation-name: spinning;
              animation-duration: 3s;
              animation-iteration-count: infinite;
              /* linear | ease | ease-in | ease-out | ease-in-out */
              animation-timing-function: linear;
            }

            .icon-size{
                height: 604px;
                /* width: 120px; */
            }
          </style>
</head>

<body>
    <nav class="navbar navbar-expand-md navbar-light navbar-fixed-top shadow-sm navigation" id="top-nav">
        <div class="container">
            <a class="navbar-brand brand-text navbrand-text" href="{{ url('/') }}">
                {{ config('app.name', 'Future Basics') }}
            </a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
                 aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="{{ __('Toggle navigation') }}">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <!-- Left Side Of Navbar -->
                <ul class="nav navbar-nav mr-auto">

                </ul>

                <ul class="navbar-nav ml-auto">
                    <!-- Right Side Of Navbar -->
                    @if (Route::has('login'))
                    <div class="hidden fixed top-0 right-0 px-6 py-4 sm:block ">
                        @auth
                        <a href="{{ url('/home') }}" class="text-sm text-gray-700  navbrand-text">Home</a>
                        @else
                        <a href="{{ route('about') }}" class="ml-4 text-sm text-gray-700  navbrand-text"> About</a>
                        <a href="{{ route('business') }}" class="ml-4 text-sm text-gray-700  navbrand-text">
                            Business</a>
                        {{-- <a href="{{ route('register') }}" class="ml-4 text-sm text-gray-700  navbrand-text">
                            Responsibilities</a>
                        <a href="{{ route('register') }}" class="ml-4 text-sm text-gray-700  navbrand-text">
                            Employees</a>
                        <a href="{{ route('register') }}" class="ml-4 text-sm text-gray-700  navbrand-text"> Social
                            Media</a> --}}
                        <a href="{{ route('register') }}" class="ml-4 text-sm text-gray-700  navbrand-text"> Contact
                            us</a>
                        <a href="{{ route('login') }}" class="ml-4 text-sm text-gray-700  navbrand-text"> Log in</a>
{{--
                        @if (Route::has('register'))
                        <a href="{{ route('register') }}" class="ml-4 text-sm text-gray-700 navbrand-text">Register</a>
                        @endif --}}
                        @endauth
                    </div>
                    @endif
                </ul>
            </div>
        </div>
    </nav>

    <!--Navbar -->
    <!-- https://mdbootstrap.com/img/Photos/Others/architecture.jpg -->
    <!-- Full Page Intro -->
    <div class="view"
        style="background-image: url('images/networld.jpg'); background-repeat: no-repeat; background-size: cover; background-position: center center; height: 740px;">
        <!-- Mask & flexbox options-->
        <div class="mask rgba-gradient align-items-center">
            <!-- Content -->
            <div class="container">
                <!--Grid row-->
                <div class="row">
                    <!--Grid column-->
                    <div class="col-md-6 white-text text-center text-md-left mt-xl-5 mb-5 wow fadeInLeft"
                        data-wow-delay="0.3s">
                        <h1 class="h1-responsive font-weight-bold mt-sm-5" style="color:rgb(216, 216, 29);  padding-top: 40px;">Simplified</h1>
                        <h1 class="h1-responsive font-weight-bold mt-sm-5" style="margin-top: 0rem !important;">Digital Solutions</h1>
                    </div>
                    <!--Grid column-->
                    <!--Grid column-->
                    <div class="col-md-6 white-text text-center text-md-left mt-xl-5 mb-5 wow fadeInRight"
                        data-wow-delay="0.3s" style="padding-top: 40px;">
                        {{-- <img class="spin icon-size" src="images/fbicon.png" alt="" class="img-fluid"> --}}
                        {{-- <img src="images/fbholo.png" alt="" class="img-fluid"> --}}
                    </div>
                    <!--Grid column-->
                </div>
                <!--Grid row-->
            </div>
            <!-- Content -->
        </div>
        <!-- Mask & flexbox options-->
    </div>

    <section id="except-intro">
        <div class="container">
            <div class="row">
                <div class="heading titleintro wow fadeInUp">
                    <h2>Find Better Solutions: Build A Better Future</h2>
                    <p style="font-size: 24px;">We venture in areas that show great potential and extract value from
                        them. Our mission is to blend creativity with technology excellence to bring value and meaning
                        to life endevours. We make our customers' steps to the future easier, smarter and valuable. </p>
                </div>
            </div>
            <div class="row">
                <div class="col-md-8">
                    <h2 class="h1-responsive font-weight-bold mt-sm-5">Simplified Digital Solutions</h2>
                    <br />
                    <p style="font-size: 24px;">We venture in areas that show great potential and extract value from
                        them. Our mission is</p>
                </div>
                <div class="col-md-4 ">
                    <div class="card">
                        <img src="https://mdbootstrap.com/img/Mockups/Lightbox/Thumbnail/img%20(67).jpg" alt="Avatar" style="width:100%">

                      </div>
                </div>
            </div>
            <br />
            <br />

        <div class="row">

            <div class="col-md-4">
                 <!-- Card -->
                 <div class="card">
                    <img src="https://mdbootstrap.com/img/Mockups/Lightbox/Thumbnail/img%20(67).jpg" alt="Avatar" style="width:100%">
                  </div>
                <!-- Card -->
            </div>
            <div class="col-md-8 pull-right">
                <h2 class="h1-responsive font-weight-bold mt-sm-5">Simplified Digital Solutions</h2>
                <br />
                <p style="font-size: 24px;">We venture in areas that show great potential and extract value from
                    them. Our mission is</p>
            </div>
        </div>
        <br />
        <br />
            <div class="row">

                <div class="col-md-4">
                     <!-- Card -->
                     <div class="card">
                        <img src="https://mdbootstrap.com/img/Mockups/Lightbox/Thumbnail/img%20(67).jpg" alt="Avatar" style="width:100%">
                      </div>
                    <!-- Card -->
                </div>
                <div class="col-md-8 pull-right">
                    <h2 class="h1-responsive font-weight-bold mt-sm-5">Simplified Digital Solutions</h2>
                    <br />
                    <p style="font-size: 24px;">We venture in areas that show great potential and extract value from
                        them. Our mission is</p>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-8">
                <h2 class="h1-responsive font-weight-bold mt-sm-5">Simplified Digital Solutions</h2>
                <br />
                <p style="font-size: 24px;">We venture in areas that show great potential and extract value from
                    them. Our mission is</p>
            </div>
            <div class="col-md-4 ">
                <div class="card">
                    <img src="https://mdbootstrap.com/img/Mockups/Lightbox/Thumbnail/img%20(67).jpg" alt="Avatar" style="width:100%">

                  </div>
            </div>
        </div>
        <br />
        <br />
    </div>
    </section>

    <br />
    <br />
    <!--
        About start
        ==================== -->
    <section class="section about bg-gray what-we-do" id="about-us">
        {{-- <div class="mask rgba-gradient align-items-center"> --}}

        <div class="container conspace">
            <div class="row">
                <div class="col-md-4 col-sm-12 wow fadeInLeft">
                    <!-- Card -->
                    <div class="card flip-card">
                        <div class="flip-card-inner">
                          <div class="flip-card-front">
                            <img src="https://mdbootstrap.com/img/Mockups/Lightbox/Thumbnail/img%20(67).jpg" alt="Avatar" style="width:300px;height:350px; padding-bottom: 160px">
                          </div>
                          <div class="flip-card-back">
                            <h1>About Us</h1>
                            <p>Architect & Engineer</p>
                            <p>We love that guy</p>
                          </div>
                        </div>
                      </div>
                    <!-- Card -->
                </div>
                <div class="col-md-4 col-sm-12 wow fadeInLeft">
                    <!-- Card -->
                    <div class="card flip-card">
                        <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <img src="https://mdbootstrap.com/img/Mockups/Lightbox/Thumbnail/img%20(67).jpg" alt="Avatar" style="width:300px;height:350px; padding-bottom: 160px;">
                        </div>
                        <div class="flip-card-back">
                            <h1>Culture</h1>
                            <p>Architect & Engineer</p>
                            <p>We love that guy</p>
                        </div>
                        </div>
                    </div>
                    <!-- Card -->
                </div>
                <div class="col-md-4 col-sm-12 wow fadeInLeft">
                    <!-- Card -->
                    <div class="card flip-card">
                        <div class="flip-card-inner">
                          <div class="flip-card-front">
                            <img src="https://mdbootstrap.com/img/Mockups/Lightbox/Thumbnail/img%20(67).jpg" alt="Avatar" style="width:300px;height:350px; padding-bottom: 160px">
                          </div>
                          <div class="flip-card-back">
                            <h1>Products</h1>
                            <p>Architect & Engineer</p>
                            <p>We love that guy</p>
                          </div>
                        </div>
                      </div>
                    <!-- Card -->
                </div>
            </div>
        </div>
    {{-- </div> --}}
    </section>

        <section class="section about bg-gray" id="about">
        <div class="container">
            <div class="row">
                <div class="col-md-7 col-sm-12 wow fadeInLeft">
                    <div class="content">
                        <div class="sub-heading">
                            <h3>
                                A dynamic company with a diverse portfolio of ventures, Technical experience and with a
                                talented team. Future Basics utilizes its out-reach and large network to create
                                sustainable and profitable ICT-based solutions.
                            </h3>
                        </div>
                        <p>
                            We support access to future technologies, execute large to small projects, consult MSMEs,
                            Local Authorities, Government Agencies, Not-for-profit organisations and development
                            programs on using technologies to build value and in ensuring our clients use the most
                            efficient and effective operating systems.
                        </p>
                        <p>
                            We are a value-oriented team bringing creativity and excellence in everything we are
                            involved in. We thrive in solving business systems problems especially in the developing
                            world. Future Basics uses latest technologies to improve efficiency in business processes
                            with the intentions of increasing productivity, minimizing administrative costs, increasing
                            connectivity and with data we assist companies to make strategic decisions.
                        </p>

                    </div>
                </div>
                <div class="col-md-5 col-sm-12 wow fadeInLeft" data-wow-delay="0.3s">
                    <div class="about-slider">
                        <!-- <img src="images/about/proto1.jpg" alt=""> -->
                        <!--                             <img src="images/about/proto2.jpg" alt="">
                            <img src="images/about/proto3.jpg" alt=""> -->
                            <div class="card clip-polygon">
                             <img src="images/about/proto4.jpg" alt="">
                            </div>

                        <!--                             <img src="images/about/proto6.jpg" alt="">
                            <img src="images/about/proto7.jpg" alt=""> -->
                    </div>
                </div>
            </div>
        </div>
    </section><!-- #about close -->

    <!--
        About start
        ==================== -->
        <section class="section about bg-gray what-we-do" id="imp">
            <div class="mask rgba-gradient align-items-center">
        <div class="container">
            {{-- background-image: url('https://mdbcdn.b-cdn.net/img/new/standard/city/041.jpg'); background-repeat: no-repeat; background-size: cover; background-position: center center; height: 560px; --}}
            <!--Grid row-->
            <div class="row">
                <!--Grid column-->
                <div class="col-md-6 white-text text-center text-md-left mt-xl-5 mb-5 wow fadeInLeft"
                    data-wow-delay="0.3s" style="padding-top: 40px;">
                    <h1 class="h1-responsive font-weight-bold mt-sm-5">Simplified Digital Solutions</h1>

                    <hr class="hr-light">
                    {{-- <h2 class="h2-responsive">Analyse, Design, Develope and Deliver </h2> --}}
                    <h6 class="mb-4">Whether its collecting Real time data, producing quality reports or simply
                        verifiying transactions for multiple sites, do it easily with radarmile.</h6>
                    <a class="btn btn-purple">Download <i class="fa fa-download"></i></a>
                    <a class="btn btn-outline-white" href="#about">Learn more</a>
                </div>
            </div>
                <!--Grid column-->
            </div>
        </div>
        <!--Grid row-->
    </div>
</section>
    <!--
        Service start
        ==================== -->
    <section id="service" class="service section">
        <div class="container">
            <div class="row">
                <div class="heading wow fadeInUp">
                    <h2>Find Better Solutions: Build A Better Future</h2>
                    <p style="font-size: 24px;">We venture in areas that show great potential and extract value from
                        them. Our mission is to blend creativity with technology excellence to bring value and meaning
                        to life endevours. We make our customers' steps to the future easier, smarter and valuable. </p>
                </div>
                <div class="col-sm-6 col-md-3 wow fadeInLeft">
                       <!-- Card -->
                       <div class="card card-fb-focus">
                        <!-- Card image -->
                        <div class="view overlay">
                            <div class="container block">
                                <i class="tf-ion-android-compass"></i>
                                <h3>Technology Solutions</h3>
                                <p>Our systems are agile on all smart devices,they are easily accessible on desktop & mobile
                                    systems</p>
                            </div>
                        </div>
                    </div>
                    <!-- Card -->

                </div>
                <div class="col-sm-6 col-md-3 wow fadeInLeft" data-wow-delay="0.3s">
                            <!-- Card -->
                            <div class="card card-fb-focus">
                                <!-- Card image -->
                                <div class="view overlay">
                                    <div class="container block">
                                        <i class="tf-ion-android-compass"></i>
                                        <h3> Consultancy</h3>
                                        <p>We help you get access to fund and capital to grow your business, offer all necessary support
                                            for them to grow.</p>
                                    </div>
                                </div>
                            </div>
                            <!-- Card -->
                </div>
                <div class="col-sm-6 col-md-3 wow fadeInLeft" data-wow-delay="0.6s">
                    <!-- Card -->
                    <div class="card card-fb-focus">
                        <!-- Card image -->
                        <div class="view overlay">
                            <div class="container block">
                                <i class="tf-ion-android-compass"></i>
                                <h3> Investments</h3>
                                <p>Offer proffesional advice and assistance on a project implementaion, in remote areas such as
                                    Africa.</p>
                            </div>
                        </div>
                    </div>
                    <!-- Card -->
                </div>
                <div class="col-sm-6 col-md-3 wow fadeInLeft" data-wow-delay="0.9s">
                     <!-- Card -->
                     <div class="card card-fb-focus">
                        <!-- Card image -->
                        <div class="view overlay">
                            <div class="container block">
                                <i class="tf-ion-android-compass"></i>
                                <h3> Construction</h3>
                                <p>We are have a team of dedicated researchers and analyst that would help you get the
                                    information and feedback about a topic.</p>
                            </div>
                        </div>
                    </div>
                    <!-- Card -->
                </div>
                <div class="col-sm-6 col-md-3 wow fadeInLeft">
                    <!-- Card -->
                    <div class="card card-fb-focus">
                        <!-- Card image -->
                        <div class="view overlay">
                            <div class="container block">
                                <i class="tf-ion-android-compass"></i>
                                <h3> Film & Entertainment</h3>
                                <p>With the growth of data today in most of businesses, the need to visualize and make strategic
                                    decisions, that will lead to new unique opportunities for you business.</p>
                            </div>
                        </div>
                    </div>
                    <!-- Card -->
                </div>
                <div class="col-sm-6 col-md-3 wow fadeInLeft" data-wow-delay="0.3s">

                    <!-- Card -->
                    <div class="card card-fb-focus">
                        <!-- Card image -->
                        <div class="view overlay">
                            <div class="container block">
                                <i class="tf-strategy"></i>
                                <h3> Communication Solutions</h3>
                                <p>Systems need to be fast, for better customer experience,this include its upload and download
                                    speed.</p>
                            </div>
                        </div>
                    </div>
                    <!-- Card -->
                </div>
                <div class="col-sm-6 col-md-3 wow fadeInLeft" data-wow-delay="0.6s">
                    <!-- Card -->
                    <div class="card card-fb-focus">
                        <!-- Card image -->
                        <div class="view overlay">
                            <div class="container block">
                                <i class="tf-anchor2"></i>
                                <h3> Communication Solutions</h3>
                                <p>Systems need to be fast, for better customer experience,this include its upload and download
                                    speed.</p>
                            </div>
                        </div>
                    </div>
                    <!-- Card -->
                </div>
                <div class="col-sm-6 col-md-3 wow fadeInLeft" data-wow-delay="0.9s">
                    <!-- Card -->
                    <div class="card card-fb-focus">
                     <!-- Card image -->
                     <div class="view overlay">
                        <div class="container block">
                            <i class="tf-globe"></i>
                            <h3>Processing and Branding</h3>
                            <p>Systems need to be fast, for better customer experience,this include its upload and download
                                speed.</p>
                        </div>
                    </div>
                </div>
                <!-- Card -->
                </div>
            </div>

        </div> <!-- end of what we do div -->
        </div><!-- .container close -->
    </section><!-- #service close -->


    <section class="call-to-action section">
        <div class="container">
            <div class="row">
                <div class="col-md-12 wow text-center">
                    <div class="block">
                        <h2>Subscribe to our mailing list</h2>
                        <p style="font-size: 24px;">Get the latest new, project updates, start news and more register
                            below</p>
                        <div class="col-lg-6 offset-lg-3">
                            <div class="input-group">
                                <input type="text" class="form-control" placeholder="Your Email Address Here">
                                <span class="input-group-btn">
                                    <button class="btn btn-default btn-subscription" type="button">Subscribe</button>
                                </span>
                            </div><!-- /input-group -->
                        </div><!-- /.col-lg-6 -->
                    </div>
                </div>
            </div>
        </div>
    </section><!-- #call-to-action close -->

    <!--
        Contact start
        ==================== -->
    <section id="contact" class="section contact">
        <div class="container">
            <div class="row">
                <div class="col-xs-12 col-sm-12 col-md-12">
                    <div class="block">
                        <div class="heading wow fadeInUp">
                            <h2>Get In Touch With Us</h2>
                            <p style="font-size: 24px;">Please feel free to contact us at any time, for any matters
                                regarding our services.
                                If its about Technology or business, please don't hesitate to ask.
                            </p>
                        </div>
                    </div>
                </div>

                <div class="col-xs-12 col-sm-12 col-md-6 offset-md-3 wow fadeInUp" data-wow-delay="0.3s">
                    <div class="form-group">
                        <form action="#" method="post" id="contact-form">
                            <div class="input-field">
                                <input type="text" class="form-control" placeholder="Your Name" name="name">
                            </div>
                            <div class="input-field">
                                <input type="email" class="form-control" placeholder="Email Address" name="email">
                            </div>
                            <div class="input-field">
                                <textarea class="form-control" placeholder="Your Message" rows="3"
                                    name="message"></textarea>
                            </div>
                            <button class="btn btn-send" type="submit">Send me</button>
                        </form>

                        <div id="success">
                            <p>Your Message was sent successfully</p>
                        </div>
                        <div id="error">
                            <p>Your Message was not sent successfully</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section clas="wow fadeInUp">
        <div class="map-wrapper">
        </div>
    </section>

    <footer>
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <div class="block">
                        <p>Copyright &copy; <a href="http://www.futurebasics.co.tz">Future Basics</a>| All right
                            reserved.</p>
                    </div>
                </div>
            </div>
        </div>
    </footer>


    <!-- Js -->
    <script src="js/vendor/jquery-2.1.1.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.3.7/js/tether.min.js"
        integrity="sha384-XTs3FgkjiBgo8qjEjBk0tGmf3wPrWtA6coPfQDfFEY8AnYJwjalXCiosYRBIBZX8" crossorigin="anonymous">
    </script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.5/js/bootstrap.min.js"
        integrity="sha384-BLiI7JTZm+JWlgKa0M0kGRpJbF2J8q+qreVrKBC47e3K6BW78kGLrCkeRX6I9RoK" crossorigin="anonymous">
    </script>
    <script src="js/vendor/modernizr-2.6.2.min.js"></script>
    <script src="js/jquery.lwtCountdown-1.0.js"></script>
    <script src="js/owl.carousel.min.js"></script>
    <script src="js/jquery.validate.min.js"></script>
    <script src="js/jquery.form.js"></script>
    <script src="js/jquery.nav.js"></script>
    <script src="js/wow.min.js"></script>
    <script>
        //animated header class
        $(window).scroll(function () {
            var scroll = $(window).scrollTop();
            //console.log(scroll);
            if (scroll > 200) {
                //console.log('a');
                $(".navigation").addClass("animated");
            } else {
                //console.log('a');
                $(".navigation").removeClass("animated");
            }
        });

    </script>

    <!-- <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js" integrity="sha384-3ceskX3iaEnIogmQchP8opvBy3Mi7Ce34nWjpBIwVTHfGYWQS9jwHDVRnpKKHJg7" crossorigin="anonymous"></script> -->

    <script src="{{ mix('js/app.js') }}"></script>
</body>

</html>
