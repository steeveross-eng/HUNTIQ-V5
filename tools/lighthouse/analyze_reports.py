#!/usr/bin/env python3
"""
HUNTIQ-V5 Lighthouse Report Analyzer
MODE: STAGING (INTERNAL_ONLY=TRUE)
Generates summary and optimization plan from Lighthouse JSON reports
"""

import json
import os
from datetime import datetime
from pathlib import Path

REPORTS_DIR = Path("/app/docs/reports/lighthouse")
OUTPUT_DIR = Path("/app/docs/reports")

# Target scores (non-négociables)
TARGETS = {
    "performance": 95,
    "accessibility": 99,
    "best-practices": 99,
    "seo": 99,
    "global_target": 99.0,
    "aspirational_target": 99.9
}

def load_lighthouse_report(filepath):
    """Load and parse a Lighthouse JSON report"""
    with open(filepath, 'r') as f:
        return json.load(f)

def extract_scores(report):
    """Extract category scores from a Lighthouse report"""
    categories = report.get('categories', {})
    return {
        'performance': round(categories.get('performance', {}).get('score', 0) * 100, 1),
        'accessibility': round(categories.get('accessibility', {}).get('score', 0) * 100, 1),
        'best-practices': round(categories.get('best-practices', {}).get('score', 0) * 100, 1),
        'seo': round(categories.get('seo', {}).get('score', 0) * 100, 1)
    }

def extract_audits_details(report):
    """Extract detailed audit information for optimization"""
    audits = report.get('audits', {})
    issues = {
        'performance': [],
        'accessibility': [],
        'best-practices': [],
        'seo': []
    }
    
    # Map audits to categories
    category_mapping = {
        'performance': [
            'first-contentful-paint', 'largest-contentful-paint', 'total-blocking-time',
            'cumulative-layout-shift', 'speed-index', 'interactive', 'render-blocking-resources',
            'uses-responsive-images', 'offscreen-images', 'unminified-css', 'unminified-javascript',
            'unused-css-rules', 'unused-javascript', 'uses-optimized-images', 'modern-image-formats',
            'uses-text-compression', 'uses-rel-preconnect', 'server-response-time', 'dom-size',
            'critical-request-chains', 'font-display', 'bootup-time', 'mainthread-work-breakdown',
            'third-party-summary', 'largest-contentful-paint-element', 'layout-shift-elements'
        ],
        'accessibility': [
            'color-contrast', 'image-alt', 'label', 'link-name', 'button-name',
            'html-has-lang', 'html-lang-valid', 'meta-viewport', 'aria-required-attr',
            'aria-valid-attr', 'bypass', 'document-title', 'heading-order', 'list',
            'listitem', 'tabindex', 'focus-traps'
        ],
        'best-practices': [
            'is-on-https', 'geolocation-on-start', 'no-document-write', 'external-anchors-use-rel-noopener',
            'js-libraries', 'deprecations', 'errors-in-console', 'image-aspect-ratio',
            'doctype', 'charset', 'valid-source-maps', 'csp-xss'
        ],
        'seo': [
            'viewport', 'document-title', 'meta-description', 'link-text', 'crawlable-anchors',
            'is-crawlable', 'robots-txt', 'image-alt', 'hreflang', 'canonical', 'font-size',
            'tap-targets', 'structured-data'
        ]
    }
    
    for category, audit_ids in category_mapping.items():
        for audit_id in audit_ids:
            audit = audits.get(audit_id, {})
            score = audit.get('score')
            if score is not None and score < 1:
                issues[category].append({
                    'id': audit_id,
                    'title': audit.get('title', audit_id),
                    'score': round(score * 100, 1) if score else 0,
                    'description': audit.get('description', ''),
                    'displayValue': audit.get('displayValue', ''),
                    'warnings': audit.get('warnings', [])
                })
    
    return issues

