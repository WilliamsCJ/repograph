const fetcher = (url_path: string) =>
  fetch(
    `http://${
      process.env.NODE_ENV == "development" ? "localhost" : "repograph-backend"
    }:3000${url_path}`
  ).then((res) => res.json());

export default fetcher;
