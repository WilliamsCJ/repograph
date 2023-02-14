
export async function postNewGraph(
  name: string,
  description: string,
  files: File[]
): Promise<void> {
  const url = new URL(
  `${process.env.NEXT_PUBLIC_BACKEND_URL}/graph/build`
  );

  let formData = new FormData();
  formData.append('name', name);
  formData.append('description', description);
  for (let file of files) {
    formData.append('files', file)
  }

  const res = await fetch(url, {
    body: formData,
    method: 'POST',
  });
  if (!res.ok) {
    throw new Error("An error occurred!");
  }

  return (await res.json());
}