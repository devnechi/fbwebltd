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
                        {{-- <a href="#contact" class="ml-4 text-sm text-gray-700  navbrand-text"> Contact
                            us</a> --}}
                        <a href="{{ route('login') }}" class="ml-4 text-sm text-gray-700  navbrand-text"> Log in</a>

                        {{-- @if (Route::has('register'))
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
     {{-- <main class="py-4"> --}}
      @yield('content')
      {{-- end of content --}}
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
{{-- </main> --}}


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
