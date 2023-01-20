const withTwin = require('./withTwin.js')

/** @type {import('next').NextConfig} */
module.exports = withTwin({
  reactStrictMode: true,
<<<<<<< Updated upstream
  output: 'standalone'
=======
  output: "standalone",
  typescript: {
    ignoreBuildErrors: true,
  }
>>>>>>> Stashed changes
});
