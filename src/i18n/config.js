import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Import translation files
import enTranslations from './locales/en.json';
import frTranslations from './locales/fr.json';
import koTranslations from './locales/ko.json';
import zhTranslations from './locales/zh.json';
import jaTranslations from './locales/ja.json';
import esTranslations from './locales/es.json';

i18n
  .use(LanguageDetector) // Detect user language
  .use(initReactI18next) // Pass i18n to React
  .init({
    resources: {
      en: { translation: enTranslations },
      fr: { translation: frTranslations },
      ko: { translation: koTranslations },
      zh: { translation: zhTranslations },
      ja: { translation: jaTranslations },
      es: { translation: esTranslations },
    },
    fallbackLng: 'en', // Default language
    detection: {
      order: ['localStorage', 'navigator'], // Check localStorage first, then browser
      caches: ['localStorage'], // Save user preference
    },
    interpolation: {
      escapeValue: false, // React already escapes
    },
  });

export default i18n;
