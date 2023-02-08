import tw from "twin.macro";
export const ApplicationBackground = tw`bg-zinc-100 dark:bg-zinc-900`;
export const Background = tw`bg-white dark:bg-zinc-800/50`;
export const Border = tw`border dark:border-zinc-700/50 border-gray-300 rounded-lg`;
export const InteriorBorder = tw`border border-zinc-200 dark:border-zinc-600 rounded-lg`;
export const Hover = tw`hover:bg-zinc-100/50 dark:hover:bg-zinc-700/50 hover:transition hover:ease-in-out hover:duration-300`;
export const AccentHover = tw`hover:bg-emerald-200/25 hover:bg-emerald-400/25 hover:transition hover:ease-in-out hover:duration-300`;
export const Divide = tw`divide-zinc-200 dark:divide-zinc-600`;
export const AccentBackground = tw`bg-emerald-400/25`;
export const ButtonText = tw`text-sm font-semibold text-zinc-800 dark:text-zinc-200`;
export const AccentText = tw`text-base font-semibold text-emerald-600 dark:text-emerald-400 dark:hover:text-emerald-300`;
export const AccentBorder = tw`border rounded-lg border-emerald-400 dark:border-emerald-700 dark:hover:border-emerald-200`;
export const Focus = tw`focus:outline-none focus:border-emerald-400 focus:ring-emerald-600 focus:ring-2 focus:ring-offset-2`;
export const FocusError = tw`focus:outline-none focus:border-red-400 focus:ring-red-600 focus:ring-2 focus:ring-offset-2`;
export const Placeholder = tw`text-zinc-700 dark:text-zinc-300`;
export const PlaceholderError = tw`text-red-700 dark:text-red-300`;
export const SelectedTab = tw`ui-selected:(
  bg-emerald-400/25 
  border rounded-lg border-emerald-400 dark:border-emerald-700 dark:hover:border-emerald-200
)`;
export const UnselectedTab = tw`ui-not-selected:(
  dark:hover:text-emerald-400 hover:text-emerald-600 hover:transition hover:ease-in-out hover:duration-300
)`;
