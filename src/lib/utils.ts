import path from "path";

export function getPathnameWithoutExtension(url: URL) {
  const parsedPath = path.parse(url.pathname);
  return path.join(parsedPath.dir, parsedPath.name);
}