/**
 * AdminPremiumPage - V5-ULTIME Administration Premium
 * ====================================================
 * 
 * Page principale d'administration avec navigation intégrée.
 * Thème: Dark Premium avec accents or/bronze.
 * Accès: Admin uniquement.
 */

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { 
  Crown, ArrowLeft, LayoutDashboard, CreditCard, Layers, 
  Zap, Target, BookOpen, Settings, BarChart3, Users, 
  FileText, Shield
} from 'lucide-react';

// Import all admin modules
import {
  AdminDashboard,
  AdminPayments,
  AdminFreemium,
  AdminUpsell,
  AdminOnboarding,
  AdminTutorials,
  AdminRules,
  AdminStrategy,
  AdminUsers,
  AdminLogs,
  AdminSettings
} from '@/ui/administration';

const navItems = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'payments', label: 'Paiements', icon: CreditCard },
  { id: 'freemium', label: 'Freemium', icon: Layers },
  { id: 'upsell', label: 'Upsell', icon: Zap },
  { id: 'onboarding', label: 'Onboarding', icon: Target },
  { id: 'tutorials', label: 'Tutoriels', icon: BookOpen },
  { id: 'rules', label: 'Règles', icon: Settings },
  { id: 'strategy', label: 'Stratégies', icon: BarChart3 },
  { id: 'users', label: 'Utilisateurs', icon: Users },
  { id: 'logs', label: 'Logs', icon: FileText },
  { id: 'settings', label: 'Paramètres', icon: Shield },
];

const AdminPremiumPage = () => {
  const navigate = useNavigate();
  const [activeSection, setActiveSection] = useState('dashboard');

  const renderContent = () => {
    switch (activeSection) {
      case 'dashboard': return <AdminDashboard onNavigate={setActiveSection} />;
      case 'payments': return <AdminPayments />;
      case 'freemium': return <AdminFreemium />;
      case 'upsell': return <AdminUpsell />;
      case 'onboarding': return <AdminOnboarding />;
      case 'tutorials': return <AdminTutorials />;
      case 'rules': return <AdminRules />;
      case 'strategy': return <AdminStrategy />;
      case 'users': return <AdminUsers />;
      case 'logs': return <AdminLogs />;
      case 'settings': return <AdminSettings />;
      default: return <AdminDashboard onNavigate={setActiveSection} />;
    }
  };

  return (
    <main 
      data-testid="admin-premium-page" 
      className="min-h-screen bg-[#050510] pt-20"
    >
      <div className="flex">
        {/* Sidebar */}
        <aside className="fixed left-0 top-16 h-[calc(100vh-4rem)] w-64 bg-[#0a0a15] border-r border-[#F5A623]/10 p-4 overflow-y-auto">
          {/* Logo */}
          <div className="flex items-center gap-3 mb-6 p-3 bg-gradient-to-r from-[#F5A623]/20 to-transparent rounded-lg">
            <Crown className="h-8 w-8 text-[#F5A623]" />
            <div>
              <h1 className="text-white font-bold">Admin Premium</h1>
              <p className="text-gray-500 text-xs">V5-ULTIME</p>
            </div>
          </div>

          {/* Back Button */}
          <Button
            variant="ghost"
            onClick={() => navigate('/')}
            className="w-full justify-start text-gray-400 hover:text-white hover:bg-white/5 mb-4"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Retour à l'app
          </Button>

          {/* Navigation */}
          <nav className="space-y-1">
            {navItems.map((item) => (
              <Button
                key={item.id}
                data-testid={`sidebar-${item.id}`}
                variant="ghost"
                onClick={() => setActiveSection(item.id)}
                className={`
                  w-full justify-start transition-all
                  ${activeSection === item.id 
                    ? 'bg-[#F5A623]/10 text-[#F5A623] border-l-2 border-[#F5A623]' 
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                  }
                `}
              >
                <item.icon className="h-4 w-4 mr-3" />
                {item.label}
              </Button>
            ))}
          </nav>
        </aside>

        {/* Main Content */}
        <div className="ml-64 flex-1 p-8">
          {renderContent()}
        </div>
      </div>
    </main>
  );
};

export default AdminPremiumPage;
