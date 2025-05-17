// testng_register_login.js

import { Builder, By, until } from 'selenium-webdriver';
import fs from 'fs';
import path from 'path';
import log4js from 'log4js';
import { expect } from 'chai';
import { fileURLToPath } from 'url';

// ESM fix for __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Logging setup
log4js.configure({
  appenders: { file: { type: 'file', filename: 'assignment_register_login.log' } },
  categories: { default: { appenders: ['file'], level: 'info' } }
});
const logger = log4js.getLogger('default');

describe("User Registration & Login Flow (TestNG Style)", function () {
  let driver;
  const baseUrl = "https://nodedatabase.onrender.com";
  const username = "Nasko2345";
  const password = "Nasko2345!";

  this.timeout(60000);

  before(async function () {
    driver = await new Builder().forBrowser("chrome").build();
    logger.info("✅ WebDriver started");
  });

  it("1️⃣ should register a new user", async function () {
    await driver.get(`${baseUrl}/users/add`);
    logger.info("🌐 Opened registration page");

    await driver.findElement(By.id("name")).sendKeys(username);
    await driver.findElement(By.id("password")).sendKeys(password);
    await driver.findElement(By.id("role")).sendKeys("general");
    await driver.findElement(By.css("button[type='submit']")).click();

    logger.info("📝 Submitted registration form");

    const filePath = path.join(__dirname, `screenshots/register_success.png`);
    const screenshot = await driver.takeScreenshot();
    fs.writeFileSync(filePath, screenshot, 'base64');
    logger.info(`📸 Screenshot saved: ${filePath}`);
  });

  it("2️⃣ should login with the new user", async function () {
    await driver.get(`${baseUrl}/users`);
    logger.info("🌐 Opened login page");

    await driver.findElement(By.id("name")).sendKeys(username);
    await driver.findElement(By.id("password")).sendKeys(password);
    await driver.findElement(By.css("button[type='submit']")).click();

    logger.info("🔐 Submitted login form");

    await driver.wait(until.urlContains("/dashboard"), 20000);
    const url = await driver.getCurrentUrl();
    expect(url).to.include("/dashboard");

    const filePath = path.join(__dirname, `screenshots/login_success.png`);
    const screenshot = await driver.takeScreenshot();
    fs.writeFileSync(filePath, screenshot, 'base64');
    logger.info(`📸 Screenshot saved: ${filePath}`);
  });

  after(async function () {
    if (driver) {
      await driver.quit();
      logger.info("🛑 WebDriver closed");
    }
  });
});
