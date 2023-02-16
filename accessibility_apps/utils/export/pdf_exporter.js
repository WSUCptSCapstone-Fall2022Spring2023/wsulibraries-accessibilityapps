const puppeteer = require('puppeteer');
const fs = require('fs');
const os = require('node:os');
const path = require('path');

(async () => {

    var htmlName = process.argv[2];
    var nameSplit = htmlName.split(".");
    var outputName = nameSplit[0]+ '.pdf';

    const browser = await puppeteer.launch({ignoreDefaultArgs: ['--disable-extensions'], args: ['--no-sandbox', '--disable-setuid-sandbox', '--enable-popup-blocking'],});

    const page = await browser.newPage();

    const web_url = path.join(__dirname, '..','..','..','data','output',htmlName);
    const html = fs.readFileSync(web_url, 'utf-8');
    await page.setContent(html, {waitUntil: 'domcontentloaded'});

    await page.emulateMediaType('screen');
    const pdf = await page.pdf({
        path:path.join(__dirname, '..','..','..','data', 'output', outputName),
        margin: { top:'100px', right:'50px', bottom:'100px', left:'50px'},
        printBackground:true,
        format:'A4',
    });

    await browser.close();

})();

//add css?
//work on formatting & font size
//test cases & shit
//steps to install on new comp