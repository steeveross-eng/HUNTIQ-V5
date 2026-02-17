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
  }
};

export default AdminService;
