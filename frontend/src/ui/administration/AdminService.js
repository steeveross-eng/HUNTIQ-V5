/**
 * AdminService - V5-ULTIME Administration Premium
 * ================================================
 * 
 * Service centralisé pour les appels API d'administration.
 */

const API_BASE = process.env.REACT_APP_BACKEND_URL;

export const AdminService = {
  // ============ DASHBOARD ============
  async getDashboard() {
    try {
      const response = await fetch(`${API_BASE}/api/v1/admin/dashboard`);
      if (!response.ok) throw new Error('Failed to fetch dashboard');
      return await response.json();
    } catch (error) {
      console.error('AdminService.getDashboard error:', error);
      return { success: false, error: error.message };
    }
  },

  // ============ PAYMENTS ============
  async getTransactions(limit = 50, status = null, skip = 0) {
    const params = new URLSearchParams({ limit, skip });
    if (status) params.append('status', status);
    const response = await fetch(`${API_BASE}/api/v1/admin/payments/transactions?${params}`);
    return await response.json();
  },

  async getRevenueStats(days = 30) {
    const response = await fetch(`${API_BASE}/api/v1/admin/payments/revenue?days=${days}`);
    return await response.json();
  },

  async getSubscriptions(tier = null, limit = 50) {
    const params = new URLSearchParams({ limit });
    if (tier) params.append('tier', tier);
    const response = await fetch(`${API_BASE}/api/v1/admin/payments/subscriptions?${params}`);
    return await response.json();
  },

  // ============ FREEMIUM ============
  async getQuotaOverview() {
    const response = await fetch(`${API_BASE}/api/v1/admin/freemium/quotas`);
    return await response.json();
  },

  async getUserFreemiumStatus(userId) {
    const response = await fetch(`${API_BASE}/api/v1/admin/freemium/users/${userId}`);
    return await response.json();
  },

  async setUserOverride(userId, overrides) {
    const response = await fetch(`${API_BASE}/api/v1/admin/freemium/users/${userId}/override`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(overrides)
    });
    return await response.json();
  },

  async getTierDistribution() {
    const response = await fetch(`${API_BASE}/api/v1/admin/freemium/tiers/stats`);
    return await response.json();
  },

  // ============ UPSELL ============
  async getUpsellCampaigns() {
    const response = await fetch(`${API_BASE}/api/v1/admin/upsell/campaigns`);
    return await response.json();
  },

  async toggleCampaign(campaignName, enabled) {
    const response = await fetch(
      `${API_BASE}/api/v1/admin/upsell/campaigns/${campaignName}/toggle?enabled=${enabled}`,
      { method: 'PUT' }
    );
    return await response.json();
  },

  async getUpsellAnalytics(days = 30) {
    const response = await fetch(`${API_BASE}/api/v1/admin/upsell/analytics?days=${days}`);
    return await response.json();
  },

  // ============ ONBOARDING ============
  async getOnboardingStats() {
    const response = await fetch(`${API_BASE}/api/v1/admin/onboarding/stats`);
    return await response.json();
  },

  async getOnboardingFlows() {
    const response = await fetch(`${API_BASE}/api/v1/admin/onboarding/flows`);
    return await response.json();
  },

  // ============ TUTORIALS ============
  async getTutorials() {
    const response = await fetch(`${API_BASE}/api/v1/admin/tutorials/list`);
    return await response.json();
  },

  async toggleTutorial(tutorialId, enabled) {
    const response = await fetch(
      `${API_BASE}/api/v1/admin/tutorials/${tutorialId}/toggle?enabled=${enabled}`,
      { method: 'PUT' }
    );
    return await response.json();
  },

  // ============ RULES ============
  async getRules() {
    const response = await fetch(`${API_BASE}/api/v1/admin/rules/list`);
    return await response.json();
  },

  async toggleRule(ruleId, enabled) {
    const response = await fetch(
      `${API_BASE}/api/v1/admin/rules/${ruleId}/toggle?enabled=${enabled}`,
      { method: 'PUT' }
    );
    return await response.json();
  },

  async updateRuleWeight(ruleId, weight) {
    const response = await fetch(
      `${API_BASE}/api/v1/admin/rules/${ruleId}/weight?weight=${weight}`,
      { method: 'PUT' }
    );
    return await response.json();
  },

  // ============ STRATEGY ============
  async getStrategies(limit = 50, userId = null) {
    const params = new URLSearchParams({ limit });
    if (userId) params.append('user_id', userId);
    const response = await fetch(`${API_BASE}/api/v1/admin/strategy/generated?${params}`);
    return await response.json();
  },

  async getStrategyDiagnostics() {
    const response = await fetch(`${API_BASE}/api/v1/admin/strategy/diagnostics`);
    return await response.json();
  },

  // ============ USERS ============
  async getUsers(limit = 50, role = null, tier = null) {
    const params = new URLSearchParams({ limit });
    if (role) params.append('role', role);
    if (tier) params.append('tier', tier);
    const response = await fetch(`${API_BASE}/api/v1/admin/users/list?${params}`);
    return await response.json();
  },

  async getUserDetail(userId) {
    const response = await fetch(`${API_BASE}/api/v1/admin/users/${userId}`);
    return await response.json();
  },

  async updateUserRole(userId, role) {
    const response = await fetch(
      `${API_BASE}/api/v1/admin/users/${userId}/role?role=${role}`,
      { method: 'PUT' }
    );
    return await response.json();
  },

  // ============ LOGS ============
  async getErrorLogs(limit = 100, severity = null) {
    const params = new URLSearchParams({ limit });
    if (severity) params.append('severity', severity);
    const response = await fetch(`${API_BASE}/api/v1/admin/logs/errors?${params}`);
    return await response.json();
  },

  async getWebhookLogs(limit = 100) {
    const response = await fetch(`${API_BASE}/api/v1/admin/logs/webhooks?limit=${limit}`);
    return await response.json();
  },

  async getEventLogs(limit = 100, eventType = null) {
    const params = new URLSearchParams({ limit });
    if (eventType) params.append('event_type', eventType);
    const response = await fetch(`${API_BASE}/api/v1/admin/logs/events?${params}`);
    return await response.json();
  },

  // ============ SETTINGS ============
  async getSettings() {
    const response = await fetch(`${API_BASE}/api/v1/admin/settings`);
    return await response.json();
  },

  async updateSetting(key, value) {
    const response = await fetch(`${API_BASE}/api/v1/admin/settings/${key}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(value)
    });
    return await response.json();
  },

  async getApiKeysStatus() {
    const response = await fetch(`${API_BASE}/api/v1/admin/settings/api-keys`);
    return await response.json();
  },

  async getToggles() {
    const response = await fetch(`${API_BASE}/api/v1/admin/settings/toggles`);
    return await response.json();
  },

  async updateToggle(toggleId, enabled) {
    const response = await fetch(
      `${API_BASE}/api/v1/admin/settings/toggles/${toggleId}?enabled=${enabled}`,
      { method: 'PUT' }
    );
    return await response.json();
  },

  // ============ E-COMMERCE (Phase 1) ============
  async ecommerceGetDashboard() {
    const response = await fetch(`${API_BASE}/api/v1/admin/ecommerce/dashboard`);
    return await response.json();
  },

  async ecommerceGetOrders(limit = 50, status = null) {
    const params = new URLSearchParams({ limit });
    if (status && status !== 'all') params.append('status', status);
    const response = await fetch(`${API_BASE}/api/v1/admin/ecommerce/orders?${params}`);
    return await response.json();
  },

  async ecommerceUpdateOrderStatus(orderId, status) {
    const response = await fetch(`${API_BASE}/api/v1/admin/ecommerce/orders/${orderId}/status?status=${status}`, { method: 'PUT' });
    return await response.json();
  },

  async ecommerceGetProducts(limit = 50, category = null) {
    const params = new URLSearchParams({ limit });
    if (category) params.append('category', category);
    const response = await fetch(`${API_BASE}/api/v1/admin/ecommerce/products?${params}`);
    return await response.json();
  },

  async ecommerceGetSuppliers(limit = 50) {
    const response = await fetch(`${API_BASE}/api/v1/admin/ecommerce/suppliers?limit=${limit}`);
    return await response.json();
  },

  async ecommerceGetCustomers(limit = 50) {
    const response = await fetch(`${API_BASE}/api/v1/admin/ecommerce/customers?limit=${limit}`);
    return await response.json();
  },

  async ecommerceGetCommissions(limit = 50) {
    const response = await fetch(`${API_BASE}/api/v1/admin/ecommerce/commissions?limit=${limit}`);
    return await response.json();
  },

  async ecommerceGetPerformance() {
    const response = await fetch(`${API_BASE}/api/v1/admin/ecommerce/performance`);
    return await response.json();
  },

  async ecommerceGetAlerts() {
    const response = await fetch(`${API_BASE}/api/v1/admin/ecommerce/alerts`);
    return await response.json();
  },

  // ============ CONTENT (Phase 2) ============
  async contentGetCategories() {
    const response = await fetch(`${API_BASE}/api/v1/admin/content/categories`);
    return await response.json();
  },

  async contentCreateCategory(data) {
    const response = await fetch(`${API_BASE}/api/v1/admin/content/categories`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await response.json();
  },

  async contentUpdateCategory(categoryId, data) {
    const response = await fetch(`${API_BASE}/api/v1/admin/content/categories/${categoryId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await response.json();
  },

  async contentDeleteCategory(categoryId) {
    const response = await fetch(`${API_BASE}/api/v1/admin/content/categories/${categoryId}`, { method: 'DELETE' });
    return await response.json();
  },

  async contentGetDepotItems(status = null, limit = 50) {
    const params = new URLSearchParams({ limit });
    if (status) params.append('status', status);
    const response = await fetch(`${API_BASE}/api/v1/admin/content/depot?${params}`);
    return await response.json();
  },

  async contentGetSeoAnalytics() {
    const response = await fetch(`${API_BASE}/api/v1/admin/content/seo-analytics`);
    return await response.json();
  },

  // ============ BACKUP (Phase 2) ============
  async backupGetStats() {
    const response = await fetch(`${API_BASE}/api/v1/admin/backup/stats`);
    return await response.json();
  },

  async backupGetCodeFiles(search = null, limit = 50) {
    const params = new URLSearchParams({ limit });
    if (search) params.append('search', search);
    const response = await fetch(`${API_BASE}/api/v1/admin/backup/code/files?${params}`);
    return await response.json();
  },

  async backupGetPromptVersions(promptType = null, limit = 50) {
    const params = new URLSearchParams({ limit });
    if (promptType) params.append('prompt_type', promptType);
    const response = await fetch(`${API_BASE}/api/v1/admin/backup/prompts?${params}`);
    return await response.json();
  },

  async backupGetDbBackups(limit = 20) {
    const response = await fetch(`${API_BASE}/api/v1/admin/backup/database?limit=${limit}`);
    return await response.json();
  },

  async backupCreateDbBackup(backupType = 'manual', description = '') {
    const params = new URLSearchParams({ backup_type: backupType, description });
    const response = await fetch(`${API_BASE}/api/v1/admin/backup/database?${params}`, { method: 'POST' });
    return await response.json();
  },

  // ============ MAINTENANCE (Phase 3) ============
  async maintenanceGetStatus() {
    const response = await fetch(`${API_BASE}/api/v1/admin/maintenance/status`);
    return await response.json();
  },

  async maintenanceToggle(enabled, message = null, estimatedEnd = null) {
    const params = new URLSearchParams({ enabled });
    if (message) params.append('message', message);
    if (estimatedEnd) params.append('estimated_end', estimatedEnd);
    const response = await fetch(`${API_BASE}/api/v1/admin/maintenance/toggle?${params}`, { method: 'PUT' });
    return await response.json();
  },

  async maintenanceGetAccessRules() {
    const response = await fetch(`${API_BASE}/api/v1/admin/maintenance/access-rules`);
    return await response.json();
  },

  async maintenanceGetAllowedIps() {
    const response = await fetch(`${API_BASE}/api/v1/admin/maintenance/allowed-ips`);
    return await response.json();
  },

  async maintenanceGetLogs(limit = 50) {
    const response = await fetch(`${API_BASE}/api/v1/admin/maintenance/logs?limit=${limit}`);
    return await response.json();
  },

  async maintenanceGetScheduled() {
    const response = await fetch(`${API_BASE}/api/v1/admin/maintenance/scheduled`);
    return await response.json();
  },

  async maintenanceGetSystemStatus() {
    const response = await fetch(`${API_BASE}/api/v1/admin/maintenance/system-status`);
    return await response.json();
  },

  // ============ CONTACTS (Phase 3) ============
  async contactsGetAll(entityType = null, status = null, search = null, limit = 50) {
    const params = new URLSearchParams({ limit });
    if (entityType) params.append('entity_type', entityType);
    if (status) params.append('status', status);
    if (search) params.append('search', search);
    const response = await fetch(`${API_BASE}/api/v1/admin/contacts?${params}`);
    return await response.json();
  },

  async contactsGetStats() {
    const response = await fetch(`${API_BASE}/api/v1/admin/contacts/stats`);
    return await response.json();
  },

  async contactsGetTags() {
    const response = await fetch(`${API_BASE}/api/v1/admin/contacts/tags`);
    return await response.json();
  },

  async contactsCreate(data) {
    const response = await fetch(`${API_BASE}/api/v1/admin/contacts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await response.json();
  },

  async contactsUpdate(contactId, data) {
    const response = await fetch(`${API_BASE}/api/v1/admin/contacts/${contactId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await response.json();
  },

  async contactsDelete(contactId) {
    const response = await fetch(`${API_BASE}/api/v1/admin/contacts/${contactId}`, { method: 'DELETE' });
    return await response.json();
  },

  // ============ HOTSPOTS (Phase 4) ============
  async hotspotsGetStats() {
    const response = await fetch(`${API_BASE}/api/v1/admin/hotspots/dashboard`);
    return await response.json();
  },

  async hotspotsGetListings(status = 'all', limit = 50) {
    const params = new URLSearchParams({ limit });
    if (status && status !== 'all') params.append('status', status);
    const response = await fetch(`${API_BASE}/api/v1/admin/hotspots/listings?${params}`);
    return await response.json();
  },

  async hotspotsGetListingDetail(listingId) {
    const response = await fetch(`${API_BASE}/api/v1/admin/hotspots/listings/${listingId}`);
    return await response.json();
  },

  async hotspotsUpdateStatus(listingId, status) {
    const response = await fetch(`${API_BASE}/api/v1/admin/hotspots/listings/${listingId}/status?new_status=${status}`, { method: 'PUT' });
    return await response.json();
  },

  async hotspotsToggleFeatured(listingId, isFeatured) {
    const response = await fetch(`${API_BASE}/api/v1/admin/hotspots/listings/${listingId}/featured?is_featured=${isFeatured}`, { method: 'PUT' });
    return await response.json();
  },

  async hotspotsGetOwners(limit = 50) {
    const response = await fetch(`${API_BASE}/api/v1/admin/hotspots/owners?limit=${limit}`);
    return await response.json();
  },

  async hotspotsGetRenters(tier = 'all', limit = 50) {
    const params = new URLSearchParams({ limit });
    if (tier && tier !== 'all') params.append('subscription_tier', tier);
    const response = await fetch(`${API_BASE}/api/v1/admin/hotspots/renters?${params}`);
    return await response.json();
  },

  async hotspotsGetAgreements(status = 'all', limit = 50) {
    const params = new URLSearchParams({ limit });
    if (status && status !== 'all') params.append('status', status);
    const response = await fetch(`${API_BASE}/api/v1/admin/hotspots/agreements?${params}`);
    return await response.json();
  },

  async hotspotsGetPricing() {
    const response = await fetch(`${API_BASE}/api/v1/admin/hotspots/pricing`);
    return await response.json();
  },

  async hotspotsUpdatePricing(updates) {
    const response = await fetch(`${API_BASE}/api/v1/admin/hotspots/pricing`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates)
    });
    return await response.json();
  },

  async hotspotsGetRegions() {
    const response = await fetch(`${API_BASE}/api/v1/admin/hotspots/regions`);
    return await response.json();
  },

  async hotspotsGetPurchases(status = 'all', limit = 50) {
    const params = new URLSearchParams({ limit });
    if (status && status !== 'all') params.append('status', status);
    const response = await fetch(`${API_BASE}/api/v1/admin/hotspots/purchases?${params}`);
    return await response.json();
  },

  // ============ NETWORKING (Phase 4) ============
  async networkingGetStats() {
    const response = await fetch(`${API_BASE}/api/v1/admin/networking/dashboard`);
    return await response.json();
  },

  async networkingGetPosts(visibility = null, limit = 50) {
    const params = new URLSearchParams({ limit });
    if (visibility) params.append('visibility', visibility);
    const response = await fetch(`${API_BASE}/api/v1/admin/networking/posts?${params}`);
    return await response.json();
  },

  async networkingTogglePostFeatured(postId, isFeatured) {
    const response = await fetch(`${API_BASE}/api/v1/admin/networking/posts/${postId}/featured?is_featured=${isFeatured}`, { method: 'PUT' });
    return await response.json();
  },

  async networkingTogglePostPinned(postId, isPinned) {
    const response = await fetch(`${API_BASE}/api/v1/admin/networking/posts/${postId}/pinned?is_pinned=${isPinned}`, { method: 'PUT' });
    return await response.json();
  },

  async networkingDeletePost(postId) {
    const response = await fetch(`${API_BASE}/api/v1/admin/networking/posts/${postId}`, { method: 'DELETE' });
    return await response.json();
  },

  async networkingGetGroups(privacy = null, limit = 50) {
    const params = new URLSearchParams({ limit });
    if (privacy) params.append('privacy', privacy);
    const response = await fetch(`${API_BASE}/api/v1/admin/networking/groups?${params}`);
    return await response.json();
  },

  async networkingToggleGroupActive(groupId, isActive) {
    const response = await fetch(`${API_BASE}/api/v1/admin/networking/groups/${groupId}/active?is_active=${isActive}`, { method: 'PUT' });
    return await response.json();
  },

  async networkingGetLeads(status = null, limit = 50) {
    const params = new URLSearchParams({ limit });
    if (status) params.append('status', status);
    const response = await fetch(`${API_BASE}/api/v1/admin/networking/leads?${params}`);
    return await response.json();
  },

  async networkingGetReferrals(status = null, limit = 50) {
    const params = new URLSearchParams({ limit });
    if (status) params.append('status', status);
    const response = await fetch(`${API_BASE}/api/v1/admin/networking/referrals?${params}`);
    return await response.json();
  },

  async networkingGetPendingReferrals() {
    const response = await fetch(`${API_BASE}/api/v1/admin/networking/referrals/pending`);
    return await response.json();
  },

  async networkingVerifyReferral(referralId) {
    const response = await fetch(`${API_BASE}/api/v1/admin/networking/referrals/${referralId}/verify`, { method: 'POST' });
    return await response.json();
  },

  async networkingRejectReferral(referralId, reason = '') {
    const params = new URLSearchParams({ reason });
    const response = await fetch(`${API_BASE}/api/v1/admin/networking/referrals/${referralId}/reject?${params}`, { method: 'POST' });
    return await response.json();
  },

  async networkingGetWallets(limit = 50) {
    const response = await fetch(`${API_BASE}/api/v1/admin/networking/wallets?limit=${limit}`);
    return await response.json();
  },

  async networkingGetReferralCodes(isActive = true, limit = 50) {
    const params = new URLSearchParams({ limit });
    if (isActive !== null) params.append('is_active', isActive);
    const response = await fetch(`${API_BASE}/api/v1/admin/networking/referral-codes?${params}`);
    return await response.json();
  }
};

export default AdminService;
