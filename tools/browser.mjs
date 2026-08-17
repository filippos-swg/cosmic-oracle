/* Shared browser launcher for the Playwright harnesses.

   The executable path must not be hardcoded: the cloud container these were
   written in keeps Chromium at /opt/pw-browsers/chromium, which does not exist
   on the installation Mac. Resolution order:

     1. $ASTRA_CHROMIUM              — explicit override
     2. /opt/pw-browsers/chromium    — the cloud container, if present
     3. Playwright's own bundled browser (the normal case on a Mac)

   If none resolve, the error tells you the one command that fixes it rather
   than leaving a stack trace. */
import { existsSync } from 'node:fs';
import { chromium } from 'playwright';

const CONTAINER_CHROMIUM = '/opt/pw-browsers/chromium';

export async function launchChromium(opts = {}) {
  const launchOpts = { ...opts };
  const explicit = process.env.ASTRA_CHROMIUM;
  if (explicit) launchOpts.executablePath = explicit;
  else if (existsSync(CONTAINER_CHROMIUM)) launchOpts.executablePath = CONTAINER_CHROMIUM;
  // else: no executablePath — Playwright resolves its own download

  try {
    return await chromium.launch(launchOpts);
  } catch (err) {
    if (/executable doesn't exist|Executable doesn't exist/i.test(String(err))) {
      console.error(
        '\n  Chromium is not installed for Playwright.\n' +
        '  Run this once:\n\n      npx playwright install chromium\n\n' +
        '  Or point at a browser you already have:\n\n' +
        '      ASTRA_CHROMIUM=/path/to/chromium npm run edge\n'
      );
      process.exit(2);
    }
    throw err;
  }
}
