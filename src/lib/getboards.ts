import type { MapDescriptor, MapDescriptor1 } from '../data/mapdescriptor';
import slug from 'slug';
import { parse } from 'path';
import { marked } from 'marked';
import DOMPurify from 'isomorphic-dompurify';
import ventureCards from "~/data/venturecards.yml";
import backgrounds, { type Background } from "~/data/backgrounds.yml";
import { execSync } from 'child_process';
import { getRandomDate } from './utils';

export type MapDescriptorExtended = Omit<MapDescriptor1, 'music' | 'changelog' | 'frbFile1' | 'frbFile2' | 'frbFile3' | 'frbFile4' | 'frbFiles'> & {
  nameEn: string;
  descEn: string;
  path: string;
  yaml: string;
  slug: string;
  imageUrls: string[];
  backgroundData: Background;
  frbFiles: string[];
  uploadDate: number;
  lastUpdated: number;
  notesHtml?: string;
  changelog?: {
    version: number | string;
    added?: string[];
    changed?: string[];
    removed?: string[];
  }[];
  currentVersion?: string | number;
  music?: Omit<MapDescriptor, 'music'> & {
    download: string[] | null;
  };
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
    board.default = undefined
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
      board.frbFile1 = undefined;
      board.frbFile2 = undefined;
      board.frbFile3 = undefined;
      board.frbFile4 = undefined;
    }
    const parsedPath = parse(path)

    // set the name and desc for the board
    board.nameEn = board.name.en;
    board.descEn = board.desc.en

    // set the directory path for the board
    board.path = parsedPath.dir;

    // set the name of the yaml file
    board.yaml = parsedPath.base;

    // set the slug name for the board
    board.slug = slug(parsedPath.name);

    // set the background data from the backgrounds.yml
    board.backgroundData = backgrounds.find((b) => b.background === board.background) as Background;

    // set the image urls for each frb file
    board.imageUrls = board.frbFiles!.map((frbFile: string) => `/boards/${board.slug}/${frbFile}.webp`);

    // render the notes
    if (board.notes !== undefined) {
      const html = marked.parse(board.notes, { async: false }) as string;
      board.notesHtml = DOMPurify.sanitize(html);
    }

    // make sure changelog is an array
    if(board.changelog !== undefined) {
      for(let i = 0; i < board.changelog.length; i++) {
        let change = board.changelog[i];
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

    // make sure music download is an array
    if(board.musicDownload !== undefined) {
      if(typeof board.musicDownload === 'string') {
        board.musicDownload = [board.musicDownload];
      }
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
      board.ventureCards = defaultVentureCards as any;
    }

    // find out the board upload date and last updated date
    if(import.meta.env.DEV) {
      // it takes way too long in dev mode to calculate, so we just set it to a random date
      board.lastUpdated = getRandomDate().getTime();
      board.uploadDate = getRandomDate().getTime();
    } else {
      // get upload date
      try {
        const command = `git log --follow --format=%at -- ".${path}"`
        const output = execSync(command, { encoding: 'utf-8' });
        const dates = output.trim().split('\n');
        board.uploadDate = (+dates[dates.length - 1])*1000;
      } catch (error) {
        console.error('Error:', error);
      }
      // get last updated date
      try {
        const frbPaths = board.frbFiles!.map((frbFile: string) => `"./_maps/${board.slug}/${frbFile}.frb"`);
        const command = `git log --format=%at-%H-%s --fixed-strings --grep='[skip]' --grep='Merge' --invert-grep --max-count=1 -- ".${path}" ${frbPaths.join(' ')}`
        const output = execSync(command, { encoding: 'utf-8' });
        const dates = output.trim().split('\n');
        board.lastUpdated = (+dates[0])*1000;
      } catch (error) {
        console.error('Error:', error);
      }
    }

    boards.push(board as any);
  }
  return boards;
};
