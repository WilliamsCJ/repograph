// import { createGlobalStyle } from "styled-components";
// import tw, { theme, GlobalStyles as BaseStyles } from "twin.macro";
//
// /**
//  * Custom TailwindCSS styles
//  */
// const CustomStyles = createGlobalStyle({
//   html: {
//     overflow: "hidden",
//     height: "100%",
//   },
//   body: {
//     height: "100%",
//     overflow: "auto",
//     WebkitTapHighlightColor: theme`colors.purple.500`,
//     ...tw`antialiased`,
//   },
// });
//
// /** GlobalStyles component combines BaseStyles and CustomStyles **/
// const GlobalStyles = () => (
//   <>
//     <BaseStyles />
//     <CustomStyles />
//   </>
// );
//
// export default GlobalStyles;


import React from 'react'
import { createGlobalStyle } from 'styled-components'
import tw, { theme, GlobalStyles as BaseStyles } from 'twin.macro'

const CustomStyles = createGlobalStyle({
  body: {
    WebkitTapHighlightColor: theme`colors.purple.500`,
    ...tw`antialiased`,
  },
})

const GlobalStyles = () => (
<>
  <BaseStyles />
  <CustomStyles />
</>
)

export default GlobalStyles