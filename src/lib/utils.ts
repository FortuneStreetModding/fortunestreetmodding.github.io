import path from "path";
import { exec } from 'child_process';

export function getPathnameWithoutExtension(url: URL) {
  const parsedPath = path.parse(url.pathname);
  return path.join(parsedPath.dir, parsedPath.name);
}

export async function run(command: string): Promise<string> {
  return new Promise((resolve, reject) => {
    exec(command, (error, stdout, stderr) => {
      if (error) {
        reject(`Error: ${error.message}`);
      } else if (stderr) {
        reject(`Stderr: ${stderr}`);
      } else {
        resolve(stdout);
      }
    });
  });
}
