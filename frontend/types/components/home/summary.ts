export type GraphSummary = {
  is_empty: boolean
  classes: number,
  functions: number,
  modules: number,
  packages: number
}

export type StatsCardProps = {
  title: string
  value: number
}