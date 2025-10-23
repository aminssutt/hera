import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import AnimatedBackground from '../components/AnimatedBackground';

const Contact = () => {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    rating: '',
    easeOfUse: '',
    quality: '',
    wouldRecommend: '',
    additionalComments: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitStatus(null);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/contact-feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        setSubmitStatus('success');
        // Reset form after 2 seconds
        setTimeout(() => {
          setFormData({
            firstName: '',
            lastName: '',
            email: '',
            rating: '',
            easeOfUse: '',
            quality: '',
            wouldRecommend: '',
            additionalComments: ''
          });
          setSubmitStatus(null);
        }, 3000);
      } else {
        setSubmitStatus('error');
      }
    } catch (error) {
      console.error('Error submitting feedback:', error);
      setSubmitStatus('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 relative overflow-hidden">
      <AnimatedBackground />
      
      <div className="relative z-10 container mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <button
            onClick={() => navigate('/')}
            className="inline-flex items-center gap-2 text-purple-600 hover:text-purple-700 mb-6 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            {t('contact.backToHome')}
          </button>
          
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-purple-600 via-pink-500 to-blue-500 text-transparent bg-clip-text">
            {t('contact.title')}
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            {t('contact.subtitle')}
          </p>
        </div>

        {/* Contact Form */}
        <div className="max-w-3xl mx-auto">
          <div className="bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl p-8 md:p-12">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Personal Info */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    {t('contact.firstName')} {t('contact.required')}
                  </label>
                  <input
                    type="text"
                    name="firstName"
                    value={formData.firstName}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition-colors"
                    placeholder="John"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    {t('contact.lastName')} {t('contact.required')}
                  </label>
                  <input
                    type="text"
                    name="lastName"
                    value={formData.lastName}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition-colors"
                    placeholder="Doe"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  {t('contact.email')} {t('contact.required')}
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition-colors"
                  placeholder="john.doe@example.com"
                />
              </div>

              {/* Rating Questions */}
              <div className="space-y-6 pt-6 border-t-2 border-gray-100">
                <h3 className="text-xl font-bold text-gray-800 mb-4">{t('contact.quickSurvey')}</h3>
                
                {/* Overall Rating */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-3">
                    {t('contact.overallRating')} {t('contact.required')}
                  </label>
                  <div className="flex gap-2">
                    {[1, 2, 3, 4, 5].map((num) => (
                      <button
                        key={num}
                        type="button"
                        onClick={() => setFormData({...formData, rating: num.toString()})}
                        className={`flex-1 py-3 rounded-xl font-semibold transition-all ${
                          formData.rating === num.toString()
                            ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg scale-105'
                            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                        }`}
                      >
                        {num === 1 ? '😞' : num === 2 ? '😐' : num === 3 ? '🙂' : num === 4 ? '😊' : '🤩'}
                        <br />
                        <span className="text-xs">{num}</span>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Ease of Use */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    {t('contact.easeOfUse')} {t('contact.required')}
                  </label>
                  <select
                    name="easeOfUse"
                    value={formData.easeOfUse}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition-colors"
                  >
                    <option value="">{t('contact.selectOption')}</option>
                    <option value="very-easy">{t('contact.veryEasy')}</option>
                    <option value="easy">{t('contact.easy')}</option>
                    <option value="neutral">{t('contact.neutral')}</option>
                    <option value="difficult">{t('contact.difficult')}</option>
                    <option value="very-difficult">{t('contact.veryDifficult')}</option>
                  </select>
                </div>

                {/* Quality */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    {t('contact.qualityRating')} {t('contact.required')}
                  </label>
                  <select
                    name="quality"
                    value={formData.quality}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition-colors"
                  >
                    <option value="">{t('contact.selectOption')}</option>
                    <option value="excellent">{t('contact.excellent')}</option>
                    <option value="good">{t('contact.good')}</option>
                    <option value="average">{t('contact.average')}</option>
                    <option value="poor">{t('contact.poor')}</option>
                    <option value="very-poor">{t('contact.veryPoor')}</option>
                  </select>
                </div>

                {/* Recommendation */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    {t('contact.recommend')} {t('contact.required')}
                  </label>
                  <select
                    name="wouldRecommend"
                    value={formData.wouldRecommend}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition-colors"
                  >
                    <option value="">{t('contact.selectOption')}</option>
                    <option value="definitely">{t('contact.definitely')}</option>
                    <option value="probably">{t('contact.probably')}</option>
                    <option value="maybe">{t('contact.maybe')}</option>
                    <option value="probably-not">{t('contact.probablyNot')}</option>
                    <option value="definitely-not">{t('contact.definitelyNot')}</option>
                  </select>
                </div>
              </div>

              {/* Additional Comments */}
              <div className="pt-6 border-t-2 border-gray-100">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  {t('contact.additionalComments')}
                </label>
                <textarea
                  name="additionalComments"
                  value={formData.additionalComments}
                  onChange={handleChange}
                  rows={5}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition-colors resize-none"
                  placeholder={t('contact.commentsPlaceholder')}
                />
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isSubmitting}
                className={`w-full py-4 rounded-xl font-bold text-lg transition-all transform ${
                  isSubmitting
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 hover:shadow-2xl hover:scale-105 text-white'
                }`}
              >
                {isSubmitting ? (
                  <span className="flex items-center justify-center gap-2">
                    <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    {t('contact.sending')}
                  </span>
                ) : (
                  t('contact.sendFeedback')
                )}
              </button>

              {/* Status Messages */}
              {submitStatus === 'success' && (
                <div className="p-4 bg-green-50 border-2 border-green-200 rounded-xl text-green-800 text-center">
                  {t('contact.successMessage')}
                </div>
              )}
              
              {submitStatus === 'error' && (
                <div className="p-4 bg-red-50 border-2 border-red-200 rounded-xl text-red-800 text-center">
                  {t('contact.errorMessage')}
                </div>
              )}
            </form>
          </div>
        </div>

        {/* Footer Note */}
        <p className="text-center text-gray-500 mt-8 text-sm">
          {t('contact.footerNote')}
        </p>
      </div>
    </div>
  );
};

export default Contact;
