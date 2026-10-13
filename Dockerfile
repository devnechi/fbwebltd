# TEMPORARY legacy runtime for Laravel 8. Upgrade Laravel/PHP before financial production use.
FROM php:8.1-fpm-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends libpng-dev libjpeg62-turbo-dev libfreetype6-dev libzip-dev libonig-dev libicu-dev unzip git \
 && docker-php-ext-configure gd --with-freetype --with-jpeg \
 && docker-php-ext-install -j"$(nproc)" pdo_mysql mbstring zip gd intl bcmath opcache \
 && rm -rf /var/lib/apt/lists/*
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer
WORKDIR /var/www/html
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-interaction --prefer-dist --no-progress --no-scripts --optimize-autoloader
COPY . .
RUN composer dump-autoload --no-dev --optimize --no-interaction \
 && mkdir -p storage/framework/cache/data storage/framework/sessions storage/framework/views storage/logs bootstrap/cache \
 && chown -R www-data:www-data storage bootstrap/cache
USER www-data
CMD ["php-fpm"]
