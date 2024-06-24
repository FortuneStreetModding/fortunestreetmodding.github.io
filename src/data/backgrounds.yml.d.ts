import type { Music } from "./mapdescriptor";

export interface Background {
  background: string;
  mapIcon: string;
  bgm: string;
  name: string;
  download: string[];
  music: Music;
}
const content: Background[];
export default content;
