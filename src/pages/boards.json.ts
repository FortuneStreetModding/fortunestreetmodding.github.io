import boards from "~/lib/getboards";

// We want to omit some properties to reduce the size of the json transferred
function omitPropertiesFromArray<T>(arr: T[], propertiesToOmit: (keyof T)[]): string {
    return JSON.stringify(arr, function(key, value) {
        // The top-level properties of the objects will have an empty string as the parent key
        if (this === arr || this instanceof Array) {
            // If the key is in the list of properties to omit, return undefined to omit it
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