def analyze_reports():
    """Analyze all Lighthouse reports and generate summary"""
    reports = {}
    all_scores = []
    all_issues = {
        'performance': [],
        'accessibility': [],
        'best-practices': [],
        'seo': []
    }
    
    # Load all reports
    for report_file in REPORTS_DIR.glob("lighthouse_*.json"):
        page_name = report_file.stem.replace("lighthouse_", "").replace("_desktop", "")
        report = load_lighthouse_report(report_file)
        scores = extract_scores(report)
        issues = extract_audits_details(report)
        
        reports[page_name] = {
            'scores': scores,
            'url': report.get('finalUrl', ''),
            'fetchTime': report.get('fetchTime', ''),
            'issues_count': {cat: len(issues[cat]) for cat in issues}
        }
        
        all_scores.append(scores)
        
        # Aggregate issues
        for category in all_issues:
            for issue in issues[category]:
                issue['page'] = page_name
                all_issues[category].append(issue)
    
    # Calculate averages
    averages = {
        'performance': round(sum(s['performance'] for s in all_scores) / len(all_scores), 1),
        'accessibility': round(sum(s['accessibility'] for s in all_scores) / len(all_scores), 1),
        'best-practices': round(sum(s['best-practices'] for s in all_scores) / len(all_scores), 1),
        'seo': round(sum(s['seo'] for s in all_scores) / len(all_scores), 1)
    }
    
    global_average = round(sum(averages.values()) / len(averages), 1)
    
    # Calculate gaps to targets
    gaps = {
        'performance': TARGETS['performance'] - averages['performance'],
        'accessibility': TARGETS['accessibility'] - averages['accessibility'],
        'best-practices': TARGETS['best-practices'] - averages['best-practices'],
        'seo': TARGETS['seo'] - averages['seo'],
        'global': TARGETS['global_target'] - global_average
    }
    
    return {
        'reports': reports,
        'averages': averages,
        'global_average': global_average,
        'gaps': gaps,
        'all_issues': all_issues
    }

def generate_optimization_plan(analysis):
    """Generate prioritized optimization plan"""
    issues = analysis['all_issues']
    gaps = analysis['gaps']
    
    # Prioritize by gap size
    priority_order = sorted(gaps.items(), key=lambda x: x[1], reverse=True)
    
    plan = {
        'priority_categories': [],
        'critical_fixes': [],
        'high_priority': [],
        'medium_priority': [],
        'low_priority': []
    }
    
    for category, gap in priority_order:
        if category == 'global':
            continue
        if gap > 0:
            plan['priority_categories'].append({
                'category': category,
                'gap': gap,
                'issues_count': len(issues.get(category, []))
            })
    
    # Categorize fixes by score
    for category, category_issues in issues.items():
        for issue in category_issues:
            fix = {
                'category': category,
                'audit_id': issue['id'],
                'title': issue['title'],
                'score': issue['score'],
                'page': issue['page'],
                'description': issue.get('displayValue', '')
            }
            
            if issue['score'] < 50:
                plan['critical_fixes'].append(fix)
            elif issue['score'] < 75:
                plan['high_priority'].append(fix)
            elif issue['score'] < 90:
                plan['medium_priority'].append(fix)
            else:
                plan['low_priority'].append(fix)
    
    # Deduplicate and sort
    for priority in ['critical_fixes', 'high_priority', 'medium_priority', 'low_priority']:
        seen = set()
        unique = []
        for fix in plan[priority]:
            key = (fix['category'], fix['audit_id'])
            if key not in seen:
                seen.add(key)
                unique.append(fix)
        plan[priority] = sorted(unique, key=lambda x: x['score'])
    
    return plan

