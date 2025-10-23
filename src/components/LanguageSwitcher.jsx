import React from 'react';
import { useTranslation } from 'react-i18next';
import { motion, AnimatePresence } from 'framer-motion';

const LanguageSwitcher = () => {
  const { i18n, t } = useTranslation();
  const [isOpen, setIsOpen] = React.useState(false);

  const languages = [
    { code: 'en', name: t('languages.en'), flag: '🇺🇸' },
    { code: 'fr', name: t('languages.fr'), flag: '🇫🇷' },
    { code: 'ko', name: t('languages.ko'), flag: '🇰🇷' },
    { code: 'zh', name: t('languages.zh'), flag: '🇨🇳' },
    { code: 'ja', name: t('languages.ja'), flag: '🇯🇵' },
    { code: 'es', name: t('languages.es'), flag: '🇪🇸' },
  ];

  const currentLanguage = languages.find(lang => lang.code === i18n.language) || languages[0];

  const changeLanguage = (langCode) => {
    i18n.changeLanguage(langCode);
    setIsOpen(false);
  };

  return (
    <div className="fixed top-4 right-4 z-50">
      <motion.button
        onClick={() => setIsOpen(!isOpen)}
        className="bg-white/90 backdrop-blur-sm hover:bg-white text-gray-800 font-fredoka font-bold px-4 py-2 rounded-full shadow-lg flex items-center gap-2 transition-all"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <span className="text-2xl">{currentLanguage.flag}</span>
        <span className="hidden sm:inline">{currentLanguage.name}</span>
        <svg 
          className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </motion.button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
            className="absolute top-14 right-0 bg-white rounded-2xl shadow-2xl overflow-hidden min-w-[200px]"
          >
            {languages.map((lang) => (
              <motion.button
                key={lang.code}
                onClick={() => changeLanguage(lang.code)}
                className={`w-full px-4 py-3 flex items-center gap-3 hover:bg-purple-50 transition-colors ${
                  i18n.language === lang.code ? 'bg-purple-100 font-bold' : ''
                }`}
                whileHover={{ x: 5 }}
              >
                <span className="text-2xl">{lang.flag}</span>
                <span className="font-fredoka">{lang.name}</span>
                {i18n.language === lang.code && (
                  <span className="ml-auto text-purple-600">✓</span>
                )}
              </motion.button>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default LanguageSwitcher;
