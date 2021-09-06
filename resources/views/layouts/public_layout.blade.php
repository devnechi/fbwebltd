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


  <!-- <link rel="stylesheet" href="css/themify-icons.css"> -->
  <link rel="stylesheet" href="css/themefisher-fonts.css">
  <link rel="stylesheet" href="css/font-awesome.min.css">
  <link rel="stylesheet" href="css/owl.carousel.css">
  <link rel="stylesheet" href="css/animate.css">
  <link rel="stylesheet" href="css/style.css">
  <!-- Responsive Stylesheet -->
  <link rel="stylesheet" href="css/responsive.css">
  <link rel="stylesheet" href="css/themify-icons.css">



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

      <!--Navbar -->
     {{-- <main class="py-4"> --}}
      @yield('content')
      {{-- end of content --}}

{{-- </main> --}}

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
  {{-- <script>
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

  </script> --}}

  <!-- <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js" integrity="sha384-3ceskX3iaEnIogmQchP8opvBy3Mi7Ce34nWjpBIwVTHfGYWQS9jwHDVRnpKKHJg7" crossorigin="anonymous"></script> -->

  <script src="{{ mix('js/app.js') }}"></script>


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
