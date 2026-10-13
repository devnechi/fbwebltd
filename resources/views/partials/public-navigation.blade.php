{{-- Public header shared by desktop and mobile. Portfolio remains available behind config flag. --}}
        <header class="main-header {{ $navVariant === 'dark' ? 'position-absolute w-100' : 'w-100' }}">
            <nav class="navbar navbar-expand-xl {{ $navVariant === 'dark' ? 'navbar-dark' : 'navbar-light' }} sticky-header">
                <div class="container d-flex align-items-center justify-content-lg-between position-relative">
                    <a href="{{ url('/') }}" class="navbar-brand d-flex align-items-center mb-md-0 text-decoration-none">
                        <img src="{{ asset('img/fb_og_logo.png') }}" alt="logo" class="img-fluid logo-white" />
                        <img src="{{ asset('img/fb_og_logo_drk.png') }}" alt="logo" class="img-fluid logo-color" />
                    </a>

                    <button class="navbar-toggler position-absolute right-0 border-0"
                            type="button"
                            data-bs-toggle="offcanvas"
                            data-bs-target="#offcanvasWithBackdrop"
                            aria-controls="offcanvasWithBackdrop"
                            aria-label="Open navigation menu">
                        <span class="far fa-bars" aria-hidden="true"></span>
                    </button>
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
                                            <a href="{{ route('all-web-development-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-globe"></i></span>
                                                <div class="drop-title">Website Design & Development</div>
                                            </a>

                                            <a href="{{ route('all-mobile-development-services') }}" class="dropdown-link">
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
                                                <span class="me-2"><i class="far fa-code-fork"></i></span>
                                                <div class="drop-title">Software Engineering</div>
                                            </a>
                                            <a href="{{ route('all-bus-sys-development-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-briefcase"></i></span>
                                                <div class="drop-title">Business System Development</div>
                                            </a>
                                            <a href="{{ route('all-branding-services') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-heartbeat"></i></span>
                                                <div class="drop-title">Branding & Digital Strategizing</div>
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
                                            <a href="#"><img src="{{ asset('img/about/bs-ppl.jpg') }}" alt="add" class="img-fluid rounded-custom" /></a>
                                        </div>
                                    </div>
                                </div>
                            </li>
                            @if(config('site_navigation.show_portfolio', false))
<li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="{{ route('business') }}" role="button" data-bs-toggle="dropdown" aria-expanded="false">Portfolio</a>
                                {{-- @guest
                                @if (Route::has('login'))
                                    <a href="{{ route('login') }}" class="btn btn-outline-primary me-2">Sign In</a>
                                @endif
                            @else
                            <a class="btn btn-outline-primary me-2" href="{{ route('logout') }}"
                                    onclick="event.preventDefault(); document.getElementById('logout-form').submit();">
                                    {{ __('Logout') }}
                                </a>
                                <form id="logout-form" action="{{ route('logout') }}" method="POST" class="d-none">
                                    @csrf
                                </form>

                            @endguest --}}
                                <div class="dropdown-menu border-0 rounded-custom shadow py-0 bg-white">
                                    <div class="dropdown-grid rounded-custom width-full">
                                        <div class="dropdown-grid-item">
                                            <h6 class="drop-heading">Enterprise Solutions</h6>
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link px-0">
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
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-code-branch"></i></span>
                                                <div class="drop-title">Smart Risiti</div>
                                            </a>
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-life-ring"></i></span>
                                                <div class="drop-title">Mennyu</div>
                                            </a>
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-headset"></i></span>
                                                <div class="drop-title">Tavrenni</div>
                                            </a>
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-laptop-code"></i></span>
                                                <div class="drop-title">Avorra</div>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </li>
@endif
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
                                <img src="{{ asset('img/fb_og_logo_drk.png') }}" alt="logo" class="img-fluid ps-2" />
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
                                    <a class="nav-link dropdown-toggle" href="{{ route('our-services') }}" role="button" data-bs-toggle="dropdown" aria-expanded="false">Our Services</a>
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
                                                <a href="{{ route('all-web-development-services') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-globe"></i></span>
                                                    <div class="drop-title">Website Design & Development</div>
                                                </a>

                                                <a href="{{ route('all-mobile-development-services') }}" class="dropdown-link">
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
                                                    <div class="drop-title">Software Engineering</div>
                                                </a>
                                                <a href="{{ route('all-bus-sys-development-services') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-briefcase"></i></span>
                                                    <div class="drop-title">Business System Development</div>
                                                </a>
                                                <a href="{{ route('all-branding-services') }}" class="dropdown-link">
                                                    <span class="me-2"><i class="far fa-heartbeat"></i></span>
                                                    <div class="drop-title">Branding & Digital Strategizing</div>
                                                </a>
                                            </div>
                                            <div class="dropdown-grid-item last-item bg-light radius-right-side">
                                                <a href="#"><img src="{{ asset('img/about/bs-ppl.jpg') }}" alt="add" class="img-fluid rounded-custom" /></a>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                @if(config('site_navigation.show_portfolio', false))
<li class="nav-item dropdown">
                                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Portfolio</a>
                                    <div class="dropdown-menu border-0 rounded-custom shadow py-0 bg-white">
                                        <div class="dropdown-grid rounded-custom width-full">
                                            <div class="dropdown-grid-item">
                                                <h6 class="drop-heading">Enterprise Solutions</h6>
                                                <a href="{{ route('coming-soon') }}" class="dropdown-link px-0">
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

                                            <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-code-branch"></i></span>
                                                <div class="drop-title">Smart Risiti</div>
                                            </a>
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-life-ring"></i></span>
                                                <div class="drop-title">Mennyu</div>
                                            </a>
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-headset"></i></span>
                                                <div class="drop-title">Tavrenni</div>
                                            </a>
                                            <a href="{{ route('coming-soon') }}" class="dropdown-link">
                                                <span class="me-2"><i class="far fa-laptop-code"></i></span>
                                                <div class="drop-title">Avorra</div>
                                            </div>
                                        </div>
                                    </div>
                                </li>
@endif
                            </ul>
                            <div class="action-btns mt-4 ps-3">
                                    @guest
                                        @if (Route::has('login'))
                                            <a href="{{ route('login') }}" class="btn btn-outline-primary me-2">Sign In</a>
                                        @endif
                                    @else
                                    <a class="btn btn-outline-primary me-2" href="{{ route('logout') }}"
                                            onclick="event.preventDefault(); document.getElementById('logout-form').submit();">
                                            {{ __('Logout') }}
                                        </a>
                                        <form id="logout-form" action="{{ route('logout') }}" method="POST" class="d-none">
                                            @csrf
                                        </form>

                                    @endguest
                                    <div>
                                        <a href="{{ route('contact-us') }}" class="btn btn-primary">Contact us</a>
                                    </div>
                            </div>

                        </div>
                       </div>
                    <!--offcanvas menu end-->
                </div>
            </nav>
        </header>
