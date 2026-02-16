/**
 * PricingPage - V5-ULTIME Monétisation
 * =====================================
 * 
 * Page de tarification avec intégration Stripe.
 */

import React, { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { PaymentDashboard } from '@/ui/monetisation/payment';
import { useAuth } from '@/components/GlobalAuth';
import { ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';

const PricingPage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { user } = useAuth();

  // Get user ID or use session
  const userId = user?.id || localStorage.getItem('session_id') || 'guest_user';

  return (
    <main className="min-h-screen bg-background pt-20 pb-16">
      <div className="max-w-7xl mx-auto px-4">
        {/* Back Button */}
        <Button 
          variant="ghost" 
          onClick={() => navigate(-1)}
          className="mb-4 text-gray-400 hover:text-white hover:bg-gray-800/50"
          data-testid="back-button-pricing"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Retour
        </Button>

        {/* Payment Dashboard */}
        <PaymentDashboard userId={userId} />
      </div>
    </main>
  );
};

export default PricingPage;
