{{-- @extends('layouts.app') --}}
@extends('layouts.admin-app-layout')
@section('content')
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">{{ __('Dashboard') }}</div>

                <div class="card-body">
                    @if (session('status'))
                        <div class="alert alert-success" role="alert">
                            {{ session('status') }}
                        </div>
                    @endif

                    {{ __('You are logged in admin!') }}
                    <ul class="nav navbar-nav justify-content-end" style="display: contents;">
                        <li><a href="#">Welcome, <strong style="color: #a7a4a2;">{{ auth()->user()->usertype_id }}</strong></a></li>
                        </ul>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
