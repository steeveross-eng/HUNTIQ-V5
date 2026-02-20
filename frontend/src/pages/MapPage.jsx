/**
 * MapPage - Interactive Map Page for Waypoints
 * Phase P3.2 - Interactive Map
 * Phase P4 - Background Geolocation & Proximity Alerts
 * Phase P6.4 - Real-time WebSocket Sync
 * Phase P6.5 - Support URL params for map centering (from Admin)
 * 
 * OPTIMISATION ERGONOMIQUE - Full Viewport Premium
 * - Carte centrée et full-viewport
 * - Aucun scroll vertical
 * - Panneaux flottants
 * - Responsive sur toutes résolutions
 */
import React, { useState, useCallback, useEffect, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { WaypointMap } from '../modules/territory';
import BackgroundTracker from '../components/BackgroundTracker';
import GeoSyncToggle from '../components/GeoSyncToggle';
import { toast } from 'sonner';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Map, Satellite, RefreshCw, X, Users, MapPin, Bell, BarChart3, Smartphone, ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useLanguage } from '@/contexts/LanguageContext';
import { GroupeTab } from '../modules/groupe';
import { useNavigate } from 'react-router-dom';

const MapPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [activeTab, setActiveTab] = useState('map');
  const [refreshKey, setRefreshKey] = useState(0);
  const { t } = useLanguage();
  const navigate = useNavigate();
  
  // Get URL parameters for map centering (from Admin "Voir sur la carte")
  const urlParams = useMemo(() => {
    const lat = parseFloat(searchParams.get('lat'));
    const lng = parseFloat(searchParams.get('lng'));
    const zoom = parseInt(searchParams.get('zoom')) || 15;
    
    if (!isNaN(lat) && !isNaN(lng)) {
      return { lat, lng, zoom, hasParams: true };
    }
    return { hasParams: false };
  }, [searchParams]);

  // Show notification when centered on a specific location
  useEffect(() => {
    if (urlParams.hasParams) {
      toast.info(`Carte centrée sur: ${urlParams.lat.toFixed(4)}, ${urlParams.lng.toFixed(4)}`);
    }
  }, [urlParams]);

  // Clear URL params (reset view)
  const clearUrlParams = () => {
    setSearchParams({});
  };

  const handleProximityAlert = (alert) => {
    console.log('Proximity alert received:', alert);
  };

  // Handle real-time sync events from other group members
  const handleEntityReceived = useCallback(({ action, entity, entityId, userId }) => {
    console.log('Sync event:', action, entity || entityId);
    setRefreshKey(prev => prev + 1);
  }, []);

  const handleMemberJoined = useCallback((userId) => {
    console.log('Member joined:', userId);
  }, []);

  const handleMemberLeft = useCallback((userId) => {
    console.log('Member left:', userId);
  }, []);

  // Get user info for sync
  const getUserId = () => {
    const user = localStorage.getItem('user');
    if (user) {
      try {
        const parsed = JSON.parse(user);
        return parsed.email || parsed.id || 'default_user';
      } catch (e) {
        return 'default_user';
      }
    }
    return 'default_user';
  };

  return (
    <div 
      className="fixed inset-0 bg-slate-900 flex flex-col overflow-hidden"
      style={{ paddingTop: '64px' }}
      data-testid="map-page"
    >
      {/* Header compact */}
      <div className="flex-shrink-0 bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border-b border-slate-700/50 px-4 py-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Button 
              variant="ghost" 
              size="sm" 
              onClick={() => navigate('/')} 
              className="text-gray-300 hover:text-white h-8 px-2"
            >
              <ArrowLeft className="h-4 w-4" />
            </Button>
            <div className="h-5 w-px bg-slate-700" />
            <div className="flex items-center gap-2">
              <Map className="h-5 w-5 text-[#f5a623]" />
              <div>
                <h1 className="text-sm font-bold text-white leading-tight">Carte Interactive</h1>
                <p className="text-[10px] text-slate-400 leading-tight">
                  Waypoints • GPS Tracking • Phase P3/P4/P6
                </p>
              </div>
            </div>
          </div>

          {/* Real-time Sync Toggle */}
          <GeoSyncToggle
            groupId="default_group"
            userId={getUserId()}
            onEntityReceived={handleEntityReceived}
            onMemberJoined={handleMemberJoined}
            onMemberLeft={handleMemberLeft}
          />
        </div>

        {/* URL Params Banner (when coming from Admin) */}
        {urlParams.hasParams && (
          <div className="mt-2 p-2 bg-blue-900/30 border border-blue-500/50 rounded-lg flex items-center justify-between">
            <div className="flex items-center gap-2">
              <MapPin className="h-4 w-4 text-blue-400" />
              <span className="text-blue-300 text-xs">
                Vue centrée: <strong>{urlParams.lat.toFixed(6)}, {urlParams.lng.toFixed(6)}</strong>
                <span className="text-blue-400 ml-2">(Zoom: {urlParams.zoom})</span>
              </span>
            </div>
            <Button 
              size="sm" 
              variant="ghost" 
              onClick={clearUrlParams}
              className="text-blue-400 hover:text-blue-300 h-6 px-2"
            >
              <X className="h-3 w-3 mr-1" />
              Réinitialiser
            </Button>
          </div>
        )}
      </div>

      {/* Tabs compact */}
      <div className="flex-shrink-0 bg-slate-900/95 border-b border-slate-800 px-4 py-1">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="bg-slate-800/50 h-8">
            <TabsTrigger value="map" className="data-[state=active]:bg-emerald-600 h-7 text-xs px-3" data-testid="tab-map">
              <Map className="h-3 w-3 mr-1.5" />
              Carte
            </TabsTrigger>
            <TabsTrigger value="tracking" className="data-[state=active]:bg-cyan-600 h-7 text-xs px-3" data-testid="tab-tracking">
              <Satellite className="h-3 w-3 mr-1.5" />
              GPS Tracking
            </TabsTrigger>
            <TabsTrigger value="groupe" className="data-[state=active]:bg-[var(--bionic-gold-primary)] h-7 text-xs px-3" data-testid="tab-groupe">
              <Users className="h-3 w-3 mr-1.5" />
              {t('groupe_tab_title')}
            </TabsTrigger>
          </TabsList>
        </Tabs>
      </div>

      {/* Content area - full remaining height */}
      <div className="flex-1 overflow-hidden relative">
        {/* Map Tab */}
        {activeTab === 'map' && (
          <div className="absolute inset-0">
            <WaypointMap 
              key={refreshKey}
              initialCenter={urlParams.hasParams ? [urlParams.lat, urlParams.lng] : null}
              initialZoom={urlParams.hasParams ? urlParams.zoom : null}
            />
          </div>
        )}

        {/* Tracking Tab */}
        {activeTab === 'tracking' && (
          <div className="absolute inset-0 overflow-y-auto p-4">
            <div className="max-w-5xl mx-auto">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <BackgroundTracker onProximityAlert={handleProximityAlert} />
                <div className="bg-slate-800/30 rounded-lg p-4 border border-slate-700">
                  <h3 className="text-base font-semibold text-white mb-3 flex items-center gap-2">
                    <MapPin className="h-4 w-4 text-[#f5a623]" /> Guide de Tracking
                  </h3>
                  <div className="space-y-3 text-xs text-slate-400">
                    <div className="bg-slate-700/30 rounded-lg p-3">
                      <h4 className="text-cyan-400 font-medium mb-1 flex items-center gap-2">
                        <Satellite className="h-3 w-3" /> Tracking Arrière-plan
                      </h4>
                      <p>Activez le tracking pour enregistrer automatiquement votre position toutes les 5 minutes.</p>
                    </div>
                    <div className="bg-slate-700/30 rounded-lg p-3">
                      <h4 className="text-amber-400 font-medium mb-1 flex items-center gap-2">
                        <Bell className="h-3 w-3" /> Alertes de Proximité
                      </h4>
                      <p>Notification à 500m d'un waypoint (700m pour les hotspots).</p>
                    </div>
                    <div className="bg-slate-700/30 rounded-lg p-3">
                      <h4 className="text-emerald-400 font-medium mb-1 flex items-center gap-2">
                        <BarChart3 className="h-3 w-3" /> Sessions de Chasse
                      </h4>
                      <p>Calcul automatique de la distance parcourue et positions enregistrées.</p>
                    </div>
                    <div className="bg-slate-700/30 rounded-lg p-3">
                      <h4 className="text-purple-400 font-medium mb-1 flex items-center gap-2">
                        <Smartphone className="h-3 w-3" /> Mode PWA
                      </h4>
                      <p>Installez HUNTIQ via "Ajouter à l'écran d'accueil" pour une meilleure expérience.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Groupe Tab */}
        {activeTab === 'groupe' && (
          <div className="absolute inset-0 overflow-y-auto p-4">
            <div className="max-w-5xl mx-auto">
              <GroupeTab
                groupId="default_group"
                userId={getUserId()}
                compact={false}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MapPage;
