const fetcher = (url_path: string) => fetch(process.env.NEXT_PUBLIC_BACKEND_URL + url_path, ).then((res) => res.json());

export default fetcher;