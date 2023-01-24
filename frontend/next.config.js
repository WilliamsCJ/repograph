const withTwin = require("./withTwin.js");

/** @type {import('next').NextConfig} */
module.exports = withTwin({
  reactStrictMode: true,
  output: "standalone",
  typescript: {
    ignoreBuildErrors: true,
  },
});
