/**
 * AnalyticsPage - Phase P3 Analytics Dashboard Page
 * BIONIC™ Global Container Applied
 * Note: Analytics est full-width pour les graphiques, seul le titre est centré
 */
import React from 'react';
import { AnalyticsDashboard } from '../modules/analytics';
import { GlobalContainer } from '../core/layouts';

const AnalyticsPage = () => {
  return (
    <div className="min-h-screen bg-slate-900">
      <GlobalContainer className="pb-12">
        <AnalyticsDashboard />
      </GlobalContainer>
    </div>
  );
};

export default AnalyticsPage;
