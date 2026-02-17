/**
 * ForecastPage - Success Forecast & WQS Dashboard
 * Phase P3 - Waypoint Scoring
 * BIONIC™ Global Container Applied
 */
import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { SuccessForecast } from '../components/SuccessForecast';
import { Target } from 'lucide-react';
import { GlobalContainer } from '../core/layouts';

const ForecastPage = () => {
  const { t } = useLanguage();
  
  return (
    <div className="min-h-screen bg-slate-900">
      <GlobalContainer maxWidth="1200px" className="pb-12">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Target className="h-7 w-7 text-[#f5a623]" />
            {t('forecast_title')}
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Waypoint Quality Score (WQS) • Phase P3
          </p>
        </div>
        <SuccessForecast />
      </GlobalContainer>
    </div>
  );
};

export default ForecastPage;
