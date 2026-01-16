#!/usr/bin/env node
/**
 * Patch libpq to suppress noisy console.log output
 * libpq prints __dirname/src on import when !module.parent is true (which happens in ESM)
 */

import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const libpqPath = path.join(__dirname, '../node_modules/libpq/index.js');

try {
  let content = fs.readFileSync(libpqPath, 'utf8');
  
  // Check if already patched
  if (content.includes('// PATCHED:')) {
    console.log('libpq already patched');
    process.exit(0);
  }
  
  // Replace the noisy console.log block
  const original = `if (!module.parent) {
  var path = require('path');
  console.log(path.normalize(__dirname + '/src'));
}`;
  
  const patched = `// PATCHED: Suppress noisy output in ESM
if (false && !module.parent) {
  var path = require('path');
  console.log(path.normalize(__dirname + '/src'));
}`;
  
  if (content.includes(original)) {
    content = content.replace(original, patched);
    fs.writeFileSync(libpqPath, content);
    console.log('libpq patched successfully');
  } else {
    console.log('libpq patch target not found (may have different version)');
  }
} catch (err) {
  console.error('Failed to patch libpq:', err.message);
  process.exit(1);
}
