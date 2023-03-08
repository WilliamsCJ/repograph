const fetcher = (url_path: string) =>
  fetch("http://localhost:3000" + url_path).then((res) =>
    res.json()
  );

export default fetcher;
