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
            from {
                transform: rotate(0deg)
            }

            to {
                transform: rotate(360deg)
            }
        }

        .spin {
            animation-name: spinning;
            animation-duration: 3s;
            animation-iteration-count: infinite;
            /* linear | ease | ease-in | ease-out | ease-in-out */
            animation-timing-function: linear;
        }

        .icon-size {
            height: 604px;
            /* width: 120px; */
        }

        @import url(https://fonts.googleapis.com/css?family=Raleway);

*, *:before, *:after{
    margin: 0;
    padding: 0;
    -webkit-box-sizing: border-box;
    -moz-box-sizing:border-box;
    box-sizing: border-box;
  }


.containerz{
    padding: 1em 0;
    float: left;
    width: 50%;
  }
  @media screen and (max-width: 640px){
    .containerz{
      display: block;
      width: 100%;
    }
  }

  @media screen and (min-width: 900px){
    .containerz{
      width: 33.33333%;
    }
  }

  .containerz .title{
    color: #1a1a1a;
    text-align: center;
    margin-bottom: 10px;
  }

  .content {
    position: relative;
    width: 90%;
    max-width: 400px;
    margin: auto;
    overflow: hidden;
  }

  .content .content-overlay {
    background: rgba(0,0,0,0.7);
    position: absolute;
    height: 99%;
    width: 100%;
    left: 0;
    top: 0;
    bottom: 0;
    right: 0;
    opacity: 0;
    -webkit-transition: all 0.4s ease-in-out 0s;
    -moz-transition: all 0.4s ease-in-out 0s;
    transition: all 0.4s ease-in-out 0s;
  }

  .contentz:hover .contentz-overlay{
    opacity: 1;
  }

  .contentz-image{
    width: 100%;
  }

  .content-details {
    position: absolute;
    text-align: center;
    padding-left: 1em;
    padding-right: 1em;
    width: 100%;
    top: 50%;
    left: 50%;
    opacity: 0;
    -webkit-transform: translate(-50%, -50%);
    -moz-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
    -webkit-transition: all 0.3s ease-in-out 0s;
    -moz-transition: all 0.3s ease-in-out 0s;
    transition: all 0.3s ease-in-out 0s;
  }

  .contentz:hover .contentz-details{
    top: 50%;
    left: 50%;
    opacity: 1;
  }

  .contentz-details h3{
    color: #fff;
    font-weight: 500;
    letter-spacing: 0.15em;
    margin-bottom: 0.5em;
    text-transform: uppercase;
  }

  .contentz-details p{
    color: #fff;
    font-size: 0.8em;
  }


  .fadeIn-top{
    top: 20%;
  }

    </style>
</head>

<body>
    <nav class="navbar navbar-expand-md navbar-light navbar-fixed-top shadow-sm navigation" id="top-nav">
        <div class="container">
            <a class="navbar-brand brand-text navbrand-text" href="{{ url('/') }}">
                {{-- {{ config('app.name', 'Future Basics') }} --}}
                <img src="images/fb_og_logo.png" alt="" class="" style="height: 100px; width: 198px; padding: 10px;">
            </a>
            <button class="navbar-toggler hidden-lg-up float-lg-right" type="button" data-toggle="collapse"
                data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
                aria-label="{{ __('Toggle navigation') }}">

                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse navbar-toggleable-md" id="navbarSupportedContent">
                <!-- Left Side Of Navbar -->
                <ul class="nav navbar-nav mr-auto">

                </ul>

                <ul class="nav navbar-nav menu float-lg-right ml-auto" id="top-nav">
                    <!-- Right Side Of Navbar -->
                    @if (Route::has('login'))
                    <div class="hidden fixed top-0 right-0 px-6 py-4 sm:block ">
                        @auth
                        <a href="{{ url('/home') }}" class="text-sm text-gray-700  navbrand-text">Home</a>
                        @else
                        <a href="{{ route('about') }}" class="ml-4 text-sm text-gray-700  navbrand-text"> About</a>
                        <a href="{{ route('business') }}" class="ml-4 text-sm text-gray-700  navbrand-text">
                            Business</a>
                        {{-- <a href="{{ route('register') }}" class="ml-4 text-sm text-gray-700 navbrand-text">
                        Responsibilities</a>
                        <a href="{{ route('register') }}" class="ml-4 text-sm text-gray-700  navbrand-text">
                            Employees</a>
                        <a href="{{ route('register') }}" class="ml-4 text-sm text-gray-700  navbrand-text"> Social
                            Media</a>--}}
                        <a href="#contact" class="ml-4 text-sm text-gray-700  navbrand-text"> Contact
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
    {{-- <section class="hero-area bg-1" style="height: 600px;">
        <div class="container">
            <div class="row">
                <div class="col-md-7" style="padding-top:90px;">
                    <div class="block" style="padding-top:90px;">
                        <h1 class="wow fadeInDown" data-wow-delay="0.3s" data-wow-duration=".2s">SIMPLIFIED BUSINESS
                            SOLUTIONS</h1>
                        <!-- 	                        <p class="wow fadeInDown" data-wow-delay="0.5s" data-wow-duration=".5s">Apply the Latest Technology, Improve your productivity, ensure customer satisfaction while delivering value</p> -->
                        <div class="wow fadeInDown" data-wow-delay="0.7s" data-wow-duration=".7s">
                            <a class="btn btn-home" href="#about" role="button">Get Started</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-5 wow zoomIn" style="padding-top:50px;">
                    <div class="block" style="padding-top:90px;">
                        <div class="col-md-6 col-xl-5 mt-xl-5 wow fadeInRight" data-wow-delay="0.3s"
                            style="height: 700px; width: 700px; padding-top: 20px;">
                            <img src="images/fb_logo_white.png" alt="" style="height: 500px; width: 890px;"
                                class="img-fluid">
                        </div>
                    </div>
                </div>
            </div><!-- .row close -->
        </div><!-- .container close -->
    </section><!-- header close -->
 --}}

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
                        <h1 class="h1-responsive font-weight-bold mt-sm-5"
                            style="color:rgb(216, 216, 29);  padding-top: 40px;">Supporting </h1>
                        <h1 class="h1-responsive font-weight-bold mt-sm-5" style="margin-top: 0rem !important;">Development space</h1>
                        <h1 class="h1-responsive font-weight-bold mt-sm-5" style="margin-top: 0rem !important;">to be <strong>competitive</strong></h1>


                        {{-- <hr class="hr-light">
                        <h2 class="h2-responsive">Analyse, Design, Develope and Deliver </h2>
                        <h6 class="mb-4">Whether its collecting Real time data, producing quality reports or simply
                            verifiying transactions for multiple sites, do it easily with radarmile.</h6>
                        <a class="btn btn-purple">Download <i class="fa fa-download"></i></a>
                        <a class="btn btn-outline-white" href="#about">Learn more</a>
                    --}}
                    </div>
                    <!--Grid column-->
                    <!--Grid column-->
                    <div class="col-md-6 white-text text-center text-md-left mt-xl-5 mb-5 wow fadeInRight"
                        data-wow-delay="0.3s" style="padding-top: 40px;">

                        {{-- <img class=" icon-size" src="images/fbicon.png" alt="" class="img-fluid"> --}}
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
                    <h2>Future basics is a digital company bringing simplified digital solution into complex development space. </h2>
                    <p style="font-size: 24px;"><strong>Future Basics</strong></p>
                    <p style="font-size: 24px;"> is a digital company</p>
                    <p style="font-size: 24px;"> bringing simplified digital solution into complex development space
                    </p>
                </div>
            </div>
        </div>
            <div class="container">
                <div class="row">
                    <div class="col-lg-4 ">
                        <div class="container containerz">
                            <h3 class="title">Text fadeIn top</h3>
                            <div class="contentz">
                              <a href="https://unsplash.com/photos/HkTMcmlMOUQ" target="_blank">
                                <div class="contentz-overlay"></div>
                                <img class="contentz-image" src="https://images.unsplash.com/photo-1433360405326-e50f909805b3?ixlib=rb-0.3.5&q=80&fm=jpg&crop=entropy&w=1080&fit=max&s=359e8e12304ffa04a38627a157fc3362">
                                <div class="contentz-details fadeIn-top">
                                  <h3>This is a title</h3>
                                  <p>This is a short description</p>
                                </div>
                              </a>
                            </div>
                          </div>
                    </div>
                    <div class="col-md-4 ">
                        <div class="container containerz">
                            <h3 class="title">Text fadeIn top</h3>
                            <div class="contentz">
                              <a href="https://unsplash.com/photos/HkTMcmlMOUQ" target="_blank">
                                <div class="contentz-overlay"></div>
                                <img class="contentz-image" src="https://images.unsplash.com/photo-1433360405326-e50f909805b3?ixlib=rb-0.3.5&q=80&fm=jpg&crop=entropy&w=1080&fit=max&s=359e8e12304ffa04a38627a157fc3362">
                                <div class="contentz-details fadeIn-top">
                                  <h3>This is a title</h3>
                                  <p>This is a short description</p>
                                </div>
                              </a>
                            </div>
                          </div>
                    </div>
                    <div class="col-md-4 ">
                        <div class="container containerz">
                            <h3 class="title">Text fadeIn top</h3>
                            <div class="contentz">
                              <a href="https://unsplash.com/photos/HkTMcmlMOUQ" target="_blank">
                                <div class="contentz-overlay"></div>
                                <img class="contentz-image" src="https://images.unsplash.com/photo-1433360405326-e50f909805b3?ixlib=rb-0.3.5&q=80&fm=jpg&crop=entropy&w=1080&fit=max&s=359e8e12304ffa04a38627a157fc3362">
                                <div class="contentz-details fadeIn-top">
                                  <h3>This is a title</h3>
                                  <p>This is a short description</p>
                                </div>
                              </a>
                            </div>
                          </div>
                    </div>
            </div>
            </div>
            <div class="container">
            <div class="row">
                <div class="col-md-8">
                    <h2 class="h1-responsive font-weight-bold mt-sm-5">Simplified Digital Solutions</h2>
                    <br />
                    <p style="font-size: 24px; padding: 1.5em;">We venture in areas that show great potential and extract value from
                        them. Our mission is</p>
                </div>
                <div class="col-md-4 ">
                    <div class="card">
                        <img src="../images/wel/notepad.jpg" alt="Avatar"
                            style="width:100%">
                        {{-- <div class="container">
                          <h4><b>John Doe</b></h4>
                          <p>Architect & Engineer</p>
                        </div> --}}
                    </div>
                </div>
            </div>
            <br />
            <br />
            <div class="row">

                <div class="col-md-4">
                    <!-- Card -->
                    <div class="card">
                        <img src="../images/wel/lap.jpg" alt="Avatar"
                            style="width:100%">
                        {{-- <div class="container">
                          <h4><b>John Doe</b></h4>
                          <p>Architect & Engineer</p>
                        </div> --}}
                    </div>
                    <!-- Card -->
                </div>
                <div class="col-md-8 pull-right">
                    <h2 class="h1-responsive font-weight-bold mt-sm-5">Innovative Digital Solutions</h2>
                    <br />
                    <p style="font-size: 24px;">We venture in areas that show great potential and extract value from
                        them. Our mission is</p>
                </div>
            </div>
            <div class="row">
                <div class="col-md-8">
                    <h2 class="h1-responsive font-weight-bold mt-sm-5">Efficient Digital Solutions</h2>
                    <br />
                    <p style="font-size: 24px;">We venture in areas that show great potential and extract value from
                        them. Our mission is</p>
                </div>
                <div class="col-md-4 ">
                    <div class="card">
                        <img src="../images/wel/cyber.jpg" alt="Avatar"
                            style="width:100%">
                        {{-- <div class="container">
                          <h4><b>John Doe</b></h4>
                          <p>Architect & Engineer</p>
                        </div> --}}
                    </div>
                </div>
            </div>
            <br />
            <br />
            <div class="row">

                <div class="col-md-4">
                    <!-- Card -->
                    <div class="card">
                        <img src="../images/wel/hex.jpg" alt="Avatar"
                            style="width:100%">
                        {{-- <div class="container">
                          <h4><b>John Doe</b></h4>
                          <p>Architect & Engineer</p>
                        </div> --}}
                    </div>
                    <!-- Card -->
                </div>
                <div class="col-md-8 pull-right">
                    <h2 class="h1-responsive font-weight-bold mt-sm-5">Tailored Digital Solutions</h2>
                    <br />
                    <p style="font-size: 24px;">We venture in areas that show great potential and extract value from
                        them. Our mission is</p>
                </div>
            </div>
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
                                <img src="../images/about/abt-us.jpg"
                                    alt="Avatar" style="width:300px;height:350px; padding-bottom: 160px">
                            </div>
                            <div class="flip-card-back">
                                <h1>About Us</h1>
                                <p>All about the Team</p>
                                <p>Structure</p>
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
                                <img src="../images/about/suit.jpg"
                                    alt="Avatar" style="width:300px;height:350px; padding-bottom: 160px;">
                            </div>
                            <div class="flip-card-back">
                                <h1>Culture</h1>
                                <p>Our Community</p>
                                <p>Meet the Team</p>
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
                                <img src="../images/about/business.jpg"
                                    alt="Avatar" style="width:300px;height:350px; padding-bottom: 160px">
                            </div>
                            <div class="flip-card-back">
                                <h1>Ventures</h1>
                                <p>Business solutions</p>
                                <p>Enterprise solutions</p>
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
                            <h3>An innovative and dynamic company with abundant technical experience, a diverse
                                portfolio of ventures and a highly skilled team.
                                Future Basics utilizes its broad network of human resources and problem understanding to
                                create effective ICT-based solutions.</h3>
                        </div>
                        {{-- <p>We support access to future technologies, execute large to small projects, consult MSMEs,
                            Local Authorities, Government Agencies, Not-for-profit organisations and development
                            programs on using technologies to build value and in ensuring our clients use the most
                            efficient and effective operating systems.</p>
                        <p>
                            We are a value-oriented team bringing creativity and excellence in everything we are
                            involved in. We thrive in solving business systems problems especially in the developing
                            world. Future Basics uses latest technologies to improve efficiency in business processes
                            with the intentions of increasing productivity, minimizing administrative costs, increasing
                            connectivity and with data we assist companies to make strategic decisions.</p> --}}

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
        Service start
        ==================== -->
    <section id="service" class="service section">
        <div class="container">
            <div class="row">
                <div class="col-lg-12 col-md-3 wow fadeInLeft">
                    <div class="heading wow fadeInUp">
                        <h2> Everything has a future, and we help shape it. </h2>
                        {{-- <p style="font-size: 24px;">We venture in areas that show great potential and extract value from
                        them. Our mission is to blend creativity with technology excellence to bring value and meaning
                        to life endevours. We make our customers' steps to the future easier, smarter and valuable. </p> --}}
                    </div>
                </div>
                <div class="col-sm-6 col-md-4 wow fadeInLeft">
                    <!-- Card -->
                    <div class="card card-fb-focus">
                        <!-- Card image -->
                        <div class="view overlay">
                            <div class="container block">
                                <i class="tf-ion-android-compass"></i>
                                <h3>Technology Solutions</h3>
                                <p>We provide digital solutions that are agile and accessible across a wide range of devices. These solutions are Efficient, Tailored and Innovative.
                                </p>
                            </div>
                        </div>
                    </div>
                    <!-- Card -->
                </div>
                <div class="col-sm-6 col-md-4 wow fadeInLeft" data-wow-delay="0.3s">
                    <!-- Card -->
                    <div class="card card-fb-focus">
                        <!-- Card image -->
                        <div class="view overlay">
                            <div class="container block">
                                <i class="tf-ion-android-compass"></i>
                                <h3> Consultancy</h3>
                                <p>We guide and advice different types of clients on how best to grow their business or overcome their obstacles through digital methods.</p>
                            </div>
                        </div>
                    </div>
                    <!-- Card -->
                </div>
                <div class="col-sm-6 col-md-4 wow fadeInLeft" data-wow-delay="0.6s">
                    <!-- Card -->
                    <div class="card card-fb-focus">
                        <!-- Card image -->
                        <div class="view overlay">
                            <div class="container block">
                                <i class="tf-ion-android-compass"></i>
                                <h3> Solution & Idea Development.</h3>
                                <p>We assist clients in implementing their solutions as well as progressing and materializing their ideas.</p>
                            </div>
                        </div>
                    </div>
                    <!-- Card -->
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
