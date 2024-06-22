import type { MapDescriptor } from './mapdescriptor';
import slug from 'slug';
import { parse } from 'path';

interface MapDescriptorExtended extends MapDescriptor {
  path: string;
  slug: string;
  imageUrls: string[];
}

const boards = getBoards();
export default boards;

function getBoards(): MapDescriptorExtended[] {
  const boardFiles: Record<string, MapDescriptor> = import.meta.glob('/_maps/*/*.{yml,yaml}', { eager: true });
  const boards: MapDescriptorExtended[] = [];
  for (const [path, boardConst] of Object.entries(boardFiles)) {
    const board = structuredClone(boardConst)
    // some post processing...

    // merge frbFile1,2,3,4 into frbFiles
    if(!board.frbFiles) {
      const frbFiles: string[] = [];
      if(board.frbFile2 !== undefined) {
        frbFiles.push(board.frbFile2);
      }
      if(board.frbFile3 !== undefined) {
        frbFiles.push(board.frbFile3);
      }
      if(board.frbFile4 !== undefined) {
        frbFiles.push(board.frbFile4);
      }
      board.frbFiles = [board.frbFile1!, ...frbFiles];
    }
    const parsedPath = parse(path)

    // set the directory path for the board
    board.path = parsedPath.dir;

    // set the slug name for the board
    board.slug = slug(parsedPath.name);

    // set the image urls for each frb file
    board.imageUrls = board.frbFiles!.map((frbFile: string) => `${parsedPath.dir}/${frbFile}.webp`);

    boards.push(board as MapDescriptorExtended);
  }
  return boards;
};
