#!/usr/bin/env node

/**
 * IntelliSustain Logo Setup Script
 * 
 * This script helps set up the IntelliSustain logo files for the application.
 * Run this script to ensure all logo files are properly configured.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('🎨 IntelliSustain Logo Setup');
console.log('============================\n');

// Check if logo files exist
const publicDir = path.join(__dirname, 'public');
const logoFiles = [
  'intellisustain-logo.svg',
  'logo-converter.html',
  'LOGO_README.md'
];

console.log('Checking logo files...\n');

logoFiles.forEach(file => {
  const filePath = path.join(publicDir, file);
  if (fs.existsSync(filePath)) {
    console.log(`✅ ${file} - Found`);
  } else {
    console.log(`❌ ${file} - Missing`);
  }
});

console.log('\n📋 Logo Setup Instructions:');
console.log('1. Open logo-converter.html in a web browser');
console.log('2. Click "Download PNG Logo" to get intellisustain-logo.png');
console.log('3. Save the PNG file to the frontend/public folder');
console.log('4. The logo will automatically appear in the UI\n');

console.log('🎯 Logo Features:');
console.log('- SVG format for crisp display');
console.log('- React component with fallback');
console.log('- Responsive design');
console.log('- Professional branding\n');

console.log('🚀 Ready to use IntelliSustain branding!'); 