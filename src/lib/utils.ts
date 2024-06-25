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


export function getRandomDate() {
  // Get today's date
  const today = new Date();

  // Calculate 1 year ago from today
  const oneYearAgo = new Date();
  oneYearAgo.setFullYear(today.getFullYear() - 1);

  // Get a random number of milliseconds between oneYearAgo and today
  const randomMilliseconds = Math.floor(Math.random() * (today.getTime() - oneYearAgo.getTime())) + oneYearAgo.getTime();

  // Create a new Date object using the random milliseconds
  const randomDate = new Date(randomMilliseconds);

  return randomDate;
}

export function daysAgo(targetDate: Date): number {
  // Get today's date
  const today = new Date();

  // Calculate the difference in milliseconds
  const differenceMs = today.getTime() - targetDate.getTime();

  // Convert milliseconds to days
  const differenceDays = Math.floor(differenceMs / (1000 * 60 * 60 * 24));

  return differenceDays;
}

export function weeksAgo(targetDate: Date): number {
  // Get today's date
  const today = new Date();

  // Calculate the difference in milliseconds
  const differenceMs = today.getTime() - targetDate.getTime();

  // Convert milliseconds to weeks
  const differenceDays = Math.floor(differenceMs / (1000 * 60 * 60 * 24 * 7));

  return differenceDays;
}

export function monthsAgo(targetDate: Date): number {
  // Get today's date
  const today = new Date();

  // Calculate the difference in milliseconds
  const differenceMs = today.getTime() - targetDate.getTime();

  // Convert milliseconds to months
  const differenceDays = Math.floor(differenceMs / (1000 * 60 * 60 * 24 * 30));

  return differenceDays;
}

export function humanReadableDate(targetDate: Date): string {
  if (daysAgo(targetDate)<1) {
    return `today`;
  } if (daysAgo(targetDate)<2) {
    return `yesterday`;
  } else if (daysAgo(targetDate)<30) {
    return `${daysAgo(targetDate)} days ago`;
  } else if (weeksAgo(targetDate)<10) {
    return `${weeksAgo(targetDate)} weeks ago`;
  } else if (monthsAgo(targetDate)<10) {
    return `${monthsAgo(targetDate)} months ago`;
  } else {
    return targetDate.toISOString().split('T')[0];
  }
}

export function isoDate(date: Date): string {
  return date.toISOString().split('T')[0];
}