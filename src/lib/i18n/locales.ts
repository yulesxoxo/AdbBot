// Add Locale here
export enum SupportedLocale {
  EN = "en",
}

export function getLocaleOrDefault(value: string): SupportedLocale {
  return Object.values(SupportedLocale).includes(value as SupportedLocale)
    ? (value as SupportedLocale)
    : SupportedLocale.EN;
}

const locales: LocaleDictionary = {
  [SupportedLocale.EN]: {}, // English uses default keys
};

type Translations = Record<string, string>;
type LocaleDictionary = Record<SupportedLocale, Translations>;
export default locales;
export type { Translations, LocaleDictionary };
