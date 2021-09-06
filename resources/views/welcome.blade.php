<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

    <title>Future Basics Company Limited</title>

    <meta name="keywords" content="Development space，Radarmile, Livestoka, Technology, Innovations">
    <meta name="description"
        content="Future Basics is a digital company bringing simplified digital solution into complex Development Space">
    <meta name="viewport"
        content="width=device-width, initial-scale=1.0, user-scalable=0, minimum-scale=1.0, maximum-scale=1.0">
    <meta name="format-detection" content="telephone=no">
    <meta http-equiv="X-UA-Compatible" content="IE=Edge">

    <!-- for FF, Chrome, Opera -->
    <link rel="icon" type="image/png" href="img/assets/favicons/fbicon.png" sizes="112x112">
    <link rel="icon" type="image/png" href="img/assets/favicons/fbicon.png" sizes="112x112">

    <!-- for IE -->
    <link rel="icon" type="image/x-icon" href="img/assets/favicons/fbicon.ico">
    <link rel="shortcut icon" type="image/x-icon" href="img/assets/favicons/fbicon.ico" />
    <!-- <script src="https://www.googletagmanager.com/gtag/js?id=G-DW9MBJC8M8" async=""></script><script src="//pingjs.qq.com/h5/stats.js?v2.0.4" name="MTAH5" sid="500665694" cid="500696449"></script><script>
          window.windowLoadList = [];
          window.windowLoad = function (call){
            windowLoadList.push(call);
          }
          var _locale = 'en-us';
        </script> -->

    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
    <link href="{{ mix('css/app.css') }}" rel="stylesheet">
    <!-- <link rel="stylesheet" href="css/bootstrap.min.css"> -->
    <!-- Bootstrap CDN -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.5/css/bootstrap.min.css"
        integrity="sha384-AysaV+vQoT3kOAXZkl02PThvDr8HYKPZhNT5h/CXfBThSRXQ6jW5DO2ekP5ViFdi" crossorigin="anonymous">


    <!-- <link rel="stylesheet" href="css/themify-icons.css"> -->
    {{-- <link rel="stylesheet" href="css/themefisher-fonts.css">
    <link rel="stylesheet" href="css/font-awesome.min.css">
    <link rel="stylesheet" href="css/owl.carousel.css"> --}}
    {{-- <link rel="stylesheet" href="css/animate.css"> --}}
    {{-- <link rel="stylesheet" href="css/style.css"> --}}
    <!-- Responsive Stylesheet -->
    {{-- <link rel="stylesheet" href="css/responsive.css">
    <link rel="stylesheet" href="css/themify-icons.css"> --}}

    <link rel="stylesheet" type="text/css" href="/css/base.css">
    <link rel="stylesheet" type="text/css" href="/css/base-2.css">
    <link rel="stylesheet" type="text/css" href="/css/index.css">
    <link href="/css/swiper.min.css" rel="stylesheet" type="text/css">
    <link rel="stylesheet" href="/css/yearpicker.css" type="text/css">



    <link rel="stylesheet" type="text/css" href="/css/base.css">
    <link rel="stylesheet" type="text/css" href="/css/base-2.css">
    <link rel="stylesheet" type="text/css" href="/css/index.css">

    <link href="/css/enhancement-base.css" rel="stylesheet" type="text/css">
    <link href="/css/home-new.css" rel="stylesheet" type="text/css">

    <link rel="stylesheet" type="text/css" href="/css/rem.css">
    <link rel="stylesheet" type="text/css" href="/css/rem-2.css">

    <style>
        footer {
            text-align: center;
            background: #272727;
            padding: 27px 0px;
        }

        footer p {
            font-weight: 300;
            font-size: 12px;
            color: #dfdfdf;
            letter-spacing: 3px;
        }

        footer p a {
            color: #fff;
        }

        footer p a:hover {
            color: #fff;
            text-decoration: none;
        }

    </style>
</head>

