[Superguitartab.com](../../README.md) >
[Developer documentation](../README.md) >
Testing

# Testing

We run unit, integration, and end-to-end automated tests. These should be run before committing and pushing to branches.

These tests will also run as part of our CI pipeline which is ran on every Git push.

## End-to-end tests

You can find our end-to-end tests in our frontend folder client/tests/e2e.

To run the tests:
- Go into client directory
- Ensure Playwright is installed
- run `npx playwright test`

## Unit tests

We use Pytest for our unit tests