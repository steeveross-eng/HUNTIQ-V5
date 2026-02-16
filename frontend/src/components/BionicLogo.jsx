/**
 * BionicLogo - Composant Logo Global V5-ULTIME-FUSION
 * 
 * Positionnement: coin supérieur gauche, espace libre
 * Dimensions: ~2.5cm x 2.5cm (96px x 96px à 96dpi)
 * Application: toutes les pages
 */

import React from 'react';
import { Link } from 'react-router-dom';

const BionicLogo = ({ 
  size = 96,  // ~2.5cm à 96dpi
  className = '',
  showOnMobile = true,
  position = 'fixed' // 'fixed' ou 'absolute'
}) => {
  return (
    <Link 
      to="/"
      className={`
        ${position === 'fixed' ? 'fixed' : 'absolute'}
        top-4 left-4
        z-40
        transition-all duration-300
        hover:scale-105
        ${!showOnMobile ? 'hidden md:block' : ''}
        ${className}
      `}
      data-testid="bionic-logo"
      aria-label="BIONIC - Retour à l'accueil"
    >
      <img 
        src="/logos/bionic-logo-official.png"
        alt="BIONIC Chasse / Hunt"
        width={size}
        height={size}
        className="object-contain drop-shadow-lg"
        style={{
          width: `${size}px`,
          height: `${size}px`,
          minWidth: `${size}px`,
          minHeight: `${size}px`
        }}
      />
    </Link>
  );
};

export default BionicLogo;
