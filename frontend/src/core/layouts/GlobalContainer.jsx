/**
 * GlobalContainer - BIONIC™ Global Layout Container
 * ==================================================
 * 
 * Container global pour centrer le contenu avec largeur maximale contrôlée.
 * Architecture LEGO V5 - Module isolé.
 * 
 * Règles:
 * - max-width: 1440px (ou configurable)
 * - margin: 0 auto (centrage horizontal)
 * - padding: 24px (responsive)
 * - Compatible avec le header fixe (pt-16)
 * 
 * Usage:
 * <GlobalContainer>
 *   <VotreContenu />
 * </GlobalContainer>
 * 
 * Avec options:
 * <GlobalContainer maxWidth="1280px" noPadding fullHeight>
 *   <VotreContenu />
 * </GlobalContainer>
 */

import React from 'react';

const GlobalContainer = ({ 
  children, 
  className = '',
  maxWidth = '1440px',
  noPadding = false,
  noTopPadding = false,
  fullHeight = false,
  centerContent = false,
  as: Component = 'div'
}) => {
  const baseClasses = [
    'w-full',
    'mx-auto',
    fullHeight ? 'min-h-screen' : '',
    centerContent ? 'flex flex-col items-center justify-center' : '',
    noTopPadding ? '' : 'pt-20',
    noPadding ? '' : 'px-4 sm:px-6 lg:px-8',
    className
  ].filter(Boolean).join(' ');

  const style = {
    maxWidth: maxWidth
  };

  return (
    <Component className={baseClasses} style={style}>
      {children}
    </Component>
  );
};

/**
 * PageContainer - Container de page standard BIONIC™
 * Inclut le padding top pour le header fixe
 */
export const PageContainer = ({ 
  children, 
  className = '',
  title,
  subtitle,
  ...props 
}) => (
  <GlobalContainer className={`py-8 ${className}`} {...props}>
    {(title || subtitle) && (
      <div className="mb-8">
        {title && (
          <h1 className="text-3xl md:text-4xl font-bold text-white golden-text">
            {title}
          </h1>
        )}
        {subtitle && (
          <p className="text-gray-400 mt-2">{subtitle}</p>
        )}
      </div>
    )}
    {children}
  </GlobalContainer>
);

/**
 * SectionContainer - Container de section avec espacement vertical
 */
export const SectionContainer = ({ 
  children, 
  className = '',
  noTopPadding = false,
  ...props 
}) => (
  <GlobalContainer 
    noTopPadding={noTopPadding}
    className={`py-12 md:py-16 ${className}`} 
    {...props}
  >
    {children}
  </GlobalContainer>
);

/**
 * AdminContainer - Container pour les pages admin (sans pt pour sidebar)
 */
export const AdminContainer = ({ 
  children, 
  className = '',
  ...props 
}) => (
  <GlobalContainer 
    maxWidth="100%"
    noTopPadding
    noPadding
    className={className} 
    {...props}
  >
    {children}
  </GlobalContainer>
);

/**
 * ContentContainer - Container de contenu centré avec largeur réduite
 * Idéal pour les articles, formulaires, etc.
 */
export const ContentContainer = ({ 
  children, 
  className = '',
  ...props 
}) => (
  <GlobalContainer 
    maxWidth="960px"
    className={`py-8 ${className}`} 
    {...props}
  >
    {children}
  </GlobalContainer>
);

export default GlobalContainer;
