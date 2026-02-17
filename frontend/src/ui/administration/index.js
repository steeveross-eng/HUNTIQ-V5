/**
 * Administration Module - V5-ULTIME Premium
 * ==========================================
 * 
 * Point d'entrée du module d'administration premium.
 * Phase 1 Migration: E-Commerce intégré
 * Phase 2 Migration: Content & Backup intégrés
 * Phase 3 Migration: Maintenance & Contacts intégrés
 * Phase 4 Migration: Hotspots & Networking intégrés
 */

export { default as AdminService } from './AdminService';
export { AdminDashboard } from './admin_dashboard';
export { AdminPayments } from './admin_payments';
export { AdminFreemium } from './admin_freemium';
export { AdminUpsell } from './admin_upsell';
export { AdminOnboarding } from './admin_onboarding';
export { AdminTutorials } from './admin_tutorials';
export { AdminRules } from './admin_rules';
export { AdminStrategy } from './admin_strategy';
export { AdminUsers } from './admin_users';
export { AdminLogs } from './admin_logs';
export { AdminSettings } from './admin_settings';
// Phase 1 Migration - E-Commerce
export { AdminEcommerce } from './admin_ecommerce';
// Phase 2 Migration - Content & Backup
export { AdminContent } from './admin_content';
export { AdminBackup } from './admin_backup';
// Phase 3 Migration - Maintenance & Contacts
export { AdminMaintenance } from './admin_maintenance';
export { AdminContacts } from './admin_contacts';
// Phase 4 Migration - Hotspots & Networking
export { AdminHotspots } from './admin_hotspots';
export { AdminNetworking } from './admin_networking';
// Phase 5 Migration - Email & Marketing
export { AdminEmail } from './admin_email';
export { AdminMarketing } from './admin_marketing';
// Phase 6 Migration - Partners & Branding
export { AdminPartners } from './admin_partners';
export { AdminBranding } from './admin_branding';
