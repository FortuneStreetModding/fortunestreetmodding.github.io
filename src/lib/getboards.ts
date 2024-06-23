import type { MapDescriptor } from '../data/mapdescriptor';
import slug from 'slug';
import { parse } from 'path';
import { marked } from 'marked';
import DOMPurify from 'isomorphic-dompurify';
import ventureCards from "~/data/venturecards.yml";
import backgrounds, { type Background } from "~/data/backgrounds.yml";

interface MapDescriptorExtended extends MapDescriptor {
  path: string;
  slug: string;
  imageUrls: string[];
  backgroundData: Background;
  notesHtml?: string | undefined;
  changelog?: {
    version: number | string;
    added?: string[];
    changed?: string[];
    removed?: string[];
  }[];
  currentVersion?: string | number | undefined;
}

const boards = getBoards();
export default boards;


function getBoards(): MapDescriptorExtended[] {
  const boardFiles: Record<string, MapDescriptor> = import.meta.glob('/_maps/*/*.{yml,yaml}', { eager: true });
  const boards: MapDescriptorExtended[] = [];
  let defaultEasyVentureCards: number[] | undefined;
  let defaultStandardVentureCards: number[] | undefined;
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

    // render the notes
    if (board.notes !== undefined) {
      const html = marked.parse(board.notes, { async: false }) as string;
      board.notesHtml = DOMPurify.sanitize(html);
    }

    // make sure changelog is an array
    if(board.changelog !== undefined) {
      for(const change of board.changelog) {
        if(typeof change.added === 'string') {
          change.added = [change.added];
        }
        if(typeof change.changed === 'string') {
          change.changed = [change.changed];
        }
        if(typeof change.removed === 'string') {
          change.removed = [change.removed];
        }
      }
      // set current version
      board.currentVersion = board.changelog[0].version;
    }

    // set the default venture card list
    if(board.ventureCards === undefined) {
      let defaultVentureCards: number[];
      if(board.ruleSet == "Standard") {
        if(defaultStandardVentureCards === undefined) {
          defaultStandardVentureCards = new Array(128).fill(0);
          for(let i = 0; i < 128; i++) {
            if(ventureCards[i].defaultStandard) {
              defaultStandardVentureCards[i] = 1;
            }
          }
        }
        defaultVentureCards = defaultStandardVentureCards;
      } else {
        if(defaultEasyVentureCards === undefined) {
          defaultEasyVentureCards = new Array(128).fill(0);
          for(let i = 0; i < 128; i++) {
            if(ventureCards[i].defaultEasy) {
              defaultEasyVentureCards[i] = 1;
            }
          }
        }
        defaultVentureCards = defaultEasyVentureCards;
      }
      // @ts-ignore
      board.ventureCards = defaultVentureCards;
    }

    // set the background data from the backgrounds.yml
    board.backgroundData = backgrounds.find((b) => b.background === board.background) as Background;

    boards.push(board as MapDescriptorExtended);
  }
  return boards;
};