def main():
    print("=" * 60)
    print("HUNTIQ-V5 LIGHTHOUSE REPORT ANALYZER")
    print("MODE: STAGING (INTERNAL_ONLY=TRUE)")
    print("=" * 60)
    
    # Analyze reports
    analysis = analyze_reports()
    
    # Print summary
    print("\n📊 SCORES PAR PAGE:")
    print("-" * 40)
    for page, data in analysis['reports'].items():
        scores = data['scores']
        print(f"\n  {page.upper()}:")
        print(f"    Performance:    {scores['performance']}")
        print(f"    Accessibility:  {scores['accessibility']}")
        print(f"    Best Practices: {scores['best-practices']}")
        print(f"    SEO:            {scores['seo']}")
    
    print("\n📈 MOYENNES GLOBALES:")
    print("-" * 40)
    for cat, score in analysis['averages'].items():
        target = TARGETS.get(cat, 99)
        gap = target - score
        status = "✅" if gap <= 0 else "🔴" if gap > 10 else "🟡"
        print(f"  {status} {cat}: {score} (cible: {target}, écart: {gap:+.1f})")
    
    print(f"\n  🎯 Score Global: {analysis['global_average']} (cible: {TARGETS['global_target']})")
    
    # Generate optimization plan
    optimization_plan = generate_optimization_plan(analysis)
    
    print("\n🔧 PLAN D'OPTIMISATION:")
    print("-" * 40)
    print(f"  Corrections critiques: {len(optimization_plan['critical_fixes'])}")
    print(f"  Haute priorité: {len(optimization_plan['high_priority'])}")
    print(f"  Priorité moyenne: {len(optimization_plan['medium_priority'])}")
    print(f"  Priorité basse: {len(optimization_plan['low_priority'])}")
    
    # Save summary report
    summary = {
        "report_id": "LIGHTHOUSE_L1_SUMMARY",
        "generated_at": datetime.now().isoformat(),
        "mode": "STAGING",
        "internal_only": True,
        "pages_audited": list(analysis['reports'].keys()),
        "scores_by_page": analysis['reports'],
        "average_scores": analysis['averages'],
        "global_average": analysis['global_average'],
        "targets": TARGETS,
        "gaps_to_target": analysis['gaps'],
        "target_achieved": analysis['global_average'] >= TARGETS['global_target'],
        "optimization_needed": any(g > 0 for g in analysis['gaps'].values())
    }
    
    with open(OUTPUT_DIR / "LIGHTHOUSE_L1_SUMMARY.json", 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\n✅ Summary saved: {OUTPUT_DIR / 'LIGHTHOUSE_L1_SUMMARY.json'}")
    
    # Save optimization plan
    plan_report = {
        "report_id": "LIGHTHOUSE_L1_OPTIMIZATION_PLAN",
        "generated_at": datetime.now().isoformat(),
        "mode": "STAGING",
        "internal_only": True,
        "current_global_score": analysis['global_average'],
        "target_score": TARGETS['global_target'],
        "aspirational_score": TARGETS['aspirational_target'],
        "priority_categories": optimization_plan['priority_categories'],
        "fixes": {
            "critical": optimization_plan['critical_fixes'][:20],
            "high": optimization_plan['high_priority'][:20],
            "medium": optimization_plan['medium_priority'][:20],
            "low": optimization_plan['low_priority'][:10]
        },
        "total_issues": {
            "critical": len(optimization_plan['critical_fixes']),
            "high": len(optimization_plan['high_priority']),
            "medium": len(optimization_plan['medium_priority']),
            "low": len(optimization_plan['low_priority'])
        },
        "recommended_actions": [
            "1. Corriger tous les problèmes critiques (score < 50)",
            "2. Optimiser les images (formats modernes, lazy loading)",
            "3. Éliminer les ressources bloquantes (CSS/JS critiques)",
            "4. Améliorer l'accessibilité (contraste, labels, aria)",
            "5. Optimiser les Core Web Vitals (LCP, CLS, TBT)",
            "6. Compresser et minifier les assets",
            "7. Implémenter le preconnect/prefetch"
        ]
    }
    
    with open(OUTPUT_DIR / "LIGHTHOUSE_L1_OPTIMIZATION_PLAN.json", 'w') as f:
        json.dump(plan_report, f, indent=2)
    print(f"✅ Plan saved: {OUTPUT_DIR / 'LIGHTHOUSE_L1_OPTIMIZATION_PLAN.json'}")
    
    print("\n" + "=" * 60)
    print("ANALYSE LIGHTHOUSE TERMINÉE")
    print("=" * 60)

if __name__ == "__main__":
    main()
