const assert = require('node:assert/strict');
const { chromium } = require('playwright');

const baseURL = process.env.TEST_BASE_URL || 'http://127.0.0.1:8765';

async function checkResponse(page, path) {
    const response = await page.goto(`${baseURL}${path}`, {
        waitUntil: 'load',
        timeout: 30000,
    });

    assert(response, `No HTTP response for ${path}`);
    assert.equal(response.status(), 200, `${path} returned HTTP ${response.status()}`);
}

async function main() {
    const browser = await chromium.launch({
        headless: true,
        executablePath: process.env.CHROME_BIN || '/usr/bin/google-chrome',
        args: ['--no-sandbox'],
    });

    try {
        // Desktop navigation.
        const desktop = await browser.newPage({
            viewport: { width: 1440, height: 900 },
        });

        await checkResponse(desktop, '/');

        assert.equal(
            await desktop.locator('nav.navbar-dark').count(),
            1,
            'Homepage should have dark navigation'
        );

        assert.equal(
            await desktop.locator('nav a:text-is("Portfolio")').count(),
            0,
            'Portfolio must be hidden by default'
        );

        const desktopServices = desktop.locator(
            'nav .collapse.navbar-collapse a.dropdown-toggle'
        ).first();

        await desktopServices.click();

        assert(
            await desktop.locator(
                'nav .collapse.navbar-collapse .dropdown-menu.show'
            ).count() > 0,
            'Desktop Services dropdown did not open'
        );

        // Inner page and public assets.
        await checkResponse(desktop, '/about');

        assert.equal(
            await desktop.locator('nav.navbar-light').count(),
            1,
            'About page should have light navigation'
        );

        const logo = desktop.locator(
            'nav .navbar-brand img.logo-color'
        ).first();

        const logoURL = await logo.getAttribute('src');
        assert(logoURL, 'Navigation logo URL is missing');

        const logoResponse = await desktop.request.get(logoURL);
        assert.equal(logoResponse.status(), 200, 'Navigation logo failed to load');

        // Service route and JavaScript availability.
        await checkResponse(desktop, '/all-web-development-services');

        const bootstrapAvailable = await desktop.evaluate(
            () => typeof window.bootstrap?.Offcanvas === 'function'
        );

        assert(bootstrapAvailable, 'Bootstrap offcanvas JavaScript is unavailable');

        // Existing business route must remain available.
        await checkResponse(desktop, '/business');

        // Mobile navigation.
        const mobile = await browser.newPage({
            viewport: { width: 390, height: 844 },
            isMobile: true,
            hasTouch: true,
        });

        await checkResponse(mobile, '/');

        const toggle = mobile.locator('button.navbar-toggler');
        const offcanvas = mobile.locator('#offcanvasWithBackdrop');

        await mobile.evaluate(() => {
            window.__offcanvasShown = false;

            document.querySelector('#offcanvasWithBackdrop')
                .addEventListener('shown.bs.offcanvas', () => {
                    window.__offcanvasShown = true;
                }, { once: true });
        });

        await toggle.click();

        await mobile.waitForFunction(
            () => window.__offcanvasShown === true,
            null,
            { timeout: 10000 }
        );

        const position = await offcanvas.boundingBox();

        assert(position, 'Mobile offcanvas has no bounding box');

        assert(
            position.x < 390 && position.x + position.width > 0,
            'Mobile offcanvas remains outside the viewport'
        );

        const finalState = await mobile.evaluate(() => {
            const element = document.querySelector('#offcanvasWithBackdrop');
            const style = getComputedStyle(element);
            const rect = element.getBoundingClientRect();

            return {
                className: element.className,
                inlineStyle: element.getAttribute('style'),
                display: style.display,
                visibility: style.visibility,
                opacity: style.opacity,
                transform: style.transform,
                transition: style.transition,
                rect: {
                    x: rect.x,
                    right: rect.right,
                    width: rect.width,
                    height: rect.height
                },
                viewportWidth: window.innerWidth,
                shownEventReceived: window.__offcanvasShown
            };
        });

        console.log(
            'FINAL OFFCANVAS STATE:',
            JSON.stringify(finalState, null, 2)
        );

        assert(
            await offcanvas.isVisible(),
            'Mobile offcanvas is not visible'
        );

        assert.equal(
            await offcanvas.locator('a:text-is("Portfolio")').count(),
            0,
            'Portfolio appears in mobile navigation'
        );

        await offcanvas.locator('a:text-is("Our Services")').click();

        assert(
            await offcanvas.locator('.dropdown-menu.show').count() > 0,
            'Mobile Services dropdown did not open'
        );

        await offcanvas.locator('[data-bs-dismiss="offcanvas"]').click();

        await mobile.waitForFunction(
            () => !document.querySelector('#offcanvasWithBackdrop')
                ?.classList.contains('show')
        );

        console.log('PASS: Desktop and mobile navigation smoke tests');
        console.log('PASS: Portfolio hidden; /business preserved');
        console.log('PASS: Public assets and Bootstrap JavaScript available');
    } finally {
        await browser.close();
    }
}

main().catch(error => {
    console.error(error);
    process.exit(1);
});
