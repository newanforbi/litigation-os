// Intl formatter construction is expensive — roughly 70x the cost of a format()
// call on an existing instance — and these run per cell across the damages,
// census and cost-of-counsel tables. Instances are cached by their options so a
// table render constructs at most one of each.

const currencyFormatters = new Map<number, Intl.NumberFormat>();
const dateFormatters = new Map<string, Intl.DateTimeFormat>();

export const formatCurrency = (value: number, maximumFractionDigits = 0) => {
  let formatter = currencyFormatters.get(maximumFractionDigits);
  if (!formatter) {
    formatter = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits });
    currencyFormatters.set(maximumFractionDigits, formatter);
  }
  return formatter.format(value);
};

const numberFormatter = new Intl.NumberFormat("en-US");
export const formatNumber = (value: number) => numberFormatter.format(value);

const DEFAULT_DATE_OPTIONS: Intl.DateTimeFormatOptions = { year: "numeric", month: "short", day: "numeric" };

export const formatDate = (value: string | Date, options: Intl.DateTimeFormatOptions = DEFAULT_DATE_OPTIONS) => {
  const key = JSON.stringify(options);
  let formatter = dateFormatters.get(key);
  if (!formatter) {
    formatter = new Intl.DateTimeFormat("en-US", options);
    dateFormatters.set(key, formatter);
  }
  return formatter.format(value instanceof Date ? value : new Date(value));
};

export const formatMatterPath = (matterNumber: number) => `/matters/${matterNumber}`;

// Matter cards show the short plaintiff name. Stored captions keep the full
// "Brendan Ngwa Nforbi v." form; only the card heading is shortened.
const FULL_PLAINTIFF_PREFIX = /^Brendan Ngwa Nforbi v\. /;
export const formatCardCaption = (caption: string) => caption.replace(FULL_PLAINTIFF_PREFIX, "Ngwa Nforbi v. ");
