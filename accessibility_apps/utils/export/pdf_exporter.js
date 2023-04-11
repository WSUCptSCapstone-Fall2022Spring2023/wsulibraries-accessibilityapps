const puppeteer = require('puppeteer');
const fs = require('fs');
const os = require('node:os');
const path = require('path');

(async () => {

    var inputName = process.argv[2];
    var outputName = process.argv[3];


    const browser = await puppeteer.launch({dumpio:false , ignoreDefaultArgs: ['--disable-extensions','--enable-popup-blocking'], args: ['headless', '--no-sandbox', '--disable-setuid-sandbox','--disable-gpu'],});

    const page = await browser.newPage();

    const html = fs.readFileSync(inputName, 'utf-8');
    await page.setContent(html, {waitUntil: 'domcontentloaded'});

    await page.emulateMediaType('screen');
    const pdf = await page.pdf({
        path:outputName,
        margin: { top:'100px', right:'50px', bottom:'100px', left:'50px'},
        printBackground:true,
        format:'A4',
    });

    await browser.close();

})();