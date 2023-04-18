const puppeteer = require('puppeteer');
const fs = require('fs');
const assert = require('assert');
const os = require('node:os');
const path = require('path');
const { PDFDocument } = require('pdf-lib');

const run = (async () => {

    var inputName = process.argv[2];
    var outputName = process.argv[3];

    const browser = await puppeteer.launch({dumpio:false , ignoreDefaultArgs: ['--disable-extensions','--enable-popup-blocking'], args: ['headless', '--no-sandbox', '--disable-setuid-sandbox','--disable-gpu'],});

    const page = await browser.newPage();

<<<<<<< HEAD
    var maxWidth = await page.evaluate(() => Math.max(document.body.scrollWidth, document.documentElement.clientWidth));

    const web_url = path.join(__dirname, '..','..','..','data','output',htmlName);
    const html = fs.readFileSync(web_url, 'utf-8');
=======
    const html = fs.readFileSync(inputName, 'utf-8');
>>>>>>> main
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