import '../styles/globals.css'
import dynamic from 'next/dynamic'

function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />
}

export default dynamic(() => Promise.resolve(MyApp), {
  ssr: false,
});