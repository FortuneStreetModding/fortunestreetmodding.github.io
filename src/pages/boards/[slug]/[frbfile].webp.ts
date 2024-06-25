import boards from '~/lib/getboards';
import fs from 'fs';

export function getStaticPaths() {
  return boards.flatMap(board => 
    board.frbFiles.map(frbfile => ({
      params: {
        slug: board.slug,
        frbfile: frbfile
      }
    }))
  );
}

export async function GET({ params } : { params: any }) {
  const slug = params.slug;
  const frbfile = params.frbfile;
  const board = boards.find(board => board.slug === slug);

  if(board === undefined) { return new Response(null, { status: 404 }); }

  const file = `.${board.path}/${frbfile}.webp`
  if(!fs.existsSync(file)) {
    return new Response(null, { status: 404 });
  }
  return new Response(fs.readFileSync(file), {
    headers: {
      'Content-Type': 'image/webp'
    },
  });
}