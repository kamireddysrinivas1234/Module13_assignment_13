import { test, expect } from '@playwright/test';

function randomEmail() {
  const rand = Math.random().toString(16).slice(2);
  return `user_${rand}@example.com`;
}

test.describe('JWT Auth E2E', () => {
  test('Positive: Register with valid data shows success and stores token', async ({ page }) => {
    const email = randomEmail();
    const password = 'StrongPass123!';

    await page.goto('/static/register.html');
    await page.fill('#email', email);
    await page.fill('#password', password);
    await page.fill('#confirm', password);
    await page.click('#submitBtn');

    const msg = page.locator('#message');
    await expect(msg).toBeVisible();
    await expect(msg).toContainText('Registration successful');

    const token = await page.evaluate(() => localStorage.getItem('jwt_token'));
    expect(token).toBeTruthy();
    expect(token!.split('.').length).toBe(3);
  });

  test('Positive: Login with correct credentials shows success and stores token', async ({ page }) => {
    const email = randomEmail();
    const password = 'StrongPass123!';

    await page.goto('/static/register.html');
    await page.fill('#email', email);
    await page.fill('#password', password);
    await page.click('#submitBtn');
    await expect(page.locator('#message')).toContainText('Registration successful');

    await page.goto('/static/login.html');
    await page.fill('#email', email);
    await page.fill('#password', password);
    await page.click('#submitBtn');

    const msg = page.locator('#message');
    await expect(msg).toBeVisible();
    await expect(msg).toContainText('Login successful');

    const token = await page.evaluate(() => localStorage.getItem('jwt_token'));
    expect(token).toBeTruthy();
  });

  test('Negative: Register with short password shows front-end validation error', async ({ page }) => {
    const email = randomEmail();
    const password = 'short';

    await page.goto('/static/register.html');
    await page.fill('#email', email);
    await page.fill('#password', password);
    await page.click('#submitBtn');

    const msg = page.locator('#message');
    await expect(msg).toBeVisible();
    await expect(msg).toContainText('at least 8 characters');
  });

  test('Negative: Login with wrong password returns 401 and UI shows invalid credentials', async ({ page }) => {
    const email = randomEmail();
    const password = 'StrongPass123!';

    await page.goto('/static/register.html');
    await page.fill('#email', email);
    await page.fill('#password', password);
    await page.click('#submitBtn');
    await expect(page.locator('#message')).toContainText('Registration successful');

    await page.goto('/static/login.html');
    await page.fill('#email', email);
    await page.fill('#password', 'WrongPassword!');
    await page.click('#submitBtn');

    const msg = page.locator('#message');
    await expect(msg).toBeVisible();
    await expect(msg).toContainText('Invalid credentials');
  });
});
