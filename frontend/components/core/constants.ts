import tw from "twin.macro";
export const ApplicationBackground = tw`bg-zinc-100 dark:bg-zinc-900`;
export const Background = tw`bg-white dark:bg-zinc-800/50`;
export const Border = tw`border dark:border-zinc-700/50 border-gray-300 rounded-lg`;
export const InteriorBorder = tw`border border-zinc-200 dark:border-zinc-600 rounded-lg`;
export const Hover = tw`hover:bg-zinc-100/50 dark:hover:bg-zinc-700/50 hover:transition hover:ease-in-out hover:duration-300`;
export const AccentHover = tw`hover:bg-accent-200/25 hover:bg-accent-400/25 hover:transition hover:ease-in-out hover:duration-300`;
export const Divide = tw`divide-zinc-200 dark:divide-zinc-600`;
export const AccentBackground = tw`bg-accent-400/25`;
export const ButtonText = tw`text-sm font-semibold text-zinc-800 dark:text-zinc-200`;
export const AccentText = tw`text-base font-semibold text-accent-600 dark:text-accent-400 dark:hover:text-accent-300`;
export const AccentBorder = tw`border rounded-lg border-accent-400 dark:border-accent-700 dark:hover:border-accent-200`;
export const Focus = tw`focus:outline-none focus:border-accent-400 focus:ring-accent-600 focus:ring-2 focus:ring-offset-2`;
export const FocusError = tw`focus:outline-none focus:border-red-400 focus:ring-red-600 focus:ring-2 focus:ring-offset-2`;
export const Placeholder = tw`text-zinc-700 dark:text-zinc-300`;
export const PlaceholderError = tw`text-red-700 dark:text-red-300`;
export const BorderError = tw`border border-2 dark:border-red-700/75 border-red-300 rounded-lg`;
export const SelectedTab = tw`ui-selected:(
  bg-accent-400/25 
  border rounded-lg border-accent-400 dark:border-accent-700 dark:hover:border-accent-200
)`;
export const UnselectedTab = tw`ui-not-selected:(
  dark:hover:text-accent-400 hover:text-accent-600 hover:transition hover:ease-in-out hover:duration-300
)`;
export const GreenBackground = tw`bg-emerald-400/25`;
export const GreenBorder = tw`border rounded-lg border-emerald-400 dark:border-emerald-700`;
export const RedBackground = tw`bg-rose-400/25`;
export const RedBorder = tw`border rounded-lg border-rose-400 dark:border-rose-700`;
export const RedText = tw`text-sm font-semibold text-rose-800 dark:text-rose-200`;
export const RedHover = tw`hover:bg-rose-500/50 dark:hover:bg-rose-300/50 hover:text-rose-700 dark:hover:text-rose-400 hover:transition hover:ease-in-out hover:duration-300`;
