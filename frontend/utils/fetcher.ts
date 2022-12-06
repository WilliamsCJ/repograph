const fetcher = (url_path: string) => fetch(import.meta.env.VITE_BACKEND_URL + url_path, ).then((res) => res.json());

export default fetcher;