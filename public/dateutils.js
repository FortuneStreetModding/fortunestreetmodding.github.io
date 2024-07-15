const UNIT_DAY = 24 * 60 * 60 * 1000;
const UNIT_WEEK = 7 * UNIT_DAY;
const UNIT_MONTH = 30 * UNIT_DAY;

/**
 * Calculates the difference between the target date and today in the specified unit.
 *
 * @param {Date} targetDate - The date to compare with today.
 * @param {number} unit - The unit to use for the difference calculation (e.g., milliseconds per day).
 * @returns {number} The difference in the specified unit.
 */
function ago(targetDate, unit) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  targetDate.setHours(0, 0, 0, 0);
  const differenceMs = today.getTime() - targetDate.getTime();
  const differenceDays = Math.floor(differenceMs / unit);
  return differenceDays;
}

/**
 * Calculates the number of days between the target date and today.
 *
 * @param {Date} targetDate - The date to compare with today.
 * @returns {number} The number of days between the target date and today.
 */
function daysAgo(targetDate) {
  return ago(targetDate, UNIT_DAY);
}

/**
 * Calculates the number of weeks between the target date and today.
 *
 * @param {Date} targetDate - The date to compare with today.
 * @returns {number} The number of weeks between the target date and today.
 */
function weeksAgo(targetDate) {
  return ago(targetDate, UNIT_WEEK);
}

/**
 * Calculates the number of months between the target date and today.
 *
 * @param {Date} targetDate - The date to compare with today.
 * @returns {number} The number of months between the target date and today.
 */
function monthsAgo(targetDate) {
  return ago(targetDate, UNIT_MONTH);
}

/**
 * Converts the target date into a human-readable string representing the time difference from today.
 *
 * @param {Date} targetDate - The date to convert.
 * @returns {string} A human-readable string representing the time difference from today.
 */
function humanReadableDate(targetDate) {
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

/**
 * Converts a Date object to an ISO 8601 formatted date string (YYYY-MM-DD).
 *
 * @param {Date} date - The date to be converted.
 * @returns {string} The ISO 8601 formatted date string.
 */
function isoDate(date) {
  return date.toISOString().split('T')[0];
}