<body>

    <div class="wrap en-us">
        <!-- Header area -->
        <div class="wrap_head hestate head_white" style="display: block; position: fixed; top: 0px;">
            <!-- Click search icon add class name search_area_show Hide the menu, show the input box -->
            <!-- add class name submenu_show show submenu -->
            <div class="head_con">
                <a class="logo" href="{{ url('/') }}">
                    {{-- <h1>Future Basics</h1> --}}
                    <h1>{{ config('app.name', 'Future Basics') }}</h1>
                </a>
                @if (Route::has('login'))

                <ul class="menu_list" style="transform: translate(0px, 0px); opacity: 1;">
                    @auth

                    <li class="menu_item">
                        <a class="txt" href="{{ route('home') }}">Home</a>
                    </li>
                    @else

                    <li class="menu_item">
                        <a class="txt" href="{{ route('about') }}">About</a>
                        <ul class="sub_list" style="display: none;">
                            <li><a href="{{ route('about') }}">About Us</a></li>
                            <li><a href="{{ route('about') }}">Vision &amp; Mission</a></li>
                        </ul>
                    </li>
                    <li class="menu_item">
                        <a class="txt" href="{{ route('business') }}">Business</a>
                        <ul class="sub_list" style="display: none;">
                            <li><a href="{{ route('business') }}">Business</a></li>
                            <li><a href="{{ route('business') }}">Enterprises</a></li>

                        </ul>
                    </li>
                    <li class="menu_item">
                        <a class="txt" href="{{ route('login') }}">Login</a>
                    </li>
                    <li class="menu_item menu_item_lan">
                        <a class="cn" lang="sw-tz">SWAHILI</a>
                        <i class="s_line">|</i>
                        <a class="en" lang="en-us">English</a>
                    </li>
                </ul>
                @endauth
                <div class="lang_area">
                    <a class="lang_ch" lang="sw-tz">SW</a>
                    <i class="s_line">|</i>
                    <a class="lang_en current" lang="en-us">EN</a>
                </div>

            </div>
            <div class="icon_menu">
                <a class="i_menu"></a>
                <a class="i_close"></a>
            </div>
            <div class="bg_hover"></div>
        </div>
        @endif


        <!-- Header area -->
        <!-- Home Page Content Start -->
        <!-- CSS Content Start -->
        <link href="/css/enhancement-base.css" rel="stylesheet" type="text/css">
        <link href="/css/home-new.css" rel="stylesheet" type="text/css">
        <!-- CSS Content End -->

        <!-- HTML Content Start -->
        <div class="ten_root">
            <div class="ten_header_pad"></div>
            <div class="whats-new-container">
                <section class="ten_banner">
                    <div class="ten_banner_swiper swiper-container inited swiper-container-initialized swiper-container-horizontal"
                        data-breakpoint="0:1" data-spacing="0" data-autoplay="8000" data-nav=".ten_banner_bullet"
                        data-prev=".ten_banner_arr_l" data-next=".ten_banner_arr_r" data-nav-click="1">
                        <div class="ten_banner_wrapper swiper-wrapper"
                            style="transition-duration: 300ms; transform: translate3d(-3810px, 0px, 0px);">
                            <div class="ten_banner_slide swiper-slide swiper-slide-duplicate swiper-slide-duplicate-active"
                                style="cursor: pointer; width: 1905px;" data-swiper-slide-index="1">
                                <a href="https://www.futurebasics.co.tz" target="_blank">
                                    <!-- <a href="https://static.www.futurebasics.com/uploads/2021/08/18/236f212d95d7402bacdbdf904a6b2b65.pdf" target="_blank">
            -->
                                    <img src="img/index/banner/nile.jpg" alt="Fin Release">
                                    <div class="ten_banner_shadow ten_banner_shadow--20"></div>
                                    <div class="ten_banner_text">
                                        <div class="ten_main">
                                            <h2>
                                                Building a digital future for everyone
                                            </h2>
                                            <h5>Details on Future Basics financial performance.</h5>
                                        </div>
                                    </div>
                                </a>
                            </div>
                            <div class="ten_banner_slide swiper-slide swiper-slide-prev swiper-slide-duplicate-next"
                                style="cursor: pointer; width: 1905px;" data-swiper-slide-index="0">
                                <a href="http://www.futurebasics.co.tz" target="_blank">
                                    <img class="banner-img" src="img/index/banner/nile.jpg"
                                        alt="futurebasics Perspectives">
                                    <div class="ten_banner_shadow ten_banner_shadow--10"></div>
                                    <div class="ten_banner_text">
                                        <div class="ten_main">
                                            <h2>Supporting #Local #Businesses with Technology solutions</h2>
                                            <h5>Building integrated communities, markets and business by leveraging
                                                Technology.</h5>
                                        </div>
                                    </div>
                                </a>
                            </div>
                            <div class="ten_banner_slide swiper-slide swiper-slide-active"
                                style="cursor: pointer; width: 1905px;" data-swiper-slide-index="1">
                                <a href="http://www.futurebasics.co.tz"
                                    target="_blank">
                                    <img src="img/some/cds.JPG" alt="Financial Release">
                                    <div class="ten_banner_shadow ten_banner_shadow--20"></div>
                                    <div class="ten_banner_text">
                                        <div class="ten_main">
                                            <h2>Innovative Solutions for Businesses, #Anywhere
                                            </h2>
                                            <h5>Stepping on time with creativity, for efficiency.</h5>
                                        </div>
                                    </div>
                                </a>
                            </div>
                            <div class="ten_banner_slide swiper-slide swiper-slide-duplicate swiper-slide-next swiper-slide-duplicate-prev"
                                style="cursor: pointer; width: 1905px;" data-swiper-slide-index="0">
                                <a href="http://www.futurebasics.co.tz" target="_blank">
                                    <img class="banner-img" src="img/index/banner/runner.jpg"
                                        alt="futurebasics Perspectives">
                                    <div class="ten_banner_shadow ten_banner_shadow--10"></div>
                                    <div class="ten_banner_text">
                                        <div class="ten_main">
                                            <h2>Providing simplified #Technology solutions</h2>
                                            <h5>Meet a few of our exceptional teammates driving innovation and using
                                                tech for good in this new series for futurebasics Perspectives. </h5>
                                        </div>
                                    </div>
                                </a>
                            </div>
                        </div>
                        <div class="ten_banner_nav">
                            <div class="ten_main">
                                <div class="ten_banner_arr">
                                    <span href="#" class="ten_banner_arr_l" tabindex="0" role="button"
                                        aria-label="Previous slide"></span>
                                    <span href="#" class="ten_banner_arr_r" tabindex="0" role="button"
                                        aria-label="Next slide"></span>
                                </div>
                                <div class="ten_banner_bullet swiper-pagination-clickable swiper-pagination-bullets">
                                    <span class="swiper-pagination-bullet" tabindex="0" role="button"
                                        aria-label="Go to slide 1"></span><span
                                        class="swiper-pagination-bullet swiper-pagination-bullet-active" tabindex="0"
                                        role="button" aria-label="Go to slide 2"></span></div>
                            </div>
                        </div>
                        <span class="swiper-notification" aria-live="assertive" aria-atomic="true"></span>
                    </div>
                </section>

            </div>


            <!--Section1-->
            <section>
                <div class="ten_main">
                    <div class="ten_links">
                        <a href="{{ route('about') }}" class="ten_img">
                            <img src="img/index/banner/open.jpg" alt="About Us">
                            <div class="ten_img_txt">
                                <h2>About Us</h2>
                            </div>
                        </a>
                        <a href="{{ route('about') }}" class="ten_img">
                            <img src="img/pics/teach.jpg" alt="Our Culture">
                            <div class="ten_img_txt">
                                <h2>Our Culture</h2>
                            </div>
                        </a>
                        <a href="{{ route('about') }}" class="ten_img">
                            <img src="img/pics/tina.jpg" alt="Our Offices">
                            <div class="ten_img_txt">
                                <h2>Our Offices</h2>
                            </div>
                        </a>
                    </div>
                </div>
            </section>
            <!--Section1-->

            <!--Section2-->
            <div class="ten_bg--dark">
                <div class="ten_main">
                    <div class="ten_home--mobile">
                        <div class="ten_img ten_img ten_img--5x2">
                            <img src="img/index/about/abt-us.jpg" alt="FutureBasics">
                            <div class="ten_img_shadow ten_img_shadow--vert"></div>
                            <div class="ten_img_txt ten_img_txt--bottom">
                                <a href="{{ route('business') }}">
                                    <h2>Supporting Business Development</h2>
                                    <p>Improving Efficiency and ease of operation</p>
                                </a>
                            </div>
                        </div>
                        <div class="ten_img ten_img ten_img--5x2">
                            <img src="img/index/banner/dada.jpg" alt="FutureBasics">
                            <div class="ten_img_shadow ten_img_shadow--vert"></div>
                            <div class="ten_img_txt ten_img_txt--bottom">
                                <a href="{{ route('business') }}">
                                    <h2>Bridging the Gap to Digitization</h2>
                                    <p>Guidance and assistance into the Digital World</p>
                                </a>
                            </div>
                        </div>
                        <div class="ten_img ten_img ten_img--5x2">
                            <img src="img/index/about/stair.jpg" alt="FutureBasics">
                            <div class="ten_img_shadow ten_img_shadow--vert"></div>
                            <div class="ten_img_txt ten_img_txt--bottom">
                                <a href="{{ route('business') }}">
                                    <h2>Supporting development spaces</h2>
                                    <p>Making progress through digitization</p>
                                </a>
                            </div>
                        </div>
                    </div>
                    <div class="ten_home">
                        <div class="ten_home_l">
                            <a href="{{ route('business') }}" class="" data-target="home1">
                                <h2>Supporting Business Development</h2>
                                <p>Improving Efficiency and ease of operation</p>
                            </a>
                            <a href="{{ route('business') }}"
                                data-target="home2" class="active">
                                <h2>Bridging the Gap to Digitization</h2>
                                <p>Guidance and assistance into the Digital World</p>
                            </a>
                            <a href="{{ route('business') }}"
                                data-target="home3" class="">
                                <h2>Supporting development spaces</h2>
                                <p>Making progress through digitization</p>
                            </a>
                        </div>
                        <div class="ten_home_r">
                            <div class="ten_home_card" id="home1">
                                <div class="ten_img ten_img ten_img--5x4">
                                    <img src="img/pics/auto-tina.jpg" alt="FutureBasics">
                                    <div class="ten_img_shadow ten_img_shadow--vert"></div>
                                    <div class="ten_img_txt ten_img_txt--bottom">
                                        <a href="{{ route('business') }}">
                                            <h3>Automate your Business</h3>
                                            <p>Offering a comprehensive suite of communications and social services that
                                                connect people to make accurate business decisions.</p>
                                        </a>
                                    </div>
                                </div>
                                <div class="ten_img ten_img ten_img--5x4">
                                    <img src="img/pics/bs-ppl.jpg" alt="FutureBasics">
                                    <div class="ten_img_shadow ten_img_shadow--vert"></div>
                                    <div class="ten_img_txt ten_img_txt--bottom">
                                        <a href="{{ route('business') }}">
                                            <h3>Moving online</h3>
                                            <p>Delivering high-quality content through industry-leading technologies, to
                                                shape our next-generation social and content offering.</p>
                                        </a>
                                    </div>
                                </div>
                                <div class="ten_img ten_img ten_img--5x4">
                                    <img src="img/index/banner/nile.jpg" alt="FutureBasics">
                                    <div class="ten_img_shadow ten_img_shadow--vert"></div>
                                    <div class="ten_img_txt ten_img_txt--bottom">
                                        <a href="{{ route('business') }}">
                                            <h3>Business systems development</h3>
                                            <p>Connecting users to merchants via fast and secure payment service,
                                                and to financial institutions via innovative consumer finance products.
                                            </p>
                                        </a>
                                    </div>
                                </div>
                                <div class="ten_img ten_img ten_img--5x4">
                                    <img src="img/index/tiles/growth.jpg" alt="FutureBasics">
                                    <div class="ten_img_shadow ten_img_shadow--vert"></div>
                                    <div class="ten_img_txt ten_img_txt--bottom">
                                        <a href="{{ route('business') }}">
                                            <h3>Assisting Expansion & Centralization</h3>
                                            <p>Developing a range of powerful software tools to meet the evolving needs
                                                of users.</p>
                                        </a>
                                    </div>
                                </div>
                            </div>
                            <div class="ten_home_card active" id="home2">
                                <div class="ten_img ten_img ten_img--5x4">
                                    <img src="img/some/offc.JPG" alt="FutureBasics">
                                    <div class="ten_img_shadow ten_img_shadow--vert"></div>
                                    <div class="ten_img_txt ten_img_txt--bottom">
                                        <a
                                            href="{{ route('business') }}">
                                            <h3>Online presence</h3>
                                            <p>A leading big data marketing platform.</p>
                                        </a>
                                    </div>
                                </div>
                                <div class="ten_img ten_img ten_img--5x4">
                                    <img src="img/pics/buildbus.jpg" alt="FutureBasics">
                                    <div class="ten_img_shadow ten_img_shadow--vert"></div>
                                    <div class="ten_img_txt ten_img_txt--bottom">
                                        <a
                                            href="{{ route('business') }}">
                                            <h3>Build with us your business system</h3>
                                            <p>Building industry-leading cloud-based products and services to support
                                                enterprises to go digital and go global.</p>
                                        </a>
                                    </div>
                                </div>
                                <div class="ten_img ten_img ten_img--5x2">
                                    <img src="img/some/top.JPG" alt="FutureBasics">
                                    <div class="ten_img_shadow ten_img_shadow--vert"></div>
                                    <div class="ten_img_txt ten_img_txt--bottom">
                                        <a
                                            href="{{ route('business') }}">
                                            <h3>Digital Data Management</h3>
                                            <p>Leveraging cutting-edge Internet technologies and products, including
                                                cloud, AI, big data analytics, security, payments, Mini Programs,
                                                location-based services and more, to assist industries to digital
                                                upgrade with our smart industry solutions.</p>
                                        </a>
                                    </div>
                                </div>
                            </div>
                            <div class="ten_home_card" id="home3">
                                <div class="ten_img ten_img ten_img--5x4">
                                    <img src="img/index/tiles/tobuy.jpg" alt="FutureBasics">
                                    <div class="ten_img_shadow ten_img_shadow--vert"></div>
                                    <div class="ten_img_txt ten_img_txt--bottom">
                                        <a
                                            href="{{ route('business') }}">
                                            <h3>Large and small scale enterprises</h3>
                                            <p>Enhancing the research and application of artificial intelligence to
                                                benefit mankind.</p>
                                        </a>
                                    </div>
                                </div>
                                <div class="ten_img ten_img ten_img--5x4">
                                    <img src="img/pics/moro.JPG" alt="FutureBasics">
                                    <div class="ten_img_shadow ten_img_shadow--vert"></div>
                                    <div class="ten_img_txt ten_img_txt--bottom">
                                        <a
                                            href="{{ route('business') }}">
                                            <h3>Businesses</h3>
                                            <p>Providing a full-stack of IoT products and solutions across a broad range
                                                of devices and applications.</p>
                                        </a>
                                    </div>
                                </div>
                                <div class="ten_img ten_img ten_img--5x4">
                                    <img src="img/index/tiles/org.jpg" alt="FutureBasics">
                                    <div class="ten_img_shadow ten_img_shadow--vert"></div>
                                    <div class="ten_img_txt ten_img_txt--bottom">
                                        <a
                                            href="{{ route('business') }}">
                                            <h3>Organizations</h3>
                                            <p>Focus on audio and video communications technologies.</p>
                                        </a>
                                    </div>
                                </div>
                                <div class="ten_img ten_img ten_img--5x4">
                                    <img src="img/index/tiles/comm.jpg" alt="FutureBasics">
                                    <div class="ten_img_shadow ten_img_shadow--vert"></div>
                                    <div class="ten_img_txt ten_img_txt--bottom">
                                        <a href="{{ route('business') }}">
                                            <h3>Communities</h3>
                                            <p>Collaborating with partners to explore new frontiers and develop
                                                technologies.</p>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!--Section1-->

            <!--Banner1-->
            <section class="ten_subbanner ten_subbanner--type1">
                <div class="ten_main">
                    <div class="swiper-container inited swiper-container-fade swiper-container-initialized swiper-container-horizontal"
                        data-breakpoint="0:1" data-spacing="0" data-autoplay="5000" data-effect="fade"
                        data-prev=".ten_banner_arr_l" data-next=".ten_banner_arr_r">
                        <div class="swiper-wrapper" style="transition-duration: 0ms;">
                            <div class="swiper-slide swiper-slide-duplicate" data-swiper-slide-index="3"
                                style="width: 600px; transition-duration: 0ms; opacity: 0; transform: translate3d(0px, 0px, 0px);">
                                <div class="ten_img ten_img--1x1">
                                    <img src="img/index/prod/radar.jpg" alt="FutureBasics">
                                    <div class="ten_img_shadow ten_img_shadow--vert"></div>
                                    <div class="ten_img_txt ten_img_txt--bottom">
                                        <a>
                                            <h3>Radarmile</h3>
                                            <p>A digital software that allows project enablers to monitor projects
                                                remotely by receiving real time activity data from across the
                                                implementation chain.</p>
                                        </a>
                                    </div>
                                </div>
                            </div>
                            <div class="swiper-slide swiper-slide-active" data-swiper-slide-index="0"
                                style="width: 600px; transition-duration: 0ms; opacity: 0; transform: translate3d(-600px, 0px, 0px);">
                                <div class="ten_img ten_img--1x1">
                                    <img src="img/index/prod/nak.jpg" alt="FutureBasics">
                                    <div class="ten_img_shadow ten_img_shadow--vert"></div>
                                    <div class="ten_img_txt ten_img_txt--bottom">
                                        <!-- <a href="https://www.futurebasics.co.tz/en-us/responsibility/combat-covid-19.html"> -->
                                        <a href="#">
                                            <h3>Inspektor </h3>
                                            <p>An online tool that facilitates and tracks business inspections.</p>
                                        </a>
                                    </div>
                                </div>
                            </div>
                            <div class="swiper-slide swiper-slide-prev" data-swiper-slide-index="1"
                                style="width: 600px; transition-duration: 0ms; opacity: 1; transform: translate3d(-1200px, 0px, 0px);">
                                <div class="ten_img ten_img--1x1">
                                    <img src="img/index/prod/inspect.jpg" alt="FutureBasics">
                                    <div class="ten_img_shadow ten_img_shadow--vert"></div>
                                    <div class="ten_img_txt ten_img_txt--bottom">
                                        <a>
                                            <h3>Naqualify</h3>
                                            <p>An online platform that provides an accommodating online certification
                                                environment by allowing organizations to post online courses for their
                                                intended demographic which upon completion, individuals receive credible
                                                qualification certificates.</p>
                                        </a>
                                    </div>
                                </div>
                            </div>

                        </div>
                        <div class="ten_subbanner_nav">
                            <div class="ten_banner_arr">
                                <a href="#" class="ten_banner_arr_l" tabindex="0" role="button"
                                    aria-label="Previous slide"></a>
                                <a href="#" class="ten_banner_arr_r" tabindex="0" role="button"
                                    aria-label="Next slide"></a>
                            </div>
                        </div>
                        <span class="swiper-notification" aria-live="assertive" aria-atomic="true"></span>
                    </div>
                    <div class="ten_subbanner_txt">
                        <a href="{{ route('business') }}">
                            <h2>Normalizing <br>Efficiency</h2>
                            <h5>Through technology, we provide access to simpler, smarter, more valuable business
                                solutions</h5>
                            <p><span class="ten_subbanner_arr"></span></p>
                        </a>
                    </div>
                </div>
            </section>
            <!--Banner1-->

            <!--Banner2-->
            <section class="ten_subbanner ten_subbanner--type2">
                <div class="swiper-container inited swiper-container-fade swiper-container-initialized swiper-container-horizontal"
                    data-breakpoint="0:1" data-spacing="0" data-autoplay="5000" data-effect="fade"
                    data-prev=".ten_banner_arr_l" data-next=".ten_banner_arr_r" data-nav=".ten_subbanner_bullet"
                    data-nav-click="1">
                    <div class="ten_subbanner_txt">
                        <div class="ten_main">
                            <!-- <a href="https://www.futurebasics.co.tz/en-us/employees.html"> -->
                            <a href="#">
                                <h2>Digitization of <br>Business <br>processes</h2>
                                <h5>We introduce innovation and technology to improve industry<br> growth, operations
                                    accuracy and improve data integrity</h5>
                                <p><span class="ten_subbanner_arr"></span></p>
                            </a>
                        </div>
                    </div>
                    <div class="swiper-wrapper" style="transition-duration: 0ms;">
                        <div class="swiper-slide swiper-slide-duplicate swiper-slide-next swiper-slide-duplicate-prev"
                            data-swiper-slide-index="2"
                            style="width: 1905px; transition-duration: 0ms; opacity: 0; transform: translate3d(0px, 0px, 0px);">
                            <div class="ten_img ten_img--2x1"><img src="img/index/about/2.jpg" alt="FutureBasics"></div>
                        </div>
                        <div class="swiper-slide swiper-slide-duplicate-active" data-swiper-slide-index="0"
                            style="width: 1905px; transition-duration: 0ms; opacity: 0; transform: translate3d(-1905px, 0px, 0px);">
                            <div class="ten_img ten_img--2x1"><img src="img/index/about/2.jpg" alt="FutureBasics"></div>
                        </div>
                        <div class="swiper-slide" data-swiper-slide-index="1"
                            style="width: 1905px; transition-duration: 0ms; opacity: 0; transform: translate3d(-3810px, 0px, 0px);">
                            <div class="ten_img ten_img--2x1"><img src="img/index/about/3.jpg" alt="FutureBasics"></div>
                        </div>
                        <div class="swiper-slide swiper-slide-prev swiper-slide-duplicate-next"
                            data-swiper-slide-index="2"
                            style="width: 1905px; transition-duration: 0ms; opacity: 0; transform: translate3d(-5715px, 0px, 0px);">
                            <div class="ten_img ten_img--2x1"><img src="img/index/about/business.jpg"
                                    alt="FutureBasics"></div>
                        </div>
                        <div class="swiper-slide swiper-slide-duplicate swiper-slide-active" data-swiper-slide-index="0"
                            style="width: 1905px; transition-duration: 0ms; opacity: 1; transform: translate3d(-7620px, 0px, 0px);">
                            <div class="ten_img ten_img--2x1"><img src="img/index/about/business.jpg"
                                    alt="FutureBasics"></div>
                        </div>
                    </div>
                    <div class="ten_subbanner_nav">
                        <div class="ten_main">
                            <div class="ten_banner_arr">
                                <span class="ten_banner_arr_l" tabindex="0" role="button"
                                    aria-label="Previous slide"></span>
                                <span class="ten_banner_arr_r" tabindex="0" role="button"
                                    aria-label="Next slide"></span>
                            </div>
                            <div class="ten_subbanner_bullet swiper-pagination-clickable swiper-pagination-bullets">
                                <span class="swiper-pagination-bullet swiper-pagination-bullet-active" tabindex="0"
                                    role="button" aria-label="Go to slide 1"></span><span
                                    class="swiper-pagination-bullet" tabindex="0" role="button"
                                    aria-label="Go to slide 2">

                                </span><span class="swiper-pagination-bullet" tabindex="0" role="button"
                                    aria-label="Go to slide 3"></span>
                            </div>
                        </div>
                    </div>
                    <span class="swiper-notification" aria-live="assertive" aria-atomic="true"></span>
                </div>
            </section>
            <!--Banner2-->
        </div>
        <!-- HTML Content End -->
        <script src="https://js.aq.qq.com/js/aq_common.js"></script>
        <script type="text/javascript" src="/js/jquery.min.js"></script>
        <script type="text/javascript" src="/js/swiper-3.4.0.jquery.min.js"></script>
        <script type="text/javascript" src="/js/js.js"></script>
        <script type="text/javascript" src="/js/js-2.js"></script>
        <script type="text/javascript" src="/js/swiper.min.js"></script>
        <script type="text/javascript" src="/js/qrcode.js"></script>
        <script type="text/javascript" src="/js/futurebasics.js"></script>
        <script type="text/javascript" src="/js/imgsize.js"></script>
        <script type="text/javascript" src="/js/yearpicker.js"></script>
        <script type="text/javascript" src="/js/jquery-throttle-debounce.js"></script>

        <!-- JS Content Start -->
        <script>
            if ($(document).scrollTop() >= $('.wrap_head').height()) {
                $('.wrap_head').addClass('head_white');
            } else {
                $('.wrap_head').removeClass('head_white');
            }
            $(window).scroll(function (event) {
                if ($(document).scrollTop() >= $('.wrap_head').height()) {
                    $('.wrap_head').addClass('head_white');
                } else {
                    $('.wrap_head').removeClass('head_white');
                }
            })

        </script>
        <!-- JS Content End -->


        <!-- Footer -->
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
