import boards from '~/lib/getboards';
import JSZip from 'jszip';
import fs from 'fs';
import { vanillaMapIcons } from '~/lib/vanilla';

export function getStaticPaths() {
  return boards.map(board => {
    return {
      params: {
        slug: board.slug
      }
    }
  })
}

export async function GET({ params } : { params: any }) {
  const slug = params.slug;
  const board = boards.find(board => board.slug === slug);

  if(board === undefined) { return new Response(null, { status: 404 }); }

  const zip = new JSZip();

  // yaml file
  let file = `.${board.path}/${board.yaml}`
  if(!fs.existsSync(file)) {
    throw new Error(`File not found: ${file}`);
  }
  zip.file(board.yaml, fs.createReadStream(file));

  // frb files
  for(const frbName of board.frbFiles) {
    file = `.${board.path}/${frbName}.frb`
    if(!fs.existsSync(file)) {
      throw new Error(`File not found: ${file}`);
    }
    zip.file(`${frbName}.frb`, fs.createReadStream(file));
  }

  // map icon file
  if(board.mapIcon && !vanillaMapIcons.includes(board.mapIcon)) {
    file = `.${board.path}/${board.mapIcon}.png`
    if(fs.existsSync(file)) {
      zip.file(`${board.mapIcon}.png`, fs.createReadStream(file));
    } else {
      console.warn(`File not found: ${file}`);
    }
  }

  const buffer = zip.generateInternalStream({
    type: "blob",
    compression: "DEFLATE",
    compressionOptions: {
        level: 9
    }
  });
  const blob = await buffer.accumulate();
  return new Response(blob, {
    headers: {
      'Content-Type': 'application/zip',
      'Content-Disposition': `attachment; filename=${slug}.zip`,
    },
  });
}