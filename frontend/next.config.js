const withTwin = require("./withTwin.js");

/** @type {import('next').NextConfig} */
module.exports = withTwin({
  reactStrictMode: false,
  output: "standalone",
  typescript: {
    ignoreBuildErrors: true,
  },
  i18n: {
    locales: ["en"],
    defaultLocale: "en"
  },
});
