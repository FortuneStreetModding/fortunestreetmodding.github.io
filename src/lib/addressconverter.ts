interface Section {
  off_beg: number;
  off_end: number;
  delta: number;
}

export class AddressSectionMapper {
  private sections: Section[];

  constructor(sections: Section[]) {
    this.sections = sections;
  }

  private sectionContainsAddress(section: Section, address: number): boolean {
    return section.off_beg <= address && address <= section.off_end;
  }

  public map(address: number): number | null {
    for (let section of this.sections) {
      if (this.sectionContainsAddress(section, address)) {
        return address - section.delta;
      }
    }
    return null;
  }

  public inverseMap(address: number): number | null {
    for (let section of this.sections) {
      const mappedAddress = address + section.delta;
      if (this.sectionContainsAddress(section, mappedAddress)) {
        return mappedAddress;
      }
    }
    return null;
  }
}

// Fortune Street Virtual to Fortune Street File
export const fsvirt_to_fsfile = new AddressSectionMapper([
  { off_beg: 0x80004000, off_end: 0x80006720, delta: 0x80003f00 },
  { off_beg: 0x80006720, off_end: 0x80006c80, delta: 0x7fbfda40 },
  { off_beg: 0x80006c80, off_end: 0x80007480, delta: 0x7fbfda40 },
  { off_beg: 0x80007480, off_end: 0x8040d940, delta: 0x80004c60 },
  { off_beg: 0x8040d940, off_end: 0x8040de80, delta: 0x80003f00 },
  { off_beg: 0x8040de80, off_end: 0x8040dea0, delta: 0x80003f00 },
  { off_beg: 0x8040dec0, off_end: 0x8044ea60, delta: 0x80003f20 },
  { off_beg: 0x8044ea60, off_end: 0x804ac680, delta: 0x80003f20 },
  { off_beg: 0x80814a80, off_end: 0x808171c0, delta: 0x8036c320 },
  { off_beg: 0x80818da0, off_end: 0x8081ede0, delta: 0x8036df00 },
]);

// Boom Street Virtual to Boom Street File
export const bsvirt_to_bsfile = new AddressSectionMapper([
  { off_beg: 0x80004000, off_end: 0x80006720, delta: 0x80003f00 },
  { off_beg: 0x80006720, off_end: 0x80006c80, delta: 0x7fbfda00 },
  { off_beg: 0x80006c80, off_end: 0x80007480, delta: 0x7fbfda00 },
  { off_beg: 0x80007480, off_end: 0x8040d980, delta: 0x80004c60 },
  { off_beg: 0x8040d980, off_end: 0x8040dec0, delta: 0x80003f00 },
  { off_beg: 0x8040dec0, off_end: 0x8040dee0, delta: 0x80003f00 },
  { off_beg: 0x8040df00, off_end: 0x8044ec00, delta: 0x80003f20 },
  { off_beg: 0x8044ec00, off_end: 0x804ac820, delta: 0x80003f20 },
  { off_beg: 0x80814c80, off_end: 0x808173c0, delta: 0x8036c380 },
  { off_beg: 0x80818fa0, off_end: 0x8081efe0, delta: 0x8036df60 },
]);

// Boom Street Virtual to Fortune Street Virtual
export const bsvirt_to_fsvirt = new AddressSectionMapper([
  { off_beg: 0x80000100, off_end: 0x8007a283, delta: 0x0 },
  { off_beg: 0x8007a2f4, off_end: 0x80268717, delta: 0x54 },
  { off_beg: 0x80268720, off_end: 0x8040d97b, delta: 0x50 },
  { off_beg: 0x8040d980, off_end: 0x8041027f, delta: 0x40 },
  { off_beg: 0x804105f0, off_end: 0x8044ebe7, delta: 0x188 },
  { off_beg: 0x8044ec00, off_end: 0x804ac804, delta: 0x1a0 },
  { off_beg: 0x804ac880, off_end: 0x8081f013, delta: 0x200 },
]);

// Boom Street Virtual to Itadaki Street Wii Virtual
export const bsvirt_to_isvirt = new AddressSectionMapper([
  { off_beg: 0x80000100, off_end: 0x8007a283, delta: 0x0 },
  { off_beg: 0x8007a2f4, off_end: 0x80268717, delta: 0x94 },
  { off_beg: 0x8026871f, off_end: 0x8040d97b, delta: 0x90 },
  { off_beg: 0x8040d97f, off_end: 0x80410278, delta: 0x80 },
  { off_beg: 0x80410578, off_end: 0x8044ebe3, delta: 0x2a8 },
  { off_beg: 0x8044ebff, off_end: 0x804ac804, delta: 0x2c0 },
  { off_beg: 0x804ac880, off_end: 0x8081f013, delta: 0x300 },
]);

// Itadaki Street Wii Virtual to Itadaki Street Wii File
export const isvirt_to_isfile = new AddressSectionMapper([
  { off_beg: 0x80004000, off_end: 0x80006720, delta: 0x80003f00 },
  { off_beg: 0x80006720, off_end: 0x80006c80, delta: 0x7fbfda80 },
  { off_beg: 0x80006c80, off_end: 0x80007480, delta: 0x7fbfda80 },
  { off_beg: 0x80007480, off_end: 0x8040d900, delta: 0x80004c60 },
  { off_beg: 0x8040d900, off_end: 0x8040de40, delta: 0x80003f00 },
  { off_beg: 0x8040de40, off_end: 0x8040de60, delta: 0x80003f00 },
  { off_beg: 0x8040de80, off_end: 0x8044e940, delta: 0x80003f20 },
  { off_beg: 0x8044e940, off_end: 0x804ac560, delta: 0x80003f20 },
  { off_beg: 0x80814980, off_end: 0x808170c0, delta: 0x8036c340 },
  { off_beg: 0x80818ca0, off_end: 0x8081ece0, delta: 0x8036df20 },
]);
