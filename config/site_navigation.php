<?php

// Public navigation visibility. Keep Portfolio routes and content intact.
// Re-enable by setting FB_SHOW_PORTFOLIO=true and refreshing Laravel config cache.
return [
    'show_portfolio' => env('FB_SHOW_PORTFOLIO', false),
];
