const puppeteer = require('puppeteer');
const fs = require('fs');
const os = require('node:os');
const path = require('path');

(async () => {
    const browser = await puppeteer.launch();

    const page = await browser.newPage();

    const web_url = path.join(__dirname, '..','..','..','data','output','example.html');
    const html = fs.readFileSync(web_url, 'utf-8');
    await page.setContent(html, {waitUntil: 'domcontentloaded'});

    await page.emulateMediaType('screen');

    const pdf = await page.pdf({
        path : path.join(__dirname, '..','..','..','data', 'output', 'exampleOutput.pdf'),
        margin: { top: '100px', right: '50px', bottom: '100px', left:'50px'},
        printBackground: true,
        format: 'A4',
    });

    await browser.close();

})();