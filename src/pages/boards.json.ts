import boards from "~/lib/getboards";

// We want to omit some properties to reduce the size of the json transferred
function omitPropertiesFromArray<T>(arr: T[], propertiesToOmit: (keyof T)[]): string {
    return JSON.stringify(arr, function(key, value) {
        // check if we are on top-level
        if (Object.keys(this).includes("frbFiles") && Object.keys(this).includes("targetAmount")) {
            if (propertiesToOmit.includes(key as keyof T)) {
                return undefined;
            }
        }
        return value;
    });
}

// Outputs: /boards.json
export async function GET() {
  return new Response(
    JSON.stringify(omitPropertiesFromArray(boards, [
      "ventureCards", "music", "notes", "notesHtml", "name", "desc", "changelog", "districtNames", "shopNames"
    ]))
  )
}