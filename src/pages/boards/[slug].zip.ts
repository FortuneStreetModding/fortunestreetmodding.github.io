import boards from '~/lib/getboards';
import * as path from 'path';
import { ZipArchive } from "@shortercode/webzip";

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

  const archive = new ZipArchive;

  await archive.set(`${board.path}/${board.yaml}`, board.yaml)
  await archive.compress_entry(board.yaml)
  for(const frbFile of board.frbFiles) {
    await archive.set(`${board.path}/${frbFile}.frb`, `${frbFile}.frb`);
    await archive.compress_entry(`${frbFile}.frb`)
  }
  if(board.mapIcon) {
    await archive.set(`${board.path}/${board.mapIcon}.png`, `${board.mapIcon}.png`);
    await archive.compress_entry(`${board.mapIcon}.png`)
  }

  const blob = archive.to_blob();
  return new Response(blob, {
    headers: {
      'Content-Type': 'application/zip',
      'Content-Disposition': `attachment; filename=${slug}.zip`,
    },
  });